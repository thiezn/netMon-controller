netMon-controller: Distributed Network Monitoring
=================================================

|Build Status| |Coverage Status| |Documentation Status|

Detailed documentation at
`netmon-controller.readthedocs.org <https://netmon-controller.readthedocs.org/>`__

netMon is a distributed network monitoring solution written in python.

The netMon controller is a web interface for the netMon-pollers running in the network.
It brings back all the poller data into a single view for configuration and analytics.

Installation
------------

.. code:: bash

    git clone https://github.com/thiezn/netMon-controller.git
    cd netMon-controller
    python3 setup.py install

Quickstart
----------

./run_controller

External Dependencies
---------------------

-  flask
-  wtforms

Testing
-------

- Tested against Ubuntu 14.04 LTS using `travis-ci <https://travis-ci.org/>`__
- Test coverage reporting through `coveralls.io <https://coveralls.io/>`__
- Tested against the following Python versions:
    * 3.5
    * 3.5-dev 
    * nightly

.. |Build Status| image:: https://travis-ci.org/thiezn/netMon-controller.svg?branch=master
   :target: https://travis-ci.org/thiezn/netMon-controller
.. |Coverage Status| image:: https://coveralls.io/repos/github/thiezn/netMon-controller/badge.svg?branch=master
   :target: https://coveralls.io/github/thiezn/netMon-controller?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/netMon/badge/?version=latest
   :target: http://netmon.readthedocs.io/en/latest/?badge=latest
