zenoss-snmp-module
==================

This project provides a Net-SNMP pass_persist script for monitoring Zenoss. If
you aren't familiar with Net-SNMP's pass_persist option, it allows an external
script to provide responses for all GET and GETNEXT requires under a configured
base OID.

Currently zenoss-snmp-module provides support for the provided ZENOSS-PROCESS-
MIB. See the following snmptranslate command for what the MIB provides::

    $ snmptranslate -Tp ZENOSS-PROCESS-MIB::zenossProcessMIB
    +--zenossProcessMIB(3)
       |
       +--zenSystemTable(1)
       |  |
       |  +--zenSystemEntry(1)
       |     |  Index: zenSystemName
       |     |
       |     +-- -R-- String    zenSystemName(1)
       |              Textual Convention: DisplayString
       |              Size: 0..255
       |
       +--zenProcessTable(2)
       |  |
       |  +--zenProcessEntry(1)
       |     |  Index: zenSystemName, zenProcessName
       |     |
       |     +-- -R-- String    zenProcessName(1)
       |              Textual Convention: DisplayString
       |              Size: 0..255
       |
       +--zenProcessMetricTable(3)
          |
          +--zenProcessMetricEntry(1)
             |  Index: zenSystemName, zenProcessName, zenProcessMetricName
             |
             +-- -R-- String    zenProcessMetricName(1)
             |        Textual Convention: DisplayString
             |        Size: 0..255
             +-- -R-- String    zenProcessMetricValue(2)
             |        Textual Convention: DisplayString
             |        Size: 0..255
             +-- -R-- String    zenProcessMetricCyclesSinceUpdate(3)
                      Textual Convention: DisplayString
                      Size: 0..255

    $ snmpwalk -v2c -c public localhost ZENOSS-PROCESS-MIB::zenossProcessMIB
    ZENOSS-PROCESS-MIB::zenSystemName."localhost" = STRING: localhost
    ZENOSS-PROCESS-MIB::zenProcessName."localhost"."zenhub" = STRING: zenhub
    ZENOSS-PROCESS-MIB::zenProcessName."localhost"."zenwebtx" = STRING: zenwebtx
    ZENOSS-PROCESS-MIB::zenProcessName."localhost"."zencommand" = STRING: zencommand
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."services" = STRING: services
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."totalTime" = STRING: totalTime
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."totalEvents" = STRING: totalEvents
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."invalidations" = STRING: invalidations
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."totalCallTime" = STRING: totalCallTime
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenhub"."workListLength" = STRING: workListLength
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."devices" = STRING: devices
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."dataPoints" = STRING: dataPoints
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."eventCount" = STRING: eventCount
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."cyclePoints" = STRING: cyclePoints
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."queuedTasks" = STRING: queuedTasks
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."runningTasks" = STRING: runningTasks
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zenwebtx"."eventQueueLength" = STRING: eventQueueLength
    ZENOSS-PROCESS-MIB::zenProcessMetricName."localhost"."zencommand"."eventQueueLength" = STRING: eventQueueLength
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."devices" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."dataPoints" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."eventCount" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."cyclePoints" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."queuedTasks" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."runningTasks" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."eventQueueLength" = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."services" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."totalTime" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."totalEvents" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."invalidations" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."totalCallTime" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenhub"."workListLength" = STRING: 2.35
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."devices" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."dataPoints" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."eventCount" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."cyclePoints" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."queuedTasks" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."runningTasks" = STRING: 0.48
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zenwebtx"."eventQueueLength" = STRING: 0.45
    ZENOSS-PROCESS-MIB::zenProcessMetricCyclesSinceUpdate."localhost"."zencommand"."eventQueueLength" = STRING: 0.12


Usage
-----

To install zenoss-snmp-module you must run the following command::

    sudo easy_install -U zenoss-snmp-module

Once installed, the ``zenoss-snmp-module`` script provides built-in support for
helping you configure it. See the following command examples for installing the
associated MIB and configuring snmpd::

    # Install ZENOSS-PROCESS-MIB.
    zenoss-snmp-module --mib | sudo tee /usr/share/snmp/mibs/ZENOSS-PROCESS-MIB.txt

    # Add pass_persist line to snmpd.conf.
    zenoss-snmp-module --snmpd | sudo tee -a /etc/snmp/snmpd.conf

    # Restart snmpd service.
    sudo service snmpd restart

After changing snmpd.conf you must restart the snmpd service. Then you should
be able to test with the following command::

    # Walk the entire zenossProcessMIB.
    snmpwalk -mALL -v2c -c public localhost zenossProcessMIB

Try snmpwalk commands like the following to get more specific results::

    # Only show metric values for the zenwebtx proces on the localhost collector.
    snmpwalk -mALL -v2c -c public localhost 'zenProcessMetricValue."localhost"."zenwebtx"'

    # Show how many cycles it's been since each metric was updated.
    snmpwalk -mALL -v2c -c public localhost 'zenProcessMetricCyclesSinceUpdate."localhost"'

You will need to know the OIDs for these values to poll them with Zenoss. Use a
command like the following to discover the OID for a given value. Note that
because these OIDs are just encoded system, process and metric names, they will
return the expected data from any system and can be considered permanent::

    # Translate from name to OID.
    snmptranslate -On 'ZENOSS-PROCESS-MIB::zenProcessMetricValue."localhost"."zenwebtx"."queuedTasks"'


Troubleshooting
---------------

Normally zenoss-snmp-module is run from within snmpd. This makes it difficult
to troubleshoot problems. To test the script outside of snmpd, you can run
``zenoss-snmp-module`` as root. If things are working properly, this will
appear to do nothing.

See the following session as an example::

    # zenoss-snmp-module
    PING
    PONG
    DUMP
    {'1.1.1.9.108.111.99.97.108.104.111.115.116': {'type': 'STRING',
                                                   'value': 'localhost'},
    ... snipped ...

It can also be useful to stop the snmpd service and run it in the foreground
with just the useful debugging enabled::

    sudo service snmpd stop
    sudo snmpd -fV -Lo -Ducd-snmp/pass_persist -Doutput

Be sure to start the snmpd service once you're done testing.
