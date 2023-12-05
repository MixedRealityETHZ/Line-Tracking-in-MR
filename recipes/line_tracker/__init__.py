from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
from pythonforandroid.util import ensure_dir

from os.path import join
import shutil


class LineTrackerRecipe(CppCompiledComponentsPythonRecipe):

    # version = '0.0.0'
    branch = 'main'
    # url = 'https://github.com/KimSinjeong/elsed_eth_mr/archive/refs/heads/main.zip'
    url = 'git+https://github.com/AidynUbingazhibov/Mixed-Reality-Pybind.git'

    depends = ['setuptools', 'pybind11', 'python3', 'opencv', 'opencv_extras']
    patches = ['CMakeLists.patch']

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        opencv = self.get_recipe('opencv', self.ctx)
        opencv_inc_dir = join(opencv.get_build_dir(arch.arch), 'build')

        env['OpenCV_LOCATION'] = opencv_inc_dir

        python = self.get_recipe('python3', self.ctx)
        python = python.get_build_dir(arch.arch)
        python_inc_dir = join(python, 'Include')
        python_lib_dir = join(python, 'android-build')
        
        env['PYTHON_INCLUDE_DIR'] = python_inc_dir
        env['PYTHON_LIBRARY'] = python_lib_dir

        return env


recipe = LineTrackerRecipe()
