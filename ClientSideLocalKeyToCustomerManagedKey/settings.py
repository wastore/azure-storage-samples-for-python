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

# if you want program to create encryption scope, change to True. if not, it will access a preexisting
# encryption scope with the name CUSTOMER_MANAGED_ENCRYPTION_SCOPE
CREATE_ENCRYPTION_SCOPE = False
# replace with name for customer managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
CUSTOMER_MANAGED_ENCRYPTION_SCOPE = "test-customer-scope"
SERVER_SIDE_KEYNAME = "testkey1"

# this needs to be replaced with the value of the key used for local client side encryption
LOCAL_KEY_VALUE = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
KEY_WRAP_ALGORITHM = "example-algorithm"

CONTAINER_NAME = "client-side-local-key-to-customer-managed-key"
BLOB_NAME = "blobExample.txt"
LOCAL_KEY_NAME = "local-test-key"
# here put what you want the encrypted blob to be named
MIGRATED_BLOB_NAME = "cmk-" + BLOB_NAME

# if user wants to overwrite blob with the same name as migrated_blob_name in the migration.py, as well as the blob_name
# uploaded in the sampleDataCreator.py, change value of overwriter to True
OVERWRITER = False


# replace with your keywrapper
class KeyWrapper:
    # REPLACE WITH YOUR PREFERRED KEYWRAPPING ALGORITHMS AND METHODS

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
