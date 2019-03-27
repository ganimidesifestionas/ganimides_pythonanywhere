"""pagination configurations config_pagination.py"""

import os
from website_app.debug_services.debug_log_services import *

log_module_start('pagination_configuration')

EYECATCH = 'PAGINATION'

PER_PAGE = 10
CSS_FRAMEWORK = 'bootstrap4'
LINK_SIZE = 'sm'
# decide whether or not a single page returns pagination
SHOW_SINGLE_PAGE = False

################################################################
log_config_param('PER_PAGE', PER_PAGE)
log_config_param('CSS_FRAMEWORK', CSS_FRAMEWORK)
log_config_param('LINK_SIZE', LINK_SIZE)
log_config_param('SHOW_SINGLE_PAGE', SHOW_SINGLE_PAGE)
################################################################

log_module_finish('pagination_configuration')
