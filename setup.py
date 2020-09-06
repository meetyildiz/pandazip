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
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)