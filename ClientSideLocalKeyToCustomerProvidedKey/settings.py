from azure.storage.blob import CustomerProvidedEncryptionKey

# the below items are fake and need to be replaced

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

# customer provided key for server side encryption
CUSTOMER_PROVIDED_KEY = CustomerProvidedEncryptionKey(key_value="",

                                                      key_hash="")

LOCAL_KEY_VALUE = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
KEY_WRAP_ALGORITHM = "example-algorithm"

CONTAINER_NAME = "client-side-local-key-to-customer-provided-key"
BLOB_NAME = "blobExample.txt"
LOCAL_KEY_NAME = "local-test-key"
# here put what you want the serverside encrypted blob to be named
MIGRATED_BLOB_NAME = "cpk-" + BLOB_NAME

# if user wants to overwrite blob with the same name as migrated_blob_name in the migration.py, as well as the blob_name
# uploaded in the sampleDataCreator.py, change value of overwriter to True
OVERWRITER = False


# replace with your keywrapper
class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek):
        self.algorithm = KEY_WRAP_ALGORITHM
        self.kek = kek
        self.kid = kek

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
