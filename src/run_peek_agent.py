#!/usr/bin/env python
"""
 * synnova.py
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by
 *  Synerty Pty Ltd
 *
"""

from rapui import LoggingSetup

LoggingSetup.setup()

from twisted.internet import reactor

from rapui import RapuiConfig
from rapui.DeferUtil import printFailure
from rapui.util.Directory import DirSettings

RapuiConfig.enabledJsRequire = False

import logging

# EXAMPLE LOGGING CONFIG
# Hide messages from vortex
# logging.getLogger('rapui.vortex.VortexClient').setLevel(logging.INFO)

# logging.getLogger('peek_agent_pof.realtime.RealtimePollerEcomProtocol'
#                   ).setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Set the parallelism of the database and reactor
reactor.suggestThreadPoolSize(10)


def main():
    # defer.setDebugging(True)
    # sys.argv.remove(DEBUG_ARG)
    # import pydevd
    # pydevd.settrace(suspend=False)


    from peek_platform import PeekPlatformConfig
    PeekPlatformConfig.componentName = "peek_agent"

    # The config depends on the componentName, order is important
    from peek_agent.PeekAgentConfig import peekAgentConfig
    PeekPlatformConfig.config = peekAgentConfig

    # Set default logging level
    logging.root.setLevel(peekAgentConfig.loggingLevel)

    # Initialise the rapui Directory object
    DirSettings.defaultDirChmod = peekAgentConfig.DEFAULT_DIR_CHMOD
    DirSettings.tmpDirPath = peekAgentConfig.tmpPath

    # First, setup the Vortex Agent
    from peek_platform.PeekVortexClient import peekVortexClient
    d = peekVortexClient.connect()

    # Start Update Handler,
    from peek_platform.sw_update_client.PeekSwUpdateHandler import peekSwUpdateHandler
    d.addCallback(lambda _: peekSwUpdateHandler.start())

    d.addErrback(printFailure)

    # Init the realtime handler

    logger.info('Peek Agent is running, version=%s', peekAgentConfig.platformVersion)
    reactor.run()


if __name__ == '__main__':
    main()
