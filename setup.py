from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/neddy/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


install_requires = [
    'pyyaml',
    'fundamentals',
    'astrocalc',
    'eventlet',
    'numpy',
    'unicodecsv'
]

# READ THE DOCS SERVERS
exists = os.path.exists("/home/docs/")
if exists:
    install_requires = ['fundamentals']

setup(name="neddy",
      version=__version__,
      description="Query the Nasa Extra-Galactic (NED) database via the command-line and programmatically",
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.9',
          'Topic :: Utilities',
      ],
      keywords=['ned, query, astronomy, conesearch'],
      url='https://github.com/thespacedoctor/neddy',
      download_url='https://github.com/thespacedoctor/neddy/archive/v%(__version__)s.zip' % locals(
      ),
      author='David Young',
      author_email='davidrobertyoung@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*tests*"]),
      include_package_data=True,
      install_requires=install_requires,
      test_suite='nose2.collector.collector',
      tests_require=['nose2', 'cov-core'],
      entry_points={
          'console_scripts': ['neddy=neddy.cl_utils:main'],
      },
      zip_safe=False)
