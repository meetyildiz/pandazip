import setuptools
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name='pandazip',
    version='0.0.10',
    description='Cut memory footprint by half in just 2 lines of code.',
    long_description_content_type='text/markdown',
    long_description=read('README.md'),
    url='https://github.com/meetyildiz/pandazip',
    author='MEHMET YILDIZ',
    author_email='myildiz.ie@gmail.com',
    packages=["pandazip"],

    install_requires=['pandas',
                      'joblib'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
