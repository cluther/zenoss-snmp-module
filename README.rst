zenoss-snmp-module
==================

This project provides a Net-SNMP pass_persist script for monitoring Zenoss. If
you aren't familiar with Net-SNMP's pass_persist option, it allows an external
script to provide responses for all GET and GETNEXT requires under a configured
base OID.

Currently zenoss-snmp-module provides support for the provided ZENOSS-PROCESS-MIB. See the following snmptranslate command for what the MIB provides::

    $ snmptranslate -Tp ZENOSS-PROCESS-MIB::zenossProcessMIB
    +--zenossProcessMIB(3)
       |
       +--zenSystemTable(1)
       |  |
       |  +--zenSystemEntry(1)
       |     |  Index: zenSystemIndex
       |     |
       |     +-- -R-- Integer32 zenSystemIndex(1)
       |     |        Range: 0..65535
       |     +-- -R-- String    zenSystemName(2)
       |              Textual Convention: DisplayString
       |              Size: 0..255
       |
       +--zenProcessTable(2)
       |  |
       |  +--zenProcessEntry(1)
       |     |  Index: zenSystemIndex, zenProcessIndex
       |     |
       |     +-- -R-- Integer32 zenProcessIndex(1)
       |     |        Range: 0..65535
       |     +-- -R-- String    zenProcessName(2)
       |              Textual Convention: DisplayString
       |              Size: 0..255
       |
       +--zenProcessMetricTable(3)
          |
          +--zenProcessMetricEntry(1)
             |  Index: zenSystemIndex, zenProcessIndex, zenProcessMetricIndex
             |
             +-- -R-- Integer32 zenProcessMetricIndex(1)
             |        Range: 0..65535
             +-- -R-- String    zenProcessMetricName(2)
             |        Textual Convention: DisplayString
             |        Size: 0..255
             +-- -R-- String    zenProcessMetricValue(3)
             |        Textual Convention: DisplayString
             |        Size: 0..255
             +-- -R-- EnumVal   zenProcessMetricFresh(4)
                      Textual Convention: TruthValue
                      Values: true(1), false(2)

See the following snmpwalk for how this looks in practice::

    $ snmpwalk -v2c -c public localhost ZENOSS-PROCESS-MIB::zenossProcessMIB
    ZENOSS-PROCESS-MIB::zenSystemIndex.1 = INTEGER: 1
    ZENOSS-PROCESS-MIB::zenSystemName.1 = STRING: localhost
    ZENOSS-PROCESS-MIB::zenProcessIndex.1.1 = INTEGER: 1
    ZENOSS-PROCESS-MIB::zenProcessIndex.1.2 = INTEGER: 2
    ZENOSS-PROCESS-MIB::zenProcessName.1.1 = STRING: zenperfsnmp
    ZENOSS-PROCESS-MIB::zenProcessName.1.2 = STRING: zenwebtx
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.1.1 = INTEGER: 1
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.1 = INTEGER: 1
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.2 = INTEGER: 2
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.3 = INTEGER: 3
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.4 = INTEGER: 4
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.5 = INTEGER: 5
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.6 = INTEGER: 6
    ZENOSS-PROCESS-MIB::zenProcessMetricIndex.1.2.7 = INTEGER: 7
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.1.1 = STRING: eventQueueLength
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.1 = STRING: cyclePoints
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.2 = STRING: dataPoints
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.3 = STRING: devices
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.4 = STRING: eventCount
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.5 = STRING: eventQueueLength
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.6 = STRING: queuedTasks
    ZENOSS-PROCESS-MIB::zenProcessMetricName.1.2.7 = STRING: runningTasks
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.1.1 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.1 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.2 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.3 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.4 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.6 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricValue.1.2.7 = STRING: 0.0
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.1.1 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.1 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.2 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.3 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.4 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.5 = INTEGER: false(2)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.6 = INTEGER: true(1)
    ZENOSS-PROCESS-MIB::zenProcessMetricFresh.1.2.7 = INTEGER: true(1)


Usage
-----

To install zenoss-snmp-module you must run the following commands::

    $ sudo easy_install -U zenoss-snmp-module

If you get the following error, it means the snmp-passpersist dependency can't
be found for your platform::

    No local packages or download links found for snmp-passpersist>=1.2.2
    error: Could not find suitable distribution for Requirement.parse('snmp-passpersist>=1.2.2')

To manually resolve this, run the following commands. Note that this requires
that you install git::

    git clone git://github.com/nagius/snmp_passpersist.git
    cd snmp_passpersist
    sudo python setup.py install
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

    snmpwalk -mALL -v2c -c public localhost zenossProcessMIB


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
    {'1.1.1.1': {'type': 'INTEGER', 'value': '1'},
     '1.1.2.1': {'type': 'STRING', 'value': 'localhost'},
     ... snipped ...
