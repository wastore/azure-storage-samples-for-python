
from azure.keyvault.keys.crypto import KeyWrapAlgorithm

# Items to access keyvault
KEYVAULT_URL = ""

# Items to access storage account
CONNECTION_STRING = ""
# Only needed to create an encryption scope
SUBSCRIPTION_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# Provide the name to a pre-existing encryption scope or set CREATE_ENCRYPTION_SCOPE
# to True to have the script create a new encryption scope
ENCRYPTION_SCOPE_NAME = "testencryptionscope"
CREATE_ENCRYPTION_SCOPE = False
# If CREATE_ENCRYPTION_SCOPE is True, specify this to create a Customer Managed Encryption
# Scope pointing to your KeyVault. Use the full KeyVault Key Identifier URL
# If this is empty, a Microsoft Managed Encryption Scope will be created instead.
ENCRYPTION_SCOPE_KEY_KEYVAULT_URI = ""

# Keyvault key used for encryption
# CLIENT_SIDE_KEYNAME should used when wrapping key with RSA keywrap algorithm, otherwise use KEYVAULT_SECRET
CLIENT_SIDE_KEYNAME = ""
KEYVAULT_SECRET = ""
KEY_WRAP_ALGORITHM = KeyWrapAlgorithm.aes_256  #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

CONTAINER_NAME = "client-side-keyvault-key-to-microsoft-managed-key"

# Whether to overwrite the existing blobs in the contianer when uploading decrypting blobs.
# If False, new blobs will be created with the given NEW_BLOB_SUFFIX.
OVERWRITE_EXISTING = False
# New blobs will have the name <existing-name> + NEW_BLOB_SUFFIX
NEW_BLOB_SUFFIX = '-mmk'
