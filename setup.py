#!/usr/bin/env python
#
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

from __future__ import print_function
depsOK = True

try:
    from setuptools import setup, find_packages
    from setuptools.extension import Extension
except ImportError:
    print("Setuptools must be installed - see http://pypi.python.org/pypi/setuptools")

try:
    import numpy
except ImportError:
    depsOK = False
    print("NumPy should be installed first from suitable binaries.")
    print("See http://numpy.scipy.org/")

try:
    import scipy
except ImportError:
    depsOK = False
    print("SciPy should be installed first from suitable binaries.")
    print("See http://www.scipy.org/")

try:
    import matplotlib
except ImportError:
    depsOK = False
    print("Matplotlib should be installed first from suitable binaries.")
    print("See http://matplotlib.sf.net/")

try:
    import mayavi
    HAS_MAYAVI = True
except ImportError:
    try:
        import enthought.mayavi
    except ImportError:
        HAS_MAYAVI = False
        
try:
    #from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    USE_CYTHON = True
    print("Using Cython to compile modules")
except ImportError:
    USE_CYTHON = False
    print("Using C sources for modules")

if USE_CYTHON:
    def c_to_pyx(sources):
        c2p = lambda path: path.strip().rsplit('.c')[0] + '.pyx'
        return [c2p(path) for path in sources]
else:
    def c_to_pyx(sources):
        return sources

natural_neighbour_sources = [
    'imusim/maths/natural_neighbour.{}'.format('pyx' if USE_CYTHON else 'c'),
    'imusim/maths/natural_neighbour/utils.c',
    'imusim/maths/natural_neighbour/delaunay.c',
    'imusim/maths/natural_neighbour/natural.c'
]

ext_modules = [
    Extension("imusim.maths.quaternions",
              c_to_pyx(['imusim/maths/quaternions.c'])),
    Extension("imusim.maths.quat_splines",
              c_to_pyx(['imusim/maths/quat_splines.c'])),
    Extension("imusim.maths.vectors",
              c_to_pyx(['imusim/maths/vectors.c'])),
    Extension("imusim.maths.natural_neighbour",
              natural_neighbour_sources)
]

if USE_CYTHON:
    ext_modules = cythonize(ext_modules)
    
packages = find_packages()

if not HAS_MAYAVI:
    print('Building without mayavi')
    print(packages)
    packages.remove('imusim.visualisation')

if depsOK:
    setup(
        name = "imusim",
        version = "0.2",
        author = "Alex Young and Martin Ling",
        license = "GPLv3",
        url = "http://www.imusim.org/",
        install_requires = ["simpy>=2.3,<3", "pyparsing"],
        packages = packages,
        include_dirs = [numpy.get_include()],
        ext_modules = ext_modules
    )

