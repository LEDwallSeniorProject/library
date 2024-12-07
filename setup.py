from setuptools import find_packages, setup

setup(
    name="calvin-cs-matrix-library",
    packages=['matrix_library'],
    version="0.1.0",
    python_requires=">=3.8,<3.12",
    description="A Python library for use of Computer Science Department at Calvin University's matrix LED display",
    author="Alex Miller, Ellie Sand, Palmer Ford, and Professor Chris Wieringa",
    author_email='cpsc-admin@calvin.edu',
    url='https://github.com/LEDwallSeniorProject/library',
    install_requires=[
        'numpy','matplotlib','pillow','pygame','scikit-image','keyboard'
    ],
    setup_requires=['wheel'],
)
