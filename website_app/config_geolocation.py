"""Geolocation configurations geolocation_config.py"""
import os
from website_app.debug_services.debug_log_services import *

log_config_start(__file__, 'geolocation_configuration')

EYECATCH = 'GEOLOCATION'

#ipstack access key (ip address geolocation)
IPSTACK_URL = 'http://api.ipstack.com/'
IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'

################################################################
log_config_param('IPSTACK_API_ACCESSKEY', IPSTACK_API_ACCESSKEY)
log_config_param('IPSTACK_URL', IPSTACK_URL)
################################################################

log_config_finish(__file__, 'geolocation_configuration')
