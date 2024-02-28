import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# read env variable DEACTIVATE_RATE_LIMIT and set to false if not exists
# that's a little convoluted to ensure that the rate limiting only gets deactivated if the variable is set to 'true'
# otherwise, the rate limiting will be activated even of a random/faulty string is set
activate_rate_limiting = os.environ.get('DEACTIVATE_RATE_LIMIT', 'false') != 'true'
limiter = Limiter(key_func=get_remote_address, enabled=activate_rate_limiting)