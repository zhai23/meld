# The original C implementation is part of the GTK+ project, under
#   gtk+/demos/gtk-demo/foreigndrawing.c
#
# This Python port of portions of the original source code is copyright
# (C) 2009-2015 Kai Willadsen <kai.willadsen@gmail.com>, and is released
# under the same LGPL version 2 (or later) license.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.


import logging
import re

from gi.repository import GObject, Gtk

log = logging.getLogger(__name__)


def append_element(path, selector):
    pseudo_classes = [
        ('active',        Gtk.StateFlags.ACTIVE),
        ('hover',         Gtk.StateFlags.PRELIGHT),
        ('selected',      Gtk.StateFlags.SELECTED),
        ('disabled',      Gtk.StateFlags.INSENSITIVE),
        ('indeterminate', Gtk.StateFlags.INCONSISTENT),
        ('focus',         Gtk.StateFlags.FOCUSED),
        ('backdrop',      Gtk.StateFlags.BACKDROP),
        ('dir(ltr)',      Gtk.StateFlags.DIR_LTR),
        ('dir(rtl)',      Gtk.StateFlags.DIR_RTL),
        ('link',          Gtk.StateFlags.LINK),
        ('visited',       Gtk.StateFlags.VISITED),
        ('checked',       Gtk.StateFlags.CHECKED),
        ('drop(active)',  Gtk.StateFlags.DROP_ACTIVE)
    ]

    toks = [t for t in re.split(r'([#\.:])', selector) if t]
    elements = [toks[i] + toks[i + 1] for i in range(1, len(toks), 2)]

    name = toks[0]
    if name[0].isupper():
        gtype = GObject.GType.from_name(name)
        if gtype == GObject.TYPE_INVALID:
            log.error('Unknown type name "%s"', name)
            return
        path.append_type(gtype)
    else:
        # Omit type, we're using name
        path.append_type(GObject.TYPE_NONE)
        path.iter_set_object_name(-1, name)

    for segment in elements:
        segment_type = segment[0]
        name = segment[1:]
        if segment_type == '#':
            path.iter_set_name(-1, name)
            break
        elif segment_type == '.':
            path.iter_add_class(-1, name)
            break
        elif segment_type == ':':
            for class_name, class_state in pseudo_classes:
                if name == class_name:
                    path.iter_set_state(
                        -1, path.iter_get_state(-1) | class_state)
                    break
            else:
                log.error('Unknown pseudo-class :%s', name)
                pass
            break
        else:
            assert False


def create_context_for_path(path, parent):
    context = Gtk.StyleContext.new()
    context.set_path(path)
    context.set_parent(parent)
    context.set_state(path.iter_get_state(-1))
    return context


def get_style(parent, selector):
    if parent:
        path = Gtk.WidgetPath.copy(parent.get_path())
    else:
        path = Gtk.WidgetPath.new()
    append_element(path, selector)
    return create_context_for_path(path, parent)
