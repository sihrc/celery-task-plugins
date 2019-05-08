#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="celery-task-plugins",
    version="0.1",
    description="Celery task plugins that wrap celery tasks",
    author="Chris Lee",
    author_email="sihrc.c.lee@gmail.com",
    packages=find_packages(),
    install_requires=[],
    extras_require={"test": ["pytest"]},
)
