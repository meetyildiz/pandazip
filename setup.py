from setuptools import setup

setup(
    name='pandazip',
    version='0.0.0',
    description='Cut memory footprint by half in just three lines of code. '
                'Compress Pandas DataFrame without losing information.',
    url='https://github.com/meetyildiz/pandazip',
    author='MEHMET YILDIZ',
    author_email='myildiz.ie@gmail.com',
    license='BSD 3-clause',
    packages=[],
    install_requires=['pandas',
                      'numpy',
                      'joblib',
                      ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-clause",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)