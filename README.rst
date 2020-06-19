=======================
core_linked_records_app
=======================

This Django reusable app contains the PID functionalities for a
CDCS project.

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

Add the ``"core_linked_records_app"`` under ``INSTALLED_APPS`` as
such:

.. code:: python

    INSTALLED_APPS = [
      ...
      "core_linked_records_app",
    ]

Add the necessary keys at the end of the file.

.. code:: python

    ID_PROVIDER_SYSTEMS = {
        "local": {
            "class": "core_linked_records_app.utils.providers.local.LocalIdProvider",
            "args": [SERVER_URI],
        },
        "handle.net": {  # Optional: if a Handle.net server is available.
            "class": "core_linked_records_app.utils.providers.handle_net.HandleNetSystem",
            "args": [
                "https://handle-net.domain/api/handles",
                SERVER_URI,
                "300%3ACDCS/ADMIN",
                "admin",
            ],
        },
    }

Edit the urls.py file
---------------------

Add the ``core_linked_records_app`` urls to the Django project as such.

.. code:: python

    url(r'^pid/', include("core_linked_records_app.urls")),

Tests
=====

To play the test suite created for this package, download the git repository
and run:

.. code:: bash

  $ python runtests.py


