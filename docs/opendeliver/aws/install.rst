AMI Installation
============================


To assist with setting up the Open Deliver process, mPowering has created an Amazon Machine Image (AMI) on Amazon Web Services (AWS), which already has the 3 key components set up and configured on one machine:

* ORB
* Moodle
* OppiaMobile server

The specific versions and machine info can be found below.

Pre-requisites
----------------

You will need to have:

* An AWS account, see: https://aws.amazon.com/ - you will need a debit/credit card for the monthly charges for hosting and bandwidth.
* Some experience in using the command line/SSH to log into and configure the server, and experience in server and MySQL database management
* A domain name registered that you can point to your new services. If you don't have this then please ask mPowering about how we can help with providing a sub-domain.

Installation
--------------

#. Log into your AWS account and go to EC2 services
#. From 'Instances' select 'Launch Instance'
#. Select 'Community AMIs' and search for 'OpenDeliver' - you may need to select the zone to be 'US East' for the AMI to appear in the search results.
#. Follow the instructions to create and launch the instance. Remember to keep the server keys safe and secure, you will need these to log into your machine and, if lost, cannot be recovered.

Once the machine is up and running you can log in using SSH.

Post Installation Set-up & Configuration (Required)
------------------------------------------------------

The following must be set up and configured to ensure your machine is accessible and secure.

Update database passwords
~~~~~~~~~~~~~~~~~~~~~~~~~~

All the database passwords are set to 'opendeliver' - all these must be changed to make your server is secure. The following passwords and configurations should be changed (using the MySQL command line):

* MySQL root password - using ``SET PASSWORD FOR 'root'@'localhost' = PASSWORD('<new-password>');``
* ORB database password - using ``SET PASSWORD for 'mpower'@'localhost' = PASSWORD('<new-password>');``
* Moodle database password - using ``SET PASSWORD for 'moodleuser'@'localhost' = PASSWORD('<new-password>');``
* Oppia database password - using ``SET PASSWORD for 'oppiauser'@'localhost' = PASSWORD('<new-password>');``
 
After changing the database passwords remember to run ``flush privileges``.

Now update the site database configurations to use your new passwords:

* ORB - edit ``/home/www/platform/mpower/mpower/settings.py``
* Moodle - edit ``/home/www/moodle/config.php``
* Oppia - edit ``/home/www/oppia/oppia_core/settings.py``


Assign static IP (elastic IP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In AWS you should create an Elastic IP and assign it to your newly created machine. This ensures that when you assign a domain name, the IP address will be static and so not change if the machine is stopped.


Assign domain names
~~~~~~~~~~~~~~~~~~~~

Each component will need it's own sub-domain (or domain) name. Once you have assigned the new elastic/static IP address to your domain & sub-domains, then update the following:

ORB:

* Apache configuration - update ``ServerName`` in ``/etc/apache2/sites-available/health-orb.conf`` and ``/etc/apache2/sites-available/health-orb-ssl.conf``
* Django - update ``ALLOWED_HOSTS`` in ``/home/www/platform/mpower/mpower/settings.py``

Moodle:

* Apache configuration - update ``ServerName`` and ``RedirectPermanent`` in ``/etc/apache2/sites-available/moodle.opendeliver.conf`` and ``ServerName`` in ``/etc/apache2/sites-available/moodle.opendeliver-le-ssl.conf``
* config - update ``$CFG->wwwroot`` in ``/home/www/moodle/config.php``

Oppia:

* Apache configuration - update ``ServerName`` in ``/etc/apache2/sites-available/oppia.conf`` and ``/etc/apache2/sites-available/oppia-ssl.conf``
* Django - update ``ALLOWED_HOSTS`` in ``/home/www/oppia/oppia_core/settings.py``


Install SSL certificates
~~~~~~~~~~~~~~~~~~~~~~~~

All the components are set up to use SSL certificates (i.e. using the secure ``https``). ORB can be accessed either through non-secure http or through secure https, but Moodle and Oppia are set to to be accessed via https only (anyone using http for either of these will be re-directed to the secure version).

The SSL certificates are generated using the free service LetsEncrypt (https://letsencrypt.org/) and will need to be updated to match your (sub-)domain names.

* Run ``sudo letsencrypt --apache certonly``, you'll need to run this 3 times, once for each of the 3 domains
* Edit the apache site configuration files to update the SSL key file paths (the directory paths are also given at the end of running letsencrypt):
  
  * For ORB (``/etc/apache2/sites-available/health-orb-ssl.conf``):
  
    SSLCertificateFile /etc/letsencrypt/live/<insert-ORB-domain-name-here>/fullchain.pem
  
    SSLCertificateKeyFile /etc/letsencrypt/live/<insert-ORB-domain-name-here>/privkey.pem
    
  * For Moodle (``/etc/apache2/sites-available/moodle.opendeliver-le-ssl.conf``):
  
    SSLCertificateFile /etc/letsencrypt/live/<insert-Moodle-domain-name-here>/fullchain.pem
  
    SSLCertificateKeyFile /etc/letsencrypt/live/<insert-Moodle-domain-name-here>/privkey.pem
    
  * For Oppia (``/etc/apache2/sites-available/oppia-ssl.conf``):
  
    SSLCertificateFile /etc/letsencrypt/live/<insert-Oppia-domain-name-here>/fullchain.pem
  
    SSLCertificateKeyFile /etc/letsencrypt/live/<insert-Oppia-domain-name-here>/privkey.pem
	
* Now enable the SSL sites by running:

  * ``sudo a2ensite health-orb-ssl.conf``
  * ``sudo a2ensite moodle.opendeliver-le-ssl.conf``
  * ``sudo a2ensite oppia-ssl.conf``
  
* Finally restart apache with ``sudo service apache2 restart``

You should now have all 3 sites running and available with your domain names and with SSL enabled.

Update component admin passwords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The administrator passwords for each of ORB, Moodle and Oppia should now be updated:

* For ORB, log into the site with username/password 'admin'/'opendeliver', then go the profile page (under 'My ORB' in the menu bar) and update the password
* For Moodle, log into the site with username/password 'admin'/'OpenDeliver1!', then go to the profile page to update the password
* For Oppia, log into the site with username/password 'admin'/'opendeliver', then go the profile page (under 'My Oppia' in the menu bar) and update the password


Post Installation Set-up & Configuration (highly recommended)
---------------------------------------------------------------------


Email configuration
~~~~~~~~~~~~~~~~~~~~

To enable the sending of emails (for example password reset and notification messages), you will need to set up and configure the AWS SES service (https://aws.amazon.com/ses/)

Reserved instance
~~~~~~~~~~~~~~~~~~

Assuming you are planning to have the site running 24x7, then you should look at purchasing a reserved instance from AWS, as this will be much cheaper than on-demand usage.

Cron tasks
~~~~~~~~~~~~~

Several scheduled tasks are set up for ORB, Moodle, Oppia, backing up and auto-renewing the SSL certificates, you check and amend the times and frequency these tasks run by looking at the sudo crontab (``sudo crontab -e``).



Regular Maintenance
----------------------

All systems need regular, ongoing maintenance to keep them up to date and secure. 

Backups
~~~~~~~~

The databases and uploads are backed up regularly (according to the cron schedule), however these backup files are stored on the server (in the directory ``/home/backup``), 
so you should ensure these are regularly copied off-server, for example by using ``rsync`` (https://en.wikipedia.org/wiki/Rsync) to copy the backup files onto another machine/device.

Operating system updates
~~~~~~~~~~~~~~~~~~~~~~~~~

You should regularly (suggested once per month) ensure that the operating system is kept up to date with the latest bug and security fixes. Use ``sudo apt-get update`` then ``sudo apt-get upgrade`` on the command line to check for and install any Ubuntu updates

Updates from core code repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AWS AMI is a point-in-time snapshot of the core code for ORB, Moodle and OppiaMobile, so you should ensure that the code for each of these is kept up to date.



