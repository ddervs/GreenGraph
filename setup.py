from setuptools import setup, find_packages

setup(
    name="GreenGraph",
    version="0.1",
    packages=find_packages(exclude=['*tests']),
    scripts=['scripts/greengraph'],
    install_requires=['argparse', 'geopy', 'numpy', 'requests', 'matplotlib', 'mock']
)
