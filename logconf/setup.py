from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='loginit',
    version='0.1',
    description='Logging Initialization',
    long_description=readme(),
    url='http://github/com/common-utils-python/loginit',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=['loginit'],
    install_requires=[
        'uuid',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'testfixtures',
    ],
    zip_safe=False)
