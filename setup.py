from setuptools import find_packages
from setuptools import setup

def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()
#
setup(
    name="geminikit",
    version="1.1.8",
    author="paviththanan",
    author_email="rkpavi06@gmail.com",
    description="The python package that returns Response of Google Gemini through Cookies.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/rekcah-pavi/geminikit",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    install_requires=[
        "httpx",
    ],
    keywords="Python, API, Gemini, Google Gemini, Large Language Model, Chatbot API, Google API, Chatbot",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
