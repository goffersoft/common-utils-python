from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='rpc',
    version='0.2',
    description='RPC Services',
    long_description=readme(),
    url='http://github/com/common-utils-python/rpc',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=[
        'com',
        'com.goffersoft',
        'com.goffersoft.rabbitmq',
        'com.goffersoft.rabbitmq.rpc',
    ],
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'testfixtures',
    ],
    zip_safe=False)
