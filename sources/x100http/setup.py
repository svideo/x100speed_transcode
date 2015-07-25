from setuptools import setup

setup(
    name='x100http',
    version='0.1.9',

    description='WebFramework support customing file upload processing',
    long_description=open('README.rst').read(),
    url='https://github.com/chengang/x100http',
    author='Chen Gang',
    author_email='yikuyiku.com@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='http webframework file upload rfc1867 x100',

    py_modules=['x100http'],
    #test_suite='tests',
)