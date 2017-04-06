ORB Knowledge Management Tasks
===============================

All of the management tasks below are done from the ORB admin pages (https://health-orb.org/admin/) 
and you will need to be an admin user to be able to access these pages, or perform any of the tasks 
listed below.
  
  
  
User/Permissions Management
----------------------------

.. _faqSearchUser:

Search for a user
~~~~~~~~~~~~~~~~~~~

* Go to the ORB admin pages
* Under the Authentication and Authorization section select 'Users'
* You can search based on name, username or email address

.. _faqUpdateUser:

Update a users information/change password
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Find the user you'd like to update (:ref:`faqSearchUser`)
* Click to edit their details
* From here you can update their information and change their password
* Click save when finished


.. _faqContentReviewer:

Add a new content reviewer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The new reviewer should register on ORB first and let us have their username so we can then assign them permissions.

* Go to the ORB admin pages
* Under the ORB section select 'User profiles'
* Search or browse for the user and click to edit their details
* Under the reviewer roles, select the role(s) to give this user
* Click 'save'

.. _faqOrganisationAnalytics: 

Give access to organisation analytics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users can be given permissions to view the analytics for all the resources published under their organisations.

* Go to the ORB admin pages
* Under the ORB section select 'Tag Owners'
* Click on 'Add tag owner' and select the user and tag to give permissions to, then save

Usually we'd give users access to tags that are organisations, although you could assign users to any tag.


.. _faqContentReviewers:

View Content Reviewers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to find out who is currently listed as being a content reviewer, and for which roles:

* Go to the ORB admin pages
* Under the ORB section select 'User profiles'
* From the filtering menu on the right hand side, you can filter the users by the reviewer roles 




Health Domain Management
-------------------------


.. _faqNewDomain:

Add a new health domain
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Go to the ORB admin pages
* Under the ORB section select 'Tags'
* Select 'Add Tag' button (top right of screen)
* For the category, select 'health domain'
* Add the name of the new name in both the 'name' and 'name [en]' fields
* Select your user id as both the create and update user
* Update the 'order by' field to reflect where in the list of health domains you would like the new 
  one to appear - if you are placing it between existing domains, you should also update the order by 
  for the existing domains to ensure consistency in display.
* Untick the 'published' checkbox if you would like to add some resources to the domain before it 
  appears on the homepage. Once you are ready to publish the domain, just tick this box.
* Click 'save'


Resource/Toolkit Management
----------------------------

.. _faqRemoveResource:

Remove/Hide a resource
~~~~~~~~~~~~~~~~~~~~~~~~~

Usually it will be best to just hide a resource, rather than delete it, since deleting it will remove all of the statistics and other information that is associated with a resource.

* Go to the ORB admin pages
* Under the ORB section select 'Resources'
* Search or browse for the resource and click to edit the details
* Change the status to either 'pending', 'rejected' or 'archived' ('archived' option coming soon)
* Click save

To completely delete the resource, from the edit page, there is an option to delete the resource.

.. _faqAddUpdateCollection:

Create/Update a collection of resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collections may be resources that are part of a particular curriculum (eg OpenWASH).

* Go to the ORB admin pages
* Under the ORB section select 'Collections'
* Either click to edit an existing collection, or click to 'Add Collection'
* Enter a title and description and then save

Now to add/edit the resources in the collection:

* Go to the ORB admin pages
* Under the ORB section select 'Collection resources'
* Click on 'Add Collection resource'
* Select the resource and the collection to add it to, optionally add an 'order by' number
* Click save, repeat for each resource to add to the collection

.. _faqUpdateToolkit:

Add or update a toolkit
~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   Currently the toolkits are hard coded, but they will move to being stored in the database soon - these instructions 
   relate to how it will work when they are managed in the database.
 
* Go to the ORB admin pages
* Under the ORB section select 'Toolkits' 
* Search or browse for the toolkit and click to edit the details


.. _faqManageTranslations:

Manage translations
~~~~~~~~~~~~~~~~~~~~

The documentation for managing the internationalisation and translations is described in the :ref:`translation-index` section.



Tag Management (incl. Languages & Geographies)
-----------------------------------------------

.. _faqUpdateTag:

Update the info/image for a tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Go to the ORB admin pages
* Under the ORB section select 'Tags'
* Browse or search for the tag to update and click to edit it
* You can upload a new image or change the information for the tag
* For the image files, ORB will automatically resize and crop (if necessary) any images files for display on the site
* Click 'save'


.. _faqUpdateOrganisation:

Update logo and information for an organisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All organisations are stored as 'tags', see :ref:`faqUpdateTag`


.. _faqUpdateGeoLangIcon: 

Update the icon for geography or language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All geographies and languages are stored as 'tags', see :ref:`faqUpdateTag`


