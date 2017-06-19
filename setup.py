from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-state-machines',
    version='0.1.2',
    description='Django finite state machine implementation',
    author='Karol Sztajerwald',
    author_email='sztajerwaldkarol@gmail.com',
    url='https://github.com/Backscratcher/django-state-machines',
    keywords="django",
    packages=['django_state_machines', ],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
