"""
Package which imports all commonly used symbols from IMUSim.
"""
# Copyright (C) 2009-2011 University of Edinburgh
#
# This file is part of IMUSim.
#
# IMUSim is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IMUSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IMUSim.  If not, see <http://www.gnu.org/licenses/>.

import pkgutil
import os
import inspect

__all__ = []
# adapted from code by hovren
try:
    # Python 3
    path = os.path.split(os.path.split(pkgutil.get_loader('imusim').path)[0])[0]
except AttributeError:
    # Python 2
    path = os.path.split(pkgutil.get_loader('imusim').filename)[0]

for loader, modname, ispkg in pkgutil.walk_packages([path]):
    if modname.startswith('imusim') \
            and not modname.startswith('imusim.tests') \
            and not modname.startswith('imusim.all'):
        exec("import %s" % modname)
        exec("module = %s" % modname)

        #symbols = filter(lambda o: not inspect.ismodule(o), module.__all__ if hasattr(module,'__all__') else dir(module))
        symbols = [o for o in (module.__all__ if hasattr(module,'__all__') else dir(module)) if not inspect.ismodule(o)]
        symbols = [s for s in symbols if not s.startswith('_')]
        exec("from %s import *" % modname)
        __all__ += symbols
