from setuptools import setup, find_packages
import os

def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from files
install_requires = read_requirements('requirements.txt')
dev_requires = read_requirements('requirements_dev.txt')

setup(
    name="requmancer",
    version="0.1.0",
    author="ParisNeo",
    author_email="parisneoai@gmail.com",
    description="A tool to generate requirements files from Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParisNeo/requmancer",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "requmancer=requmancer.main:main",
        ],
    },
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
)