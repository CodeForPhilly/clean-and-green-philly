"""
Note: `pip install --user pybind11` mandatory. Did not really test if the
instal_requires and import workaround below works. If not, just install it
manually first.

Credits:
- https://pybind11.readthedocs.io/en/latest/compiling.html
- https://github.com/pybind/python_example
"""

from setuptools import setup, find_packages

from pybind11.setup_helpers import Pybind11Extension, build_ext


ext_modules = [
    Pybind11Extension(
        # Module name (toplevel same as python, then same as in C++ file)
        name="awkde.backend",
        sources=["cpp/backend.cpp"],
        extra_compile_args=["-O3"],  # "-ggdb" for debugging stuff
    ),
]

setup(
    name="awkde",
    version="0.1",
    author="Thorben Menne",
    author_email="thorben.menne@tu-dortmund.de",
    url="https://github.com/mennthor/awkde",
    description="Adaptive width gaussian KDE",
    packages=find_packages(),
    install_requires=["numpy", "scipy", "scikit-learn", "pybind11", "future"],
    ext_modules=ext_modules,  # Compiled external modules
    cmdclass={"build_ext": build_ext},  # Finds highest supported C++ version
)
