REST API
=====================================


The REST API is still under development.

There is an example of the search API running at: http://alexlittle.net/mpowering/examples/search.php

Current versions of the API helper libraries can be found at:

* for PHP: https://github.com/mPowering/mpowering-api-php
* for Python: https://github.com/mPowering/mpowering-api-python

These helper libraries also include some examples of how to use the API.

Accessing the API
------------------

.. note::
	Currently, for any REST API method requests, you will need to contact us so we can enable your account for these API methods.

To make any request to the API, you must supply your username and API Key (your API key can be found on your ORB profile page).

Resource
----------

For getting the information about a resource, submitting a new resource or updating an existing resource

Endpoint: /api/v1/resource/

Allowed methods:

* GET
* POST
* PUT

Required params (POST and PUT):

* `title`
* `description`


Search
------

For searching the ORB database

Endpoint: /api/v1/resource/search/

Allowed methods:

* GET

Required params:

* `q` - the query search term

Resource Tag
------------

Endpoint: /api/v1/resourcetag/

Allowed methods:

* GET
* POST
* PUT


Resource Tag
------------

Endpoint: /api/v1/resourcetag/

Allowed methods:

* GET
* POST
* DELETE


Resource File
--------------

Endpoint: /api/v1/resourcefile/

Allowed methods:

* GET
* DELETE

Resource URL
--------------

Endpoint: /api/v1/resourceurl/

Allowed methods:

* GET
* DELETE

Resource Image Upload
----------------------

Endpoint: /api/upload/image/

Allowed methods:

* POST


Resource File Upload
---------------------

Endpoint: /api/upload/file/

Allowed methods:

* POST

Tag
--------------

Endpoint: /api/v1/tag/

Allowed methods:

* GET
* POST

Tags
--------------

Endpoint: /api/v1/tags/

Allowed methods:

* GET

Tags Resource
--------------

Endpoint: /api/v1/tagsresource/

Allowed methods:

* GET

