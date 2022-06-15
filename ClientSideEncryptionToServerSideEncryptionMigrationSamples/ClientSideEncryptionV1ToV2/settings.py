# Items to access storage account
CONNECTION_STRING = ""

# Replace these with your local key id, key value and algorithm
LOCAL_KEY_NAME = "local-test-key"
LOCAL_KEY_VALUE = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
KEY_WRAP_ALGORITHM = "example-algorithm"

CONTAINER_NAME = "client-side-encryption-v1-to-v2"

# Whether to overwrite the existing blobs in the container when uploading decrypted blobs.
# If False, new blobs will be created with the given NEW_BLOB_SUFFIX.
OVERWRITE_EXISTING = False
# New blobs will have the name <existing-name> + NEW_BLOB_SUFFIX
NEW_BLOB_SUFFIX = '-v2'


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
