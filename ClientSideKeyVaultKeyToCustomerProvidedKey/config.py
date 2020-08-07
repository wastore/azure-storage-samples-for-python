from azure.storage.blob import CustomerProvidedEncryptionKey
from azure.keyvault.keys.crypto import KeyWrapAlgorithm

# the below values are fake and need to be replaced

# items to access keyvault
KEYVAULT_URL = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
TENANT_ID = ""

# items to access storage account
CONNECTION_STRING = ""
SUBSCRIPTION_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# if using customer provided key, set values here
CUSTOMER_PROVIDED_KEY = CustomerProvidedEncryptionKey(key_value="",
                                                      key_hash="")

# keyvault key used for encryption
CLIENT_SIDE_KEYNAME = ""
KEYVAULT_SECRET = ""
CLIENT_SIDE_KEY_WRAP_ALGORITHM = KeyWrapAlgorithm.rsa_oaep #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

CONTAINER_NAME = "client-side-keyvault-key-to-customer-provided-key"
BLOB_NAME = "blobExample.txt"
MIGRATED_BLOB_NAME = "cpk-" + BLOB_NAME

# if user wants to overwrite blob with the same name as migrated_blob_name in the migration.py, as well as the blob_name
# uploaded in the sampleDataCreator.py, change value of overwriter to True
OVERWRITER = False
