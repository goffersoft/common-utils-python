from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='msg',
    version='0.1',
    description='Generic Message Module',
    long_description=readme(),
    url='http://git.ccp.cable.comcast.com/peaswar_utils/python_utils',
    author='peaswa001c',
    author_email='prakash_easwar@cable.comcast.com',
    license='MIT',
    packages=[
        'msg',
    ],
    install_requires=[
        'utils',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'testfixtures',
    ],
    zip_safe=False)
