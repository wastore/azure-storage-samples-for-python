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
customer_key = CustomerProvidedEncryptionKey(key_value="",

                                             key_hash="")

local_key = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
key_wrap_algorithm = "example-algorithm"

cont_name = "client-side-local-key-to-customer-provided-key"
blob_name = "blobExample.txt"
local_key_name = "local-test-key"
# here put what you want the serverside encrypted blob to be named
migrated_blob_name = "cpk-" + blob_name

# if user wants overwrite to be available, change to True
overwriter = False