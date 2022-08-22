from setuptools import setup


setup_kwargs = dict(
    name='uetools',
    version='0.0.0',
    description='Tools for Unreal Engine',
    author='Pierre Delaunay',
    author_email='pierre@delaunay.io',
    license='BSD-3-Clause',
    url="https://uetools.readthedocs.io",
    packages=[
        'uetools',
        'uetools.commands',
    ],
    zip_safe=True,
    setup_requires=['setuptools'],
    install_requires=["appdirs", "colorama", "cookiecutter"],
    python_requires='>=3.7.*',
    entry_points={
        'console_scripts': [
            'uecli = uetools.cli:main',
        ]
    },
    package_data={
        "uetools": [
            'uetools/templates/TemplateServer.Target.cs'
        ]
    },
)

if __name__ == "__main__":
    setup(**setup_kwargs)
