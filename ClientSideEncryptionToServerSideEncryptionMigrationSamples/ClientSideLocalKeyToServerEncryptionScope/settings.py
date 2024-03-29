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

# Replace these with your local key id, key value and algorithm
LOCAL_KEY_NAME = "local-test-key"
LOCAL_KEY_VALUE = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
KEY_WRAP_ALGORITHM = "example-algorithm"

CONTAINER_NAME = "client-side-local-key-to-encryption-scope"

# Whether to overwrite the existing blobs in the container when uploading decrypted blobs.
# If False, new blobs will be created with the given NEW_BLOB_SUFFIX.
OVERWRITE_EXISTING = False
# New blobs will have the name <existing-name> + NEW_BLOB_SUFFIX
NEW_BLOB_SUFFIX = '-ec'


# Replace with your keywrapper
class KeyWrapper:
    def __init__(self, kid, kek):
        self.algorithm = KEY_WRAP_ALGORITHM
        self.kid = kid
        self.kek = kek

    def wrap_key(self, key):
        if self.algorithm == "example-algorithm":
            return key
        return key

    def unwrap_key(self, key, _):
        if self.algorithm == "example-algorithm":
            return key
        return key

    def get_key_wrap_algorithm(self):
        return self.algorithm

    def get_kid(self):
        return self.kid
