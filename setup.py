from setuptools import setup
import os

THIS_DIR = os.path.dirname(__file__)
VERSION_FILE = os.path.join(THIS_DIR, 'go_game', '__init__.py')

def get_version():
    with open(VERSION_FILE) as f:
        lines = f.readlines()
    version_line = [l for l in lines if '__version__' in l][0]
    version = version_line.split('=')[-1].strip()[1:-1]
    return version

setup(name='go_game',
      version=get_version(),
      description='Go game with a CLI',
      url='https://github.com/MadATF2727/go_game.git',
      author='Arna Friend',
      author_email='arnafriend@gmail.com',
      license='MIT',
      packages=['go_game'],
      zip_safe=False,
      install_requires=[
            'importlib-metadata ~= 1.0 ; python_version < "3.8"',
      ],
      )