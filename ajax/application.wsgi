import sys
sys.path.append('/var/www/avenews/ajax/')

from avenews import app as application

import monitor
monitor.start(interval=1.0)
