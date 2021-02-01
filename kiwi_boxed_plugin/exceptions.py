# Copyright (c) 2020 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of kiwi-boxed-build.
#
# kiwi-boxed-build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi-boxed-build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi-boxed-build.  If not, see <http://www.gnu.org/licenses/>
#
from kiwi.exceptions import KiwiError


class KiwiBoxPluginConfigError(KiwiError):
    """
    Exception raised if the box config yaml file is invalid
    """


class KiwiBoxPluginBoxNameError(KiwiError):
    """
    Exception raised if the boxname could not be found
    """


class KiwiBoxPluginVirtioFsError(KiwiError):
    """
    Exception raised if virtiofsd does not start
    """


class KiwiBoxPluginArchNotFoundError(KiwiError):
    """
    Exception raised if the selected architecture has no configuration
    """
