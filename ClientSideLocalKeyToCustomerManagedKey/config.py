KEYVAULT_URL = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
TENANT_ID = ""
connection_str = ""

# items to make encryption scope
SUB_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# replace with name for customer managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
customer_managed_encryption_scope = "test-customer-scope"
serverside_encryption_keyname = "testkey1"

# this needs to be replaced with the value of the key used for local client side encryption
local_key = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
key_wrap_algorithm = "example-algorithm"

cont_name = "client-side-local-key-to-customer-managed-key"
blob_name = "blobExample.txt"
local_key_name = "local-test-key"
# here put what you want the encrypted blob to be named
migrated_blob_name = "cmk-" + blob_name

# if user wants overwrite to be available, change to True
overwriter = False

