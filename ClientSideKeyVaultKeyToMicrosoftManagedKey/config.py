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

# replace with name for customer managed encryption scope
SERVER_MANAGED_ENCRYPTION_SCOPE = "test-server-scope"
CLIENT_SIDE_KEYNAME = ""
KEYVAULT_SECRET = ""
KEY_WRAP_ALGORITHM = KeyWrapAlgorithm.rsa1_5 #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

CONTAINER_NAME = "client-side-keyvault-key-to-microsoft-managed-key"
BLOB_NAME = "blobExample.txt"
MIGRATED_BLOB_NAME = "mmk-" + BLOB_NAME

# if user wants to overwrite blob with the same name as migrated_blob_name in the migration.py, as well as the blob_name
# uploaded in the sampleDataCreator.py, change value of overwriter to True
OVERWRITER = False
