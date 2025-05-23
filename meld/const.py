# Copyright (C) 2014-2024 Kai Willadsen <kai.willadsen@gmail.com>
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

import enum
from typing import Dict, Final, Tuple

from gi.repository import GtkSource

from meld.conf import _


class ActionMode(enum.IntEnum):
    """Action mode for chunk change actions"""
    Replace: Final[int] = 0
    Delete: Final[int] = 1
    Insert: Final[int] = 2


class ChunkAction(enum.Enum):
    delete: Final[str] = 'delete'
    replace: Final[str] = 'replace'
    copy_down: Final[str] = 'copy_down'
    copy_up: Final[str] = 'copy_up'


class FileComparisonMode(enum.Enum):
    AutoMerge: Final[str] = 'AutoMerge'
    Compare: Final[str] = 'Compare'


class FileLoadError(enum.IntEnum):
    LINE_TOO_LONG: Final[int] = 1


NEWLINES: Dict[GtkSource.NewlineType, Tuple[str, str]] = {
    GtkSource.NewlineType.LF: ('\n', _("UNIX (LF)")),
    GtkSource.NewlineType.CR_LF: ('\r\n', _("DOS/Windows (CR-LF)")),
    GtkSource.NewlineType.CR: ('\r', _("Mac OS (CR)")),
}

FILE_FILTER_ACTION_FORMAT: Final[str] = 'folder-custom-filter-{}'
TEXT_FILTER_ACTION_FORMAT: Final[str] = 'text-custom-filter-{}'

#: Sentinel value for mtimes on files that don't exist.
MISSING_TIMESTAMP: Final[int] = -2147483648
