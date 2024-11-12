from setuptools import find_packages, setup

setup(
    name="calvin-cs-matrix-library",
    packages=['matrix_library'],
    ]),
    version="0.1.0",
    python_requires=">=3.9",
    description="A Python library for use of Computer Science Department at Calvin University's matrix LED display",
    author="Alex Miller, Ellie Sand, Palmer Ford, and Professor Chris Wieringa",
    author_email='cpsc-admin@calvin.edu',
    url='https://github.com/LEDwallSeniorProject/library',
    install_requires=[
        'numpy','matplotlib','PIL','pygame','scikit-image'
    ]
)
