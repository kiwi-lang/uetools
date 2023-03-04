
setup_kwargs = dict(
    name='{{cookiecutter.plugin_name}}',
    version='0.0.0',
    description='',
    author='',
    author_email='@',
    license='BSD-3-Clause',
    url="https://gamekit.readthedocs.io",
    packages=[
        '{{cookiecutter.plugin_name}}',
    ],
    package_dir={"": "Source/python"},
    namespace_packages=[
        '{{cookiecutter.plugin_name}}',
    ],
    zip_safe=True,
    setup_requires=['setuptools'],
    install_requires=[],
    python_requires='>=3.7.*',
)


if __name__ == "__main__":
    from setuptools import setup
    setup(**setup_kwargs)
