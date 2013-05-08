##############################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
##############################################################################

import math
import os
import sys

import argparse
import rrdtool
import snmp_passpersist as snmp
import time
import which


BASE_OID = '.1.3.6.1.4.1.14296.3'

PP = None
ZENHOME = None


def main():
    global PP
    global ZENHOME

    default_zenhome = os.getenv('ZENHOME', '/opt/zenoss')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--zenhome',
        help='ZENHOME directory. Default is {0}'.format(default_zenhome),
        default=default_zenhome)

    help_group = parser.add_argument_group(
        'Configuration Help',
        'These arguments print configuration information then exit.')

    # Nested mutually exclusive groups currently appear to be broken.
    # Leaving this here so it'll work once it's fixed in Python.
    mutex_help_group = help_group.add_mutually_exclusive_group()

    mutex_help_group.add_argument(
        '--readme', action='store_true',
        help='Prints README.')

    mutex_help_group.add_argument(
        '--info', action='store_true',
        help='Prints system, process and metric information.')

    mutex_help_group.add_argument(
        '--mib', action='store_true',
        help='Prints ZENOSS-PROCESS-MIB.')

    mutex_help_group.add_argument(
        '--snmpd', action='store_true',
        help='Prints snmpd.conf configuration excerpt.')

    args = parser.parse_args()

    ZENHOME = args.zenhome

    if args.readme:
        print_local_file('README.rst')
        sys.exit(0)

    if args.info:
        print_information()
        sys.exit(0)

    if args.mib:
        print_local_file('ZENOSS-PROCESS-MIB.txt')
        sys.exit(0)

    if args.snmpd:
        print_snmpd()
        sys.exit(0)

    # Required for snmp_passpersist to work.
    unbuffer_stdout()

    # Respond to OID requests.
    PP = snmp.PassPersist(BASE_OID)

    try:
        PP.start(update, 10)
    except KeyboardInterrupt:
        # It's OK. Let the user quit.
        pass


def print_local_file(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        print f.read()


def print_information():
    for system_name in system_names():
        print "System: {0}".format(system_name)

        for process_name in process_names(system_name):
            print "  Process: {0}".format(process_name)

            for metric_name in metric_names(system_name, process_name):
                print "    Metric: {0}".format(metric_name)

            print

        print


def print_snmpd():
    global ZENHOME

    try:
        script_path = which.which('zenoss-snmp-module')
    except which.WhichError:
        script_path = '/usr/bin/zenoss-snmp-module'

    print "# Pass control of ZENOSS-PROCESS-MIB::zenossProcessMIB."
    print "pass_persist {0} {1} --zenhome={2}".format(
        BASE_OID, script_path, ZENHOME)


def unbuffer_stdout():
    unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbuffered


def none_or_nan(value):
    if value is None or math.isnan(value):
        return True


class MIB:
    '''
    Class representation of ZENOSS-PROCESS-MIB.
    '''
    zenSystemTable = '1'
    zenSystemEntry = '1.1'
    zenSystemName = '1.1.1'
    zenProcessTable = '2'
    zenProcessEntry = '2.1'
    zenProcessName = '2.1.1'
    zenProcessMetricTable = '3'
    zenProcessMetricEntry = '3.1'
    zenProcessMetricName = '3.1.1'
    zenProcessMetricValue = '3.1.2'
    zenProcessMetricCyclesSinceUpdate = '3.1.3'


def oid(identifier, string_indices):
    return '{0}.{1}'.format(
        identifier,
        '.'.join(map(PP.encode, string_indices)))


def update():
    global PP

    update_zenSystemTable(PP)


def update_zenSystemTable(PP):
    for system_name in system_names():
        indices = [system_name]
        PP.add_str(
            oid(MIB.zenSystemName, indices),
            system_name)

        update_zenProcessTable(PP, system_name)


def update_zenProcessTable(PP, system_name):
    for process_name in process_names(system_name):
        indices = [system_name, process_name]
        PP.add_str(oid(MIB.zenProcessName, indices), process_name)

        update_zenProcessMetricTable(PP, system_name, process_name)


def update_zenProcessMetricTable(PP, system_name, process_name):
    for metric_name in metric_names(system_name, process_name):
        indices = [system_name, process_name, metric_name]
        PP.add_str(oid(MIB.zenProcessMetricName, indices), metric_name)

        try:
            rrd_filename = daemons_path(
                system_name,
                '{0}_{1}.rrd'.format(process_name, metric_name))

            info, _, values = rrdtool.fetch(rrd_filename, 'AVERAGE')

            # Often the last sample is missing. Allow for it by using
            # the second-most-recent sample instead.
            if not none_or_nan(values[-1][0]):
                metric_value = values[-1][0]
            else:
                metric_value = values[-2][0]

            if not none_or_nan(metric_value):
                PP.add_str(
                    oid(MIB.zenProcessMetricValue, indices),
                    metric_value)

            # Figure out how many cycles (with decimal precision) it has
            # been since the metric was last updated. This is a better
            # measure than seconds since update because some metrics are
            # stored more frequently than others.
            step = info[2]
            seconds_since_update = time.time() - rrdtool.last(rrd_filename)
            cycles_since_update = seconds_since_update / step

            PP.add_str(
                oid(MIB.zenProcessMetricCyclesSinceUpdate, indices),
                '{0:.2f}'.format(cycles_since_update))

        except Exception:
            pass


def zen_path(*args):
    return os.path.join(ZENHOME, *args)


def daemons_path(*args):
    return zen_path('perf', 'Daemons', *args)


def system_names():
    for dirname in os.listdir(daemons_path()):
        if os.path.isdir(daemons_path(dirname)):
            yield dirname


def process_names(system_name):
    yielded = set()

    for filename in os.listdir(daemons_path(system_name)):
        if not os.path.isfile(daemons_path(system_name, filename)):
            continue

        if not filename.endswith('.rrd'):
            continue

        process_name = filename.split('_', 1)[0]
        if process_name not in yielded:
            yielded.add(process_name)
            yield process_name


def metric_names(system_name, process_name):
    for filename in os.listdir(daemons_path(system_name)):
        if not os.path.isfile(daemons_path(system_name, filename)):
            continue

        if not filename.endswith('.rrd'):
            continue

        if not filename.startswith('{0}_'.format(process_name)):
            continue

        yield filename.split('_', 1)[1].split('.')[0]


if __name__ == '__main__':
    main()
