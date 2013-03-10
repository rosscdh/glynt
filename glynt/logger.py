import logging
from local_settings import SPLUNKSTORM_ENDPOINT, SPLUNKSTORM_PORT


class SplunkStormLogger(logging.handlers.SysLogHandler):
    host = SPLUNKSTORM_ENDPOINT
    port = SPLUNKSTORM_PORT
    def __init__(self):
        super(SplunkStormLogger, self).__init__(address=(self.host, self.port,))
