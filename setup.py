import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-orb',
    version='2.8.1',
    packages=[
        'orb',
        'orb.analytics',
        'orb.api',
        'orb.migrations',
        'orb.fixtures',
        'orb.utils',
        'orb.profiles',
    ],
    include_package_data=True,
    license='GNU GPL v3 License',
    description='',
    long_description=README,
    url='http://oppia-mobile.org/',
    author='Alex Little, Digital Campus',
    author_email='alex@digital-campus.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "Django==1.11.15",
        "django-tastypie>=0.11.0,<1.13.0",
        "django-tablib>=0.9.11,<4.0",
        "django-crispy-forms>=1.4.0,<2.0",
        "django-tinymce>=1.5.0,<2.0",
        "django-wysiwyg>=0.7.0,<1.0",
        "django-haystack>=2.3.0,<2.4.0",
        "pysolr>=3.3.0,<3.4.0",
        "Pillow>=2.7.0,<3.0.0",
        "sorl-thumbnail>=12.0,<13.0",
        "textract>=1.2.0,<1.3.0",
        "pytz>=2014,<2015",
    ],
)
