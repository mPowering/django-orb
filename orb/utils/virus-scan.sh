#!/bin/bash

TO='to@me.com'
FROM='from@me.com'

sudo freshclam

RESULTS=`sudo clamscan -r /full/path/to/media/dir/`

/usr/sbin/sendmail -f $FROM $TO <<EOF
subject:[ORB] Virus scan results
from:$FROM
$RESULTS
EOF