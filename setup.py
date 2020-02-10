from setuptools import setup, find_packages
import os

version = "2.0"

setup(
    name="cs.htmlmailer",
    version=version,
    description="A library to send emails with HTML and Text mixed content",
    long_description=open("README.txt").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=["Programming Language :: Python"],
    keywords="",
    author="Mikel Larreategi",
    author_email="mlarreategi@codesyntax.com",
    url="https://github.com/codesyntax/cs.htmlmailer/",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["cs"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
