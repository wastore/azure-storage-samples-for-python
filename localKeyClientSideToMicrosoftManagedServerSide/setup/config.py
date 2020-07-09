import os
from azure.storage.blob import CustomerProvidedEncryptionKey

# set environmental variables
KEYVAULT_URL = "https://caromekeyvault.vault.azure.net/"
CLIENT_ID = "321522b8-e1b7-4866-8767-ef10dcc25d65"
CLIENT_SECRET = "B_8qDWGZKA~7eIyOu-o85naX2h_54APt36"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
connection_str = "DefaultEndpointsProtocol=https;AccountName=caromedevtest;AccountKey=/IaVQtMqKb0qO1C/miYYAHbyjIla" \
                 "/O3f1kXxMhksgCfa/KDDcdkd1x2iaFGu4tFY3LlR4xYNXMLFrlQOhWZpig==;EndpointSuffix=core.windows.net "

# items to make encryption scope
SUB_ID = "ba45b233-e2ef-4169-8808-49eb0d8eba0d"
RESOURCE_GROUP = "carmen_romero"
STORAGE_ACCOUNT = "caromedevtest"
# replace with name for server managed encryption scope
SERVER_SCOPE_NAME = "server-scope"
# replace with name for customer managed encryption scope
CUSTOMER_SCOPE_NAME = "customer-scope"

# if using customer provided key, set values here
customer_key = CustomerProvidedEncryptionKey(key_value="MDEyMzQ1NjcwMTIzNDU2NzAxMjM0NTY3MDEyMzQ1Njc=",
                                             key_hash="3QFFFpRA5+XANHqwwbT4yXDmrT/2JaLt/FKHjzhOdoE=")

cont_name = "privatecsetests"
file = "privatecsetest2.txt"
keyvault_keyname = "testkey2"
