
from decouple import config
# from .base import *

# Load the project variable from the .env file
project = config('PROJECT', default='dev')

# Determine which settings to import based on the project variable
if project == 'local':
    print("Running development...", 'green')
    from .local import *
else:
    print("Running production...", 'green')
    from .dev import *