from setuptools import setup, find_packages

setup(
    name="bitcoin_python",
    version="0.1",
    description="Python library for Bitcoin node",
    author="Sosthène",
    license="MIT",
    include_package_data=True,
    packages=find_packages(exclude=["test"]),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
