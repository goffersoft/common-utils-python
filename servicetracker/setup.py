from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='servicetracker',
    version='0.1',
    description='Service Tracker',
    long_description=readme(),
    url='http://github/com/common-utils-python/servicetracker',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=[
        'com',
        'com.goffersoft',
        'com.goffersoft.servicetracker',
    ],
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
    zip_safe=False)
