import re
from setuptools import setup, find_packages

with open("lernsax/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

with open("requirements.txt", "r") as file:
    INSTALL_REQUIRES = file.readlines()

with open("README.md") as readme:
    setup(
        name="lernsax",
        version=version,
        description="A Python Async LernSax Client",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        license="MIT License",
        author="okok7711",
        author_email="okok7711@etstun.de",
        url="https://github.com/okok7711/lernsax",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
        keywords="lernsax, client, files, internet, download, upload, sachsen, deutschland, ostdeutschland",
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(),
    )