

import setuptools

setuptools.setup(
    name='pandazip',
    version='0.0.2',
    description='Cut memory footprint by half in just 2 lines of code. Compress Pandas DataFrame without losing information.',
    url='https://github.com/meetyildiz/pandazip',
    author='MEHMET YILDIZ',
    author_email='myildiz.ie@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['pandas',
                      'numpy',
                      'joblib',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)