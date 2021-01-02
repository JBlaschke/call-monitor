#!/usr/bin/env python
# -*- coding: utf-8 -*-



import setuptools



with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="callmonitor",
    version="0.3.2",
    author="Johannes Blaschke",
    author_email="johannes@blaschke.science",
    description="A light-weight package that allows you to monitor function calls with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBlaschke/call-monitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
      'numpy',
    ],
)
