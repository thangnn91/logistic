# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "NZsERl2bqsk4RjiuD38a"

# Secret key for signing cookies
SECRET_KEY = "XDrN9AQ4m3YuE34LH8r7"

# Auto reload templates
TEMPLATES_AUTO_RELOAD = True

DB_CONNECTSTRING = {
            'user' : 'root',
            'passwd' : 'nnt',
            'host' : '127.0.0.1',
            'schema' : 'logistic',
            'charset' : 'utf8mb4'
}