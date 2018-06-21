import os
import sys

from setuptools import find_packages
from setuptools import setup


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
        README = readme.read()
except Exception:
    README = '<failed to open README.md>'


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


install_dependencies = (
    'Django>=1.8' + (',<1.11.99' if sys.version_info[0] < 3 else ''),
)

test_dependencies = (
    'mock',
    'djangorestframework',
)


setup(
    name='django-lookup-tables',
    version='0.13.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Combine all lookup tables into a single unified system.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='jeffrey k eliasen',
    author_email='jeff+django-lookup-tables@jke.net',
    url='https://github.com/seawolf42/django-lookup-tables',
    zip_safe=False,
    keywords='django-lookup-tables',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=install_dependencies,
    tests_require=install_dependencies + test_dependencies,
    test_suite='runtests.run_tests',
)
