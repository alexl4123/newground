import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install


#class CustomBuildExt(build_ext):
class CustomBuildExt(install):
    def run(self):
        # Run the Makefile to compile Cython and C code
        subprocess.check_call(["make", "compile-heuristic-cython-c"])
        subprocess.check_call(["make", "compile-nagg-cython"])
        super().run()


setup(
    name="newground",
    version="3.00.8",
    packages=find_packages(where=""),
    #cmdclass={"build_ext": CustomBuildExt},
    cmdclass={"install": CustomBuildExt},
    entry_points={
        "console_scripts": [
            "newground=heuristic_splitter:main",
        ],
    },
    package_data={
        "heuristic_splitter": ["*.c", "*.so", "**/*.so"],
        "cython_nagg": ["*.so", "**/*.so"],
    },
    include_package_data=True,
)
