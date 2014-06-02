from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='projtemplate',
    version='0.1',
    description='Python Directory Structure Template',
    long_description=readme(),
    url='http://github/com/common-utils-python/projtemplate',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=['projtemplate'],
    install_requires=[
        'uuid',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
    zip_safe=False)
