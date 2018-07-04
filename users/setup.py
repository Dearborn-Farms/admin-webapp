"""Install arXiv auth package."""

from setuptools import setup, find_packages

setup(
    name='arxiv-users',
    version='0.1.1',
    packages=[f'arxiv.{package}' for package
              in find_packages('./arxiv', exclude=['*test*'])],
    install_requires=[
        "pycountry",
        "sqlalchemy",
        "mysqlclient",
        "python-dateutil",
        "arxiv-base",
        "jwt"
    ],
    zip_safe=False
)
