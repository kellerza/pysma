=============
pysma library
=============
.. image:: https://circleci.com/gh/kellerza/pysma.svg?style=svg
    :target: https://circleci.com/gh/kellerza/pysma
.. image:: https://codecov.io/gh/kellerza/pysma/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/kellerza/pysma
  
SMA Webconnect library for Python 3. The library was originally crated to intrgrate SMA with HomeAssistant

See http://www.sma-solar.com for more information on the SMA solar inverters

Currently tested on Sunnyboy 1.5 and various other Webconnect models, If you can access your SMA via your browser, this might work for you.

Other SMA interfaces include https://sbfspot.codeplex.com/ and a Python
`adaptation <https://github.com/TD22057/T-Home/>`_

=============
Example usage
=============

See `example.py <./example.py>`_ for a basic usage and tests

==============
Home Assistant
==============

.. role:: yaml(code)
   :language: yaml
   
The Home Assistant sma sensor documentation can be found `here <https://www.home-assistant.io/components/sma>`_

By default ssl is disabled (Sunnyboy 1.5 WebConnect uses :code:`http://`). If you access your SMA WebConnect via :code:`https://` you should set both :yaml:`ssl: true` and :yaml:`verify_ssl: false`. 

Daily usage is not always available from the SMA WebConnect interface. It is possible to get around this by using a `utility meter <https://www.home-assistant.io/components/utility_meter>`_
