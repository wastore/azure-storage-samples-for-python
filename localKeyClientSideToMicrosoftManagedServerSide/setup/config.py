# set environmental variables
KEYVAULT_URL = "https://caromekeyvault.vault.azure.net/"
CLIENT_ID = "321522b8-e1b7-4866-8767-ef10dcc25d65"
CLIENT_SECRET = "B_8qDWGZKA~7eIyOu-o85naX2h_54APt36"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
connection_str = "DefaultEndpointsProtocol=https;AccountName=caromedevtest;AccountKey=/IaVQtMqKb0qO1C/miYYAHbyjIla" \
                 "/O3f1kXxMhksgCfa/KDDcdkd1x2iaFGu4tFY3LlR4xYNXMLFrlQOhWZpig==;EndpointSuffix=core.windows.net"

# items to make encryption scope
SUB_ID = "ba45b233-e2ef-4169-8808-49eb0d8eba0d"
RESOURCE_GROUP = "carmen_romero"
STORAGE_ACCOUNT = "caromedevtest"

# replace with name for microsoft managed encryption scope
SERVER_SCOPE_NAME = "server-scope"

cont_name = "privatecsetests"
file = "privatecsetest2.txt"
local_key_path = "setup\localkey.key"
# here put what you want the encrypted blob to be named
new_blob_name = "microsoft-managed-" + file
