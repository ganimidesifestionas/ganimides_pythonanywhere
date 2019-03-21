"""Geolocation configurations geolocation_config.py"""
import os
from website_app.debug_services.debug_log_services import *

log_module_start('geolocation_configuration')

EYECATCH = 'GEOLOCATION'

#ipstack access key (ip address geolocation)
IPSTACK_URL = 'http://api.ipstack.com/'
IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'

################################################################
log_variable('IPSTACK_API_ACCESSKEY', IPSTACK_API_ACCESSKEY)
log_variable('IPSTACK_URL', IPSTACK_URL)
################################################################

log_module_finish('geolocation_configuration')
