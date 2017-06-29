#!/bin/bash

# On the first run, we need to copy the selected configurition files.
if [ ! -f /opt/solr/example/solr/collection1/conf/.installed ]; then
	# Check, if partial search function should be enabled on text fields.
	if [ "${PARTIAL_SEARCH_ENABLED}" == "false" ]; then
		cp /srv/solr/schemas/default/* /opt/solr/example/solr/collection1/conf
	else
		cp /srv/solr/schemas/partial_search/* /opt/solr/example/solr/collection1/conf
	fi
	touch /opt/solr/example/solr/collection1/conf/.installed
fi

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
