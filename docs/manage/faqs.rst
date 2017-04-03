ORB Knowledge Management Tasks
===============================

All of the management tasks below are done from the ORB admin pages (https://health-orb.org/admin/) 
and you will need to be an admin user to be able to access these pages, or perform any of the tasks 
listed below.
   

.. _faqNewDomain:

Add a new health domain
--------------------------

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

.. _faqContentReviewer:

Add a new content reviewer
-----------------------------

* Go to the ORB admin pages
* Under the ORB section select 'User profiles'
* Search or browse for the user and click to edit their details
* Under the reviewer roles, select the role(s) to give this user
* Click 'save'


.. _faqUpdateTag:

Update the info/image for a tag
-----------------------------------

* Go to the ORB admin pages
* Under the ORB section select 'Tags'
* Browse or search for the tag to update and click to edit it
* You can upload a new image or change the information for the tag
* For the image files, ORB will automatically resize and crop (if necessary) any images files for display on the site
* Click 'save'


.. _faqSearchUser:

Search for a user
------------------

* Go to the ORB admin pages
* Under the Authentication and Authorization section select 'Users'
* You can search based on name, username or email address

.. _faqUpdateUser:

Update a users information/change password
-------------------------------------------

* Find the user you'd like to update (:ref:`faqSearchUser`)
* Click to edit their details
* From here you can update their information and change their password
* Click save when finished


.. _faqRemoveUser:

Remove/Hide a resource
------------------------

Usually it will be best to just hide a resource, rather than delete it, since deleting it will remove all of the statistics and other information that is associated with a resource.

* Go to the ORB admin pages
* Under the ORB section select 'Resources'
* Search or browse for the resource and click to edit the details
* Change the status to either 'pending', 'rejected' or 'archived' ('archived' option coming soon)
* Click save

To completely delete the resource, from the edit page, there is an option to delete the resource.


.. _faqUpdateToolkit:

Add or update a toolkit
------------------------

.. note::
   Currently the toolkits are hard coded, but they will move to being stored in the database soon - these instructions 
   relate to how it will work when they are managed in the database.
 
* Go to the ORB admin pages
* Under the ORB section select 'Toolkits' 
* Search or browse for the toolkit and click to edit the details

   
.. _faqManageTranslations:

Manage translations
--------------------

The documentation for managing the internationalisation and translations is described in the :ref:`translation-index` section.


 
.. _faqUpdateOrganisation:

Update logo and information for an organisation
------------------------------------------------

All organisations are stored as 'tags'


.. _faqUpdateIcon: 

Update the icon for geography or language
-------------------------------------------


.. _faqOrganisationAnalytics: 

Give access to organisation analytics
----------------------------------------


.. _faqAddUpdateCollection:

Create/Update a collection of resources
----------------------------------------
