from distutils.core import setup, Extension
from Cython.Build import cythonize

import numpy
# setup(ext_modules = cythonize(Extension(
#     'interface',
#     sources=['interface.pyx'],
#     language='c++',
#     include_dirs=[numpy.get_include()],
#     extra_compile_args=['-Wno-unused-function', '-std=c++11','-mmacosx-version-min=10.9'],
#     library_dirs=[],
#     libraries=[],
#     extra_link_args=[]
# )))


setup(
    name = 'interface_c',
    ext_modules = cythonize("interface.pyx"),
    language='c',
    include_dirs=[numpy.get_include()],

)