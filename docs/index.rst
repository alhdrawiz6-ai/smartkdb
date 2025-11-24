SmartKDB Documentation
======================

Welcome to SmartKDB v5 - The Cognitive AI-Native Database Platform!

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   INSTALLATION
   USER_GUIDE

.. toctree::
   :maxdepth: 2
   :caption: Development:

   DEVELOPER_GUIDE
   API_REFERENCE
   ARCHITECTURE

.. toctree::
   :maxdepth: 2
   :caption: Additional Resources:

   CONTRIBUTING
   SECURITY
   CHANGELOG
   PUBLISHING_GUIDE
   PROJECT_STRUCTURE
   INTELLISENSE_UPGRADE

Quick Start
-----------

Install SmartKDB:

.. code-block:: bash

   pip install smartkdb

Basic Usage:

.. code-block:: python

   from smartkdb import SmartKDB

   # Create database
   db = SmartKDB("mydb.kdb")
   
   # Create table
   users = db.create_table("users")
   
   # Insert data
   users.insert({"name": "Alice", "age": 25})

Features
--------

* **ACID Transactions** - Bank-grade reliability
* **Time-Travel Queries** - Access historical data
* **AI Brain** - Automatic query optimization
* **Zero Configuration** - Works instantly
* **Pure Python** - No external dependencies

Links
-----

* PyPI: https://pypi.org/project/smartkdb/
* GitHub: https://github.com/alhdrawiz6-ai/smartkdb
* Issues: https://github.com/alhdrawiz6-ai/smartkdb/issues

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

