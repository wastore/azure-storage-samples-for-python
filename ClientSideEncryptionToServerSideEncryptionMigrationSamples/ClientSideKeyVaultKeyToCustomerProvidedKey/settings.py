
from azure.keyvault.keys.crypto import KeyWrapAlgorithm
from azure.storage.blob import CustomerProvidedEncryptionKey

# Items to access keyvault
KEYVAULT_URL = ""

# Items to access storage account
CONNECTION_STRING = ""
# Only needed to create an encryption scope
SUBSCRIPTION_ID = ""
RESOURCE_GROUP = ""
STORAGE_ACCOUNT = ""

# if using customer provided key, set values here
CUSTOMER_PROVIDED_KEY = CustomerProvidedEncryptionKey(key_value="",
                                                      key_hash="")

# Keyvault key used for encryption
# CLIENT_SIDE_KEYNAME should used when wrapping key with RSA keywrap algorithm, otherwise use KEYVAULT_SECRET
CLIENT_SIDE_KEYNAME = ""
KEYVAULT_SECRET = ""
KEY_WRAP_ALGORITHM = KeyWrapAlgorithm.aes_256  #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

CONTAINER_NAME = "client-side-keyvault-key-to-customer-provided-key"

# Whether to overwrite the existing blobs in the container when uploading decrypted blobs.
# If False, new blobs will be created with the given NEW_BLOB_SUFFIX.
OVERWRITE_EXISTING = False
# New blobs will have the name <existing-name> + NEW_BLOB_SUFFIX
NEW_BLOB_SUFFIX = '-cpk'
