import os
from .base import *

try:
    from .local import *
except ImportError:
    print('No local settings found')
