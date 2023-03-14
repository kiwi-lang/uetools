
from pathlib import Path

setup_kwargs = dict(
    name='{{cookiecutter.plugin_name}}',
    version='0.0.0',
    description='{{cookiecutter.plugin_description}}',
    long_description=(Path(__file__).parent / "README.rst").read_text(),
    author='{{cookiecutter.plugin_author}}',
    author_email='@',
    license='BSD-3-Clause',
    url="https://{{cookiecutter.gitlab_org}}.gitlab.io/{{cookiecutter.gitlab_repo}}/o",
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
    python_requires='>=3.8',
)


if __name__ == "__main__":
    from setuptools import setup
    setup(**setup_kwargs)
