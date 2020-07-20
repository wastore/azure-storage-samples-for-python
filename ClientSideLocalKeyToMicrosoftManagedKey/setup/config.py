KEYVAULT_URL = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
TENANT_ID = ""
connection_str = ""

# items to make encryption scope
SUB_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# replace with name for microsoft managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
SERVER_SCOPE_NAME = "test-server-scope"

cont_name = "client-side-local-key-to-customer-managed-key"
blob_name = "blobExample.txt"
local_key_name = "local-test-key"
# here put what you want the encrypted blob to be named
new_blob_name = "new" + blob_name

# this needs to be replaced with the value of the key used for local client side encryption
local_key = ["your_client_side_encryption_key_value"]
