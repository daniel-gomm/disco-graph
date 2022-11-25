from setuptools import find_packages, setup

setup(
    name='graph-connector',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        #TODO: Add missing dependencies
    ],
)
