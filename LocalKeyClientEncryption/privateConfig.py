##########################################
# this is a configuration file for CPK-N #
# migration using Keyvault. Please update#
# the follow variables as needed         #
##########################################

import os
from azure.storage.blob import CustomerProvidedEncryptionKey

# set environmental variables
KEYVAULT_URL = os.getenv('AZURE_KEYVAULT_DNS_NAME')
CLIENT_ID = os.getenv('ACTIVE_DIRECTORY_APPLICATION_ID')
CLIENT_SECRET = os.getenv('ACTIVE_DIRECTORY_APPLICATION_SECRET')
TENANT_ID = os.getenv('ACTIVE_DIRECTORY_TENANT_ID')
connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# items to make encryption scope
SUB_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP_NAME")
STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT_NAME")
# replace with name for server managed encryption scope
SERVER_SCOPE_NAME = "server-scope"
# replace with name for customer managed encryption scope
CUSTOMER_SCOPE_NAME = "customer-scope"

# if using customer provided key, set values here
customer_key = CustomerProvidedEncryptionKey(key_value="MDEyMzQ1NjcwMTIzNDU2NzAxMjM0NTY3MDEyMzQ1Njc=",
                                             key_hash="3QFFFpRA5+XANHqwwbT4yXDmrT/2JaLt/FKHjzhOdoE=")

# optional to change if using for your own migration
cont_name = "privatecsetests"
file = "privatecsetest1.txt"  # your file name
keyvault_keyname = "testkey2"