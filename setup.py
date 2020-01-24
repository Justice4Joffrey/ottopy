from distutils.core import setup
import setuptools


setuptools.setup(
    name="ottopy",
    version="0.1.0",
    author="Otto Castle",
    author_email="otto.castle1@gmail.com",
    description="Python tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

