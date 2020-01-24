from distutils.core import setup
import setuptools


setup(
    name="ottopy",
    version="0.0.1",
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

