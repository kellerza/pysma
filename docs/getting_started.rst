Getting Started
===============


Install
*******
PySMA is available on `pypi`_ and can be installed using pip.

.. code-block:: console
   
   pip install pysma

.. _pypi: https://pypi.org/project/pysma/


Create SMA instance
*******************

The :class:`~pysma.SMA` class requires a `ClientSession`_ object, an URL and a password.
The default user group is "user", but can be changed by passing it as the fourth ``group`` parameter.

.. code-block:: python3

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    url = "https://device-hostname"
    password = "MyPassword!"
    
    sma = pysma.SMA(session, url, password)

.. _ClientSession: https://docs.aiohttp.org/en/stable/client_reference.html

Create Sensors
**************

To retrieve values from the device you need a :class:`~pysma.sensor.Sensors` object. The easiest way is to generate one using the :meth:`~pysma.SMA.get_sensors` method. This will query the device to figure out the device class and returns a :class:`~pysma.sensor.Sensors` object containing specific :class:`~pysma.sensor.Sensor` objects for your device.


.. code-block:: python3

    sma_sensors = sma.get_sensors()

Alternatively this can be manually created by initializing an empty :class:`~pysma.sensor.Sensors` object and adding new :class:`~pysma.sensor.Sensor` objects to it using the :meth:`~pysma.sensor.Sensors.add` method.
Predefined sensors can be found in :mod:`pysma.definitions`. See also `definitions.py at Github`_.

.. code-block:: python3

    sma_sensors = Sensors()
    my_sensor = Sensor("6300_12345678_0", "dummy_sensor") # This key won't work!
    sma_sensors.add(my_sensor)
    sma_sensors.add(pysma.definitions.pv_power_a)

.. _definitions.py at Github: https://github.com/kellerza/pysma/blob/master/pysma/definitions.py

Read Sensor values
******************

Now you have a :class:`~pysma.sensor.Sensors` object, you can pass this to :meth:`~pysma.SMA.read` to read the values from the device. The retrieved values are stored in the respective :class:`~pysma.sensor.Sensor`.

.. code-block:: python3

    sma.read(sma_sensors)

    for sma_sensor in sma_sensors:
        print(f"{sma_sensor.name}: {sma_sensor.value}")


Complete Example
****************

A full example can be found in the `Github repository`_

.. _Github repository: https://github.com/kellerza/pysma/blob/master/example.py
