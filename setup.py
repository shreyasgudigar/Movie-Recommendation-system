from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

REPO_NAME = "CineMatch"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit', 'requests', 'pandas']


setup(
    name=SRC_REPO,
    version="1.0.0",
    description="CineMatch - A content-based movie recommendation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
