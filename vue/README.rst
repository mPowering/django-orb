===========================
ORB Front-end Applications
===========================

Development
===========

For initial development set up, run `make vue-deps` in your root folder. This will install all dependencies.

ORB front-end applications and compiled and bundled through ParcelJS. Build configuration is contained within
`vue/orb.yaml`.

For running the development environment, first run `docker` and follow the general steps for running
the Django instance. Then in a new terminal window, run `make vue-dev`. This will compile our application
code and use Hot Module Reloading (HMR) for ease of development.

Production
==========

From your root folder, run `make vue-build`. This will compile our application code for production and minify
the Javascript and CSS for efficient transfer.

CourseBuilder
=============

Single Page Application (SPA)
-----------------------------

On landing on a course page, the application will convert server-based template data into a usable single
page application. This enables the user to navigate within the CourseBuilder app for all views (list/new/detail)
efficiently without needing to return to the server for repeated and redundant code/views. Additionally, this
keeps app state current for the user.

On initial load, and subsequent hard reloads, the application will load in data that is embedded into the
server template to hydrate state. The user will not need to revisit the server for templates for their
current CourseBuilder use.

* If the user initially visits a course detail page, the page will recognize that the user has
not visited the course list page and will request a one-time hard reload to get pertinent course data for all
courses the user is able to access.*


3rd Party Javascript
--------------------

CourseBuilder requires:

Third-party platform scripts are mounted through `vendor/bundle.js`. The build scripts
take care of using the minified scripts for production and development versions are used
during the development process.

- VueJS: our JavaScript app development platform
- Vuex/Vuex-ORM: state and data model control for normalizing data between server and front-end code.
- VueRouter: routing control to better user experience and pass data between front-end application views



Internationalization
--------------------

All user interface items that are non-user editable are based on an internationalization document. Most
texts are currently set up for English, but will be run through Django's translation functions.
Internationalization texts/translations are set up in 'orb/templates/orb/course/script_initializatons.html`.
