from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1"

REPO_NAME = "DataSciecne_Project_forcasting"
AUTHOR_USER_NAME = "sheshpal"
SRC_REPO = "forcastingproject"

setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    description="Sales Forecasting End-to-End MLOps Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)

