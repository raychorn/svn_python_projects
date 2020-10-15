# Django settings for jobsportal project.

import os

TEMPLATE_DIRS = tuple(list(TEMPLATE_DIRS) + list(os.path.join(os.path.dirname(__file__), 'templates'),))

