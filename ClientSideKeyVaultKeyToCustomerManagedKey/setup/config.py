from azure.keyvault.keys.crypto import KeyWrapAlgorithm
# the below values are fake and need to be replaced

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
customer_managed_encryption_scope = "test-customer-scope"
keyname = ""
serverside_encryption_keyname = ""
secret = ""
key_wrap_algorithm = KeyWrapAlgorithm.rsa1_5 #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

cont_name = "client-side-keyvault-key-to-customer-managed-key"
blob_name = "blobExample.txt"
migrated_blob_name = "cmk-" + blob_name
