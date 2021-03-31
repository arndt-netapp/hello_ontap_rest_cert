#! /usr/bin/env python3

# Simple script to show the use of the ONTAP REST API when authenticating
# with certificate based authentication.
#
# Example of certificate creation and required ONTAP configuration:
# 1. Create the certificate for the "cert_user" account.  This account name,
#    as well as the key and pem filenames, can be changed as required.
#    linux$ openssl req -x509 -nodes -days 1095 -newkey rsa:2048 \
#           -keyout restcert.key -out restcert.pem \
#           -subj "/C=US/ST=NC/L=RTP/O=NetApp/CN=cert_user"
# 2. Install the restcert.pem file into the cluster or svm:
#    ontap::> security certificate install -type client-ca -vserver {clus|svm}
# 3. Enable SSL client based authentication for the cluster or svm:
#    ontap::> security ssl modify -vserver {clus|svm} -client-enabled true
# 4. Create the account in ONTAP for this user, matching the username given in
#    step 1 above.  Note that the application is "http" for the REST API, and
#    you can use a different role as required to meet your needs.
#    ::> security login create -user-or-group-name cert_user -application http \
#        -authentication-method cert -role {admin|vsadmin} -vserver {clus|svm}
#
# Other requirements:
# 1. Python 3.5 or higher.
# 2. The netapp-ontap Python package as described at:
#    https://pypi.org/project/netapp-ontap/
# 3. ONTAP 9.6 or higher.

# Import the required netap_ontap modules.
from netapp_ontap import HostConnection, NetAppRestError, config, utils
from netapp_ontap.resources import Cluster

# Uncomment these for additional ONTAP REST API debugging.
#import logging
#logging.basicConfig(level=logging.DEBUG)
#utils.DEBUG = 1
#utils.LOG_ALL_API_CALLS = 1

# Define the ONTAP endpoint and local certificate files.
cluster = "ontapsim1"
pemfile = "restcert.pem"
keyfile = "restcert.key"

# Setup the REST API connection to ONTAP.
# Using verify=False to ignore that we have self-signed SSL certificates.
config.CONNECTION = HostConnection(
    cluster, cert=pemfile, key=keyfile, verify=False,
)

# Get the cluster version from the /api/cluster REST API call to show that
# out certificate based authentication is working. 
print("Connecting to host " + cluster)
try:
    clus = Cluster()
    clus.get(fields="version")
    version = clus.version.full
    print("Host " + cluster + " is running: " + version)
except NetAppRestError:
    print("Error connecting to host " + cluster)
    raise
