# Copyright (C) 2002-2006 Stephen Kennedy <stevek@gnome.org>
# Copyright (C) 2009-2010, 2013 Kai Willadsen <kai.willadsen@gmail.com>
# Copyright (C) 2025 Christoph Brill <opensource@christophbrill.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import difflib
import os
from typing import Any, Dict, List, Optional, Tuple, cast

from gi.repository import Gdk, Gio, GLib, Gtk, GtkSource

from meld.conf import _
from meld.iohelpers import prompt_save_filename
from meld.misc import error_dialog
from meld.settings import MeldSettings, get_meld_settings
from meld.sourceview import LanguageManager


@Gtk.Template(resource_path='/org/gnome/meld/ui/patch-dialog.ui')
class PatchDialog(Gtk.Dialog):

    __gtype_name__ = "PatchDialog"

    left_radiobutton: Gtk.RadioButton = Gtk.Template.Child("left_radiobutton")
    reverse_checkbutton: Gtk.CheckButton = Gtk.Template.Child("reverse_checkbutton")
    right_radiobutton: Gtk.RadioButton = Gtk.Template.Child("right_radiobutton")
    side_selection_box: Gtk.Box = Gtk.Template.Child("side_selection_box")
    side_selection_label: Gtk.Label = Gtk.Template.Child("side_selection_label")
    textview: Gtk.TextView = Gtk.Template.Child("textview")

    def __init__(self, filediff: Any) -> None:
        super().__init__()

        self.set_transient_for(filediff.get_toplevel())
        self.filediff = filediff

        buf: GtkSource.Buffer = GtkSource.Buffer()
        self.textview.set_buffer(buf)
        lang: Optional[GtkSource.Language] = LanguageManager.get_language_from_mime_type("text/x-diff")
        buf.set_language(lang)
        buf.set_highlight_syntax(True)

        self.index_map: Dict[Gtk.RadioButton, Tuple[int, int]] = {
            self.left_radiobutton: (0, 1),
            self.right_radiobutton: (1, 2)
        }
        self.left_patch: bool = True
        self.reverse_patch: bool = self.reverse_checkbutton.get_active()

        if self.filediff.num_panes < 3:
            self.side_selection_label.hide()
            self.side_selection_box.hide()

        meld_settings: MeldSettings = get_meld_settings()
        self.textview.modify_font(meld_settings.font)
        self.textview.set_editable(False)
        meld_settings.connect('changed', self.on_setting_changed)

    def on_setting_changed(self, settings: MeldSettings, key: str) -> None:
        if key == "font":
            self.textview.modify_font(settings.font)

    @Gtk.Template.Callback()
    def on_buffer_selection_changed(self, radiobutton: Gtk.RadioButton) -> None:
        if not radiobutton.get_active():
            return
        self.left_patch = radiobutton == self.left_radiobutton
        self.update_patch()

    @Gtk.Template.Callback()
    def on_reverse_checkbutton_toggled(self, checkbutton: Gtk.CheckButton) -> None:
        self.reverse_patch = checkbutton.get_active()
        self.update_patch()

    def update_patch(self) -> None:
        indices: Tuple[int, int] = (0, 1)
        if not self.left_patch:
            indices = (1, 2)
        if self.reverse_patch:
            indices = (indices[1], indices[0])

        texts: List[List[str]] = []
        for b in self.filediff.textbuffer:
            start, end = b.get_bounds()
            text: str = b.get_text(start, end, False)
            lines: List[str] = text.splitlines(True)

            # Ensure that the last line ends in a newline
            barelines: List[str] = text.splitlines(False)
            if barelines and lines and barelines[-1] == lines[-1]:
                # Final line lacks a line-break; add in a best guess
                if len(lines) > 1:
                    previous_linebreak: str = lines[-2][len(barelines[-2]):]
                else:
                    previous_linebreak: str = "\n"
                lines[-1] += previous_linebreak

            texts.append(lines)

        names: List[str] = [self.filediff.textbuffer[i].data.label for i in range(3)]
        prefix: str = os.path.commonprefix(names)
        names = [n[prefix.rfind("/") + 1:] for n in names]

        buf: GtkSource.Buffer = cast(GtkSource.Buffer, self.textview.get_buffer())
        text0, text1 = texts[indices[0]], texts[indices[1]]
        name0, name1 = names[indices[0]], names[indices[1]]

        diff = difflib.unified_diff(text0, text1, name0, name1)
        diff_text: str = "".join(d for d in diff)
        buf.set_text(diff_text)

    def save_patch(self, targetfile: Gio.File) -> None:
        buf: GtkSource.Buffer = self.textview.get_buffer()
        sourcefile: GtkSource.File = GtkSource.File.new()
        saver: GtkSource.FileSaver = GtkSource.FileSaver.new_with_target(
            buf, sourcefile, targetfile)
        saver.save_async(
            GLib.PRIORITY_HIGH,
            callback=self.file_saved_cb,
        )

    def file_saved_cb(self, saver: GtkSource.FileSaver, result: Gio.AsyncResult, *args: Any) -> None:
        gfile: Gio.File = saver.get_location()
        try:
            saver.save_finish(result)
        except GLib.Error as err:
            filename: str = GLib.markup_escape_text(gfile.get_parse_name())
            error_dialog(
                primary=_("Could not save file %s.") % filename,
                secondary=_("Couldn’t save file due to:\n%s") % (
                    GLib.markup_escape_text(str(err))),
            )

    def run(self) -> int:
        self.update_patch()

        result: int = super().run()
        if result < 0:
            self.hide()
            return

        # Copy patch to clipboard
        if result == 1:
            buf: Gtk.TextBuffer = self.textview.get_buffer()
            start, end = buf.get_bounds()
            clip: Gtk.Clipboard = Gtk.Clipboard.get_default(Gdk.Display.get_default())
            clip.set_text(buf.get_text(start, end, False), -1)
            clip.store()
        # Save patch as a file
        else:
            gfile: Optional[Gio.File] = prompt_save_filename(_("Save Patch"))
            if gfile:
                self.save_patch(gfile)

        self.hide()
