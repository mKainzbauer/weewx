#!/usr/bin/env python
#
#    Copyright (c) 2013-2023 Matthew Wall and Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Command line utility for configuring devices."""

import importlib
import logging
import sys

import configobj

import weecfg
import weeutil.logger
import weewx
from weeutil.weeutil import to_int

log = logging.getLogger(__name__)


def main():
    # Load the configuration file
    try:
        config_fn, config_dict = weecfg.read_config(None, sys.argv[1:])
    except (OSError, configobj.ConfigObjError) as e:
        sys.exit(e)
    print('Using configuration file %s' % config_fn)

    # Set weewx.debug as necessary:
    weewx.debug = to_int(config_dict.get('debug', 0))

    # Customize the logging with user settings.
    weeutil.logger.setup('wee_device', config_dict)

    try:
        # Find the device type
        device_type = config_dict['Station']['station_type']
        driver = config_dict[device_type]['driver']
    except KeyError as e:
        sys.exit("Unable to determine driver: %s" % e)

    print(f"Using driver {driver}.")

    # Try to load the driver
    try:
        driver_module = importlib.import_module(driver)
        loader_function = getattr(driver_module, 'configurator_loader')
    except ImportError as e:
        msg = "Unable to import driver %s: %s." % (driver, e)
        log.error(msg)
        sys.exit(msg)
    except AttributeError as e:
        msg = "The driver %s does not include a configuration tool." % driver
        log.info("%s: %s" % (msg, e))
        sys.exit(msg)
    except Exception as e:
        msg = "Cannot load configurator for '%s'." % device_type
        log.error("%s: %s" % (msg, e))
        sys.exit(msg)

    device = loader_function(config_dict)

    # Try to determine driver name and version.
    try:
        driver_name = driver_module.DRIVER_NAME
    except AttributeError:
        driver_name = '?'
    try:
        driver_vers = driver_module.DRIVER_VERSION
    except AttributeError:
        driver_vers = '?'
    print('Using %s driver version %s (%s)' % (driver_name, driver_vers, driver))

    device.configure(config_dict)


if __name__ == "__main__":
    main()