from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='cucumber_reports',
    version='0.0.1',
    keywords='cucumber testing framework python-testing test driven development',
    description='Reporting and statistics tool for output of cucumber framework',
    long_description=long_description,
    author='Vaclav Stengl',
    author_email='stengvac@fit.cvut.cz',
    # license='??', todo pick some
    url='https://github.com/stengvac/cucumber-sem',
    packages=find_packages(),
    package_data={
        'cucumber_reports': [
            'static/cucumber_reports/*',
            'templates/reports/*.html',
            'templates/statistics/*.html',
            'templates/errors/*.html'
        ]
    },
    install_requires=[
        'django',
        'numpy',
        'pandas',
        'django-pandas',
        'django-bootstrap3',
        'matplotlib',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-django'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
    ],
)