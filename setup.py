import os
from pathlib import Path

from setuptools import setup


with open("uetools/core/__init__.py") as file:
    for line in file.readlines():
        if 'version' in line:
            version = line.split('=')[1].strip().replace('"', "")
            break

assert os.path.exists(os.path.join('uetools', '__init__.py')) is False, "uetools is a namespace not a module"


setup_kwargs = dict(
    name='uetools',
    version=version,
    description='Tools for Unreal Engine',
    long_description=(Path(__file__).parent / "README.rst").read_text(),
    author='Pierre Delaunay',
    author_email='pierre@delaunay.io',
    license='BSD-3-Clause',
    url="https://uetools.readthedocs.io",
    packages=[
        'uetools.core',
        'uetools.commands',
        'uetools.format',
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    zip_safe=True,
    setup_requires=['setuptools'],
    install_requires=["appdirs", "colorama", "cookiecutter", "simple-parsing", "GitPython"],
    python_requires='>=3.7.*',
    entry_points={
        'console_scripts': [
            'uecli = uetools.core.cli:main',
        ]
    },
    package_data={
        "uetools": [
            'uetools/templates/TemplateServer.Target.cs'
        ]
    },
    include_package_data=True,
)

if __name__ == "__main__":
    setup(**setup_kwargs)
