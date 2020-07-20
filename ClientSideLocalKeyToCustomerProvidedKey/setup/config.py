from azure.storage.blob import CustomerProvidedEncryptionKey

KEYVAULT_URL = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
TENANT_ID = ""
connection_str = ""

# items to make encryption scope
SUB_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# customer provided key for server side encryption
customer_key = CustomerProvidedEncryptionKey(key_value=[""],

                                             key_hash=[""])
local_key = ["your_client_side_encryption_key_value"]
# here put what you want the encrypted blob to be named

cont_name = "client-side-local-key-to-customer-managed-key"
blob_name = "blobExample.txt"
local_key_name = "local-test-key"
# here put what you want the encrypted blob to be named
new_blob_name = "new" + blob_name
