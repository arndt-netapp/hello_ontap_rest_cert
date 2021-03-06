Simple script to show the use of the ONTAP REST API when authenticating
with certificate based authentication.

Example of certificate creation and required ONTAP configuration:
1. Create the certificate for the "cert_user" account.  This account name,
   as well as the key and pem filenames, can be changed as required.
~~~text
   linux$ openssl req -x509 -nodes -days 1095 -newkey rsa:2048 \
          -keyout restcert.key -out restcert.pem \
          -subj "/C=US/ST=NC/L=RTP/O=NetApp/CN=cert_user"
~~~
2. Install the restcert.pem file into the cluster or svm:
~~~text
   ontap::> security certificate install -type client-ca -vserver {clus|svm}
~~~
3. Enable SSL client based authentication for the cluster or svm:
~~~text
   ontap::> security ssl modify -vserver {clus|svm} -client-enabled true
~~~
4. Create the account in ONTAP for this user, matching the username given in
   step 1 above.  Note that the application is "http" for the REST API, and
   you can use a different role as required to meet your needs.
~~~text
   ::> security login create -user-or-group-name cert_user -application http \
       -authentication-method cert -role {admin|vsadmin} -vserver {clus|svm}
~~~

Other requirements:
1. Python 3.5 or higher.
2. The netapp-ontap Python package as described at:
   https://pypi.org/project/netapp-ontap/
3. ONTAP 9.6 or higher.

Notes:
1. If using a custom role (other than admin or vsadmin), the custom role must
   must have access to the rest web service of the vserver:
~~~text
vserver services web access create -vserver {svm} -name rest -role {role}
~~~

