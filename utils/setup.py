from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='utils',
    version='0.3',
    description='Logging Configuration',
    long_description=readme(),
    url='http://github/com/common-utils-python/utils',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=[
        'com',
        'com.goffersoft',
        'com.goffersoft.logging',
        'com.goffersoft.sip',
        'com.goffersoft.http',
    ],
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'testfixtures',
    ],
    zip_safe=False)
