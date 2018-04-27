===================================
ORB Peer Network - :mod:`orb.peers`
===================================

.. index:: peers
.. module:: orb.peers
:synopsis: Shared data across a network of peers


The ORB API provides a way for data on an ORB site to be accessed programmatically.
This allows for other one ORB instance to download resources from another, syncing
resources across a network of ORB peers.

The starting requirement is API access to the target ORB (e.g. the global mPowering ORB).

Setting up peers
================

A peer is added to your ORB instance by adding three data items:

- host name
- user name
- API key

This can be done from the Django admin or using a management command, `add_peer`.

The management command is especially helpful for automating setup of an ORB instance.

Note that the API key is stored and read in plaintext.

Syncing data
============

To sync data from a configured ORB peer, use the `sync_peer_resources` management
command. This can be used without arguments or the numeric primary keys of configured
peers can be provided to sync only from select peers.

The primary keys can be discovered via the Django admin or by using the management
command `list_peers`.

How syncing works
=================

The core action of the peer data sync is to copy or update resources from the remote
ORB to the local ORB.

Global IDs
----------

Every resource has a globally unique identifier which is copied with synced resources.
This ensures that a resource can be downloaded from one ORB and from yet another and
still retain a non-overridable ID that tracks it across instances. This GUID is used to
identify resources for update.

Pending by default
------------------

Resources on the remote ORB that are not present on the local ORB are copied to new
resources in the local ORB and placed in the pending state. These must be reviewed
by a content administrator prior to becoming public on the local ORB.

Updates
-------

Updates to a remote resource will overwrite any local changes.

Languages
---------

ORB instances may have resources available with multiple language translations.
Only data for languages explicitly supported on the local ORB instance will be
synced. Other languages will be ignored.


Module overview
===============

.. automodule:: peers.management
    :members:
