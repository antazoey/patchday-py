#!/usr/bin/env python
from setuptools import find_packages, setup

extras_require = {
    "test": [
        "pytest>=6.0",
        "pytest-xdist",
        "pytest-cov",
        "hypothesis>=6.2.0,<7.0",
    ],
    "lint": [
        "ruff>=0.11.0",
        "mypy>=1.13.0,<2",
        "types-setuptools",
        "types-requests",
        "mdformat>=0.7.19",
        "mdformat-gfm>=0.3.5",
        "mdformat-frontmatter>=0.4.1",
        "mdformat-pyproject>=0.0.2",
    ],
    "release": [
        "setuptools>=75.6.0",
        "wheel",
        "twine",
    ],
    "dev": [
        "commitizen",
        "pre-commit",
    ],
}

extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="patchday",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""patchday: HRT schedule in Python""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="antazoey",
    author_email="admin@antazoey.me",
    url="https://github.com/antazoey/patchday-py",
    include_package_data=True,
    install_requires=[
        "pydantic>=2.10.4,<3",
    ],
    python_requires=">=3.9,<4",
    extras_require=extras_require,
    py_modules=["patchday"],
    license="Apache-2.0",
    zip_safe=False,
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"patchday": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
