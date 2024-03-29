=======================
core_linked_records_app
=======================

This Django reusable app contains the PID functionalities for a CDCS project.

Pre-requisites
==============

For automated and manual install, the following software are needed:

* ``python``
* ``pip``
* virtual env (``conda`` or ``venv``)

In addition, for manual setup, ``git`` is needed.

Installation
============

Automated installation
----------------------

.. code:: bash

  $ pip install core_linked_records_app

Manual installation
-------------------

.. code:: bash

    $ git clone https://github.com/usnistgov/core_linked_records_app.git
    $ cd core_linked_records_app
    $ python setup.py
    $ pip install sdist/*.tar.gz

Configuration
=============

Edit the setting.py file
------------------------

Add the ``"core_linked_records_app"`` under ``INSTALLED_APPS`` as such:

.. code:: python

    INSTALLED_APPS = [
      ...
      "core_linked_records_app",
    ]

Add the necessary setting keys at the end of the file.

.. code:: python

    ID_PROVIDER_SYSTEM_NAME = "local",
    """ str: internal name of the provider system.
    """

    ID_PROVIDER_SYSTEM_CONFIG = {
        "class": "core_linked_records_app.utils.providers.local.LocalIdProvider",
        "args": [],
    }
    """ dict: provider system configuration for resolving PIDs.
    """

    ID_PROVIDER_PREFIXES = ["cdcs"]
    """ list<str>: accepted prefixes if manually specifying PIDs (first item is the
    default prefix).
    """

    ID_PROVIDER_PREFIX_DEFAULT = ID_PROVIDER_PREFIXES[0]
    """ str: default prefix for records (optional).
    """

    ID_PROVIDER_PREFIX_BLOB = ID_PROVIDER_PREFIXES[0]
    """ str: default prefix for blobs (optional).
    """

    PID_XPATH = "root.pid"
    """ string: location of the PID in the document, specified as dot notation.
    """

When using handle.net, the ``ID_PROVIDER_SYSTEM_CONFIG`` key has to be changed and
additional optional settings keys are available.

.. code:: python

    ID_PROVIDER_SYSTEM_NAME = "handle.net"
    """ str: internal name of the provider system.
    """

    ID_PROVIDER_SYSTEM_CONFIG = {
        "class": "core_linked_records_app.utils.providers.handle_net.HandleNetSystem",
        "args": [
            "https://hdl.handle.net",  # Lookup domain, displayed on the records.
            "https://handle-net.domain",  # Regsitration domain, for CRUD operations.
            "300%3ACDCS/ADMIN",
            "admin",
        ],
    }
    """ dict: provider system configuration for resolving PIDs.
    """

    HANDLE_NET_RECORD_INDEX = 1
    """ int: index of record when using handle.net.
    """

    HANDLE_NET_ADMIN_DATA = {
        "index": 100,
        "type": "HS_ADMIN",
        "data": {
            "format": "admin",
            "value": {
                "handle": f"0.NA/{ID_PROVIDER_PREFIX_DEFAULT}",
                "index": 200,
                "permissions": "011111110011",
            },
        },
    }
    """ dict: datastructure to insert with the record in order to give the
    handle.net user creation, edition and deletion rights.
    """

Edit the urls.py file
---------------------

Add the ``core_linked_records_app`` urls to the Django project as such.

.. code:: python

    re_path(r'^pid/', include("core_linked_records_app.urls")),


Example configuration and XML file:
-----------------------------------

The example below shows a configuration of a CDCS instance using the
core_linked_records_app settings and what an XML document with a PID would look
like in this case:

1. Edit `settings.py`:

.. code:: python

    SERVER_URI = "http://localhost:8000"
    ID_PROVIDER_SYSTEM_NAME = "local"
    ID_PROVIDER_SYSTEM_CONFIG = {
        "class": "core_linked_records_app.utils.providers.local.LocalIdProvider",
        "args": [],
    }
    ID_PROVIDER_PREFIXES = ["cdcs"]
    PID_XPATH = "root.pid"


2. Upload the XML file:

.. code:: XML

    <root><pid>http://localhost:8000/pid/rest/local/cdcs/0123ABCD</pid></root>


3. Explanation:

The pid is stored in the "pid" element under the "root" element like indicated
in PID_XPATH (root.pid). The generated PID
(http://localhost:8000/pid/rest/local/cdcs/0123ABCD) is composed of:

- the SERVER_URI: http://localhost:8000
- the route to core_linked_records_app as defined in urls.py: pid
- the route to the rest endpoints of this app: rest
- the name of the PID provider specified by ID_PROVIDER_SYSTEM_NAME: local
- a prefix found in the ID_PROVIDER_PREFIXES list: cdcs
- a unique random identifier generated by the local PID provider: 0123ABCD

Tests
=====

To play the test suite created for this package, download the git repository
and run:

.. code:: bash

  $ python runtests.py


