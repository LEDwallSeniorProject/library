from setuptools import find_packages, setup

setup(
    name="calvin-cs-matrix-library",
    packages=['matrix_library'],
    version="1.0.0",
    python_requires=">=3.8,<3.12",
    description="A Python library for use of Computer Science Department at Calvin University's matrix LED display",
    author="Alex Miller, Ellie Sand, Palmer Ford, Eli Lewis, Yigit Turan, and Professor Chris Wieringa",
    author_email='cpsc-admin@calvin.edu',
    url='https://github.com/LEDwallSeniorProject/library',
    install_requires=[
        'numpy','matplotlib','pillow','pygame','scikit-image','pynput','requests'
    ],
    setup_requires=['wheel'],
)
