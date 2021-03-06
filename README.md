TrueSight Pulse Meter Plugin SDK for Python
===========================================

This provides a framework for the development of the TrueSight Pulse Meter Plugins

[![Build Status](https://travis-ci.org/boundary/meter-plugin-sdk-python.svg?branch=develop)](https://travis-ci.org/boundary/meter-plugin-sdk-python)


Measurement Transports
----------------------

The SDK supports sending measurements to Pulse via 3 different methods:

- Standard Out
- Meter RPC (Future)
- Measurement API (Future)

### Standard Out

Plugin writes to standard out which is read by the Plugin Manager
which then forwards to the meter via Meter RPC API, which then sends to
Pulse.
                                                                     
### Meter RPC

Plugin writes to Meter RPC channel which then sends to Pulse.

### Measurement API

Plugin writes to Pulse Measurement REST API directly sending to Pulse

Data Collectors
---------------

The framework supports the following data collectors, custom data
collectors can be created by extending the default data collector

- Database
- Exec
- HTTP/HTTPS
- Logfile
- TCP/UDP Socket

Example Plugins
---------------

Plugins that use the Meter Plugin SDK for Python:

- [Random](https://github.com/boundary/meter-plugin-sdk-python-random)
