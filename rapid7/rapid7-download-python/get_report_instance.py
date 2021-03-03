# Uncomment to run sample without library built or installed on system
from __future__ import print_function
import sys
sys.path.append(r'/opt/bmc/rapid7/vm-console-client-python')
import rapid7vmconsole
import base64
import logging
import sys
import time
from rapid7vmconsole.rest import ApiException
from pprint import pprint

config = rapid7vmconsole.Configuration(name='Rapid7')
config.username = '<RAPID7-USERNAME>
config.password = '<RAPID7-PASSWORD>'
config.host = 'https://<RAPID7-FQDN>:<PORT>'
config.verify_ssl = False
config.assert_hostname = False
config.proxy = None
config.ssl_ca_cert = None
config.connection_pool_maxsize = None
config.cert_file = None
config.key_file = None
config.safe_chars_for_path_param = ''

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)
config.debug = False


auth = "%s:%s" % (config.username, config.password)
auth = base64.b64encode(auth.encode('ascii')).decode()
client = rapid7vmconsole.ApiClient(configuration=config)
client.default_headers['Authorization'] = "Basic %s" % auth

# Download report content 
api_instance = rapid7vmconsole.ReportApi(client)

# MUST SPECIFY THE ID OF REPORT BELOW 
#
id = 2824 # int | The identifier of the report.
try:
    # Report Histories
    api_response = api_instance.get_report_instances(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportApi->get_report_instances: %s\n" % e)
