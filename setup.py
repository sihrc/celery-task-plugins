#!/usr/bin/env python
from setuptools import find_packages, setup

redis_chain_store_requires = ["redis==3.2.1", "hiredis==1.0.0"]

setup(
    name="celery_task_plugins",
    version="0.1",
    description="Celery task plugins that wrap celery tasks",
    author="Chris Lee",
    author_email="sihrc.c.lee@gmail.com",
    packages=find_packages(),
    install_requires=["celery>=4.3.0"],
    extras_require={
        "redis_chain_store": redis_chain_store_requires,
        "test": ["pytest"] + redis_chain_store_requires,
    },
)
