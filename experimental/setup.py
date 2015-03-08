from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='experimental',
    version='0.4',
    description='Logging Configuration',
    long_description=readme(),
    url='http://github/com/common-utils-python/experimental',
    author='goffer',
    author_email='goffersoft@gmail.com',
    license='MIT',
    packages=[
        'com',
        'com.goffersoft',
        'com.goffersoft.logging',
        'com.goffersoft.sip',
        'com.goffersoft.http',
        'com.goffersoft.utils',
        'com.goffersoft.msg',
        'com.goffersoft.raw',
        'com.goffersoft.rabbitmq',
        'com.goffersoft.rabbitmq.rpc',
        'com.goffersoft.zeromq',
        'com.goffersoft.zeromq.servicetracker',
    ],
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'testfixtures',
    ],
    zip_safe=False)
