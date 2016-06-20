from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/neddy/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.rst') as f:
        return f.read()


setup(name="neddy",
      version=__version__,
      description="CL-util to query the NASA/IPAC Extragalactic Database (NED)",
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords=['tools, NED'],
      url='https://github.com/thespacedoctor/neddy',
      download_url='https://github.com/thespacedoctor/neddy/archive/v%(__version__)s.zip' % locals(
      ),
      author='David Young',
      author_email='davidrobertyoung@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pyyaml',
          'neddy',
          'fundamentals',
          'astrocalc'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['neddy=neddy.cl_utils:main'],
      },
      zip_safe=False)
