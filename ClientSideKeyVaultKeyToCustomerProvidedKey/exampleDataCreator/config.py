from azure.storage.blob import CustomerProvidedEncryptionKey
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

# if using customer provided key, set values here
customer_key = CustomerProvidedEncryptionKey(key_value="",
                                             key_hash="")

# keyvault key used for encryption
keyname = ""
secret = ""
key_wrap_algorithm = KeyWrapAlgorithm.rsa_oaep #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

cont_name = "client-side-keyvault-key-to-customer-provided-key"
blob_name = "blobExample.txt"
migrated_blob_name = "cpk-" + blob_name