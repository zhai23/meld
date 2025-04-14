# Copyright (C) 2018-2024 Kai Willadsen <kai.willadsen@gmail.com>
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

from gi.repository import Gio


def replace_menu_section(menu: Gio.Menu, section: Gio.MenuItem):
    """Replaces an existing section in GMenu `menu` with `section`

    The sections are compared by their `id` attributes, with the
    matching section in `menu` being replaced by the passed `section`.

    If there is no section in `menu` that matches `section`'s `id`
    attribute, a ValueError is raised.
    """
    section_id = section.get_attribute_value("id").get_string()
    for idx in range(menu.get_n_items()):
        item_id = menu.get_item_attribute_value(idx, "id").get_string()
        if item_id == section_id:
            break
    else:
        # FIXME: Better exception
        raise ValueError("Section %s not found" % section_id)
    menu.remove(idx)
    menu.insert_item(idx, section)
