Virus Checking
=====================================

Since the ORB platform allows users to upload files, these files should be 
checked for viruses.

Even if an uploaded file contains a virus that may not harm the server operating 
system, users who download the files may be using operating systems which are 
susceptible to the virus.

The ORB server uses the `ClamAV <http://www.clamav.net/>`_ open source antivirus
engine to scan uploaded files.

A sample shell script to run the virus checker and email the results is included 
in the ``utils`` directory (``virus-scan.sh``)

