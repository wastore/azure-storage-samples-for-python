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

# replace with name for microsoft managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
SERVER_MANAGED_ENCRYPTION_SCOPE = "test-server-scope"

LOCAL_KEY_VALUE = "6wcF1o5QEzJJKIrH8QpR7mGjSqTP3d28ScSxV0hJ67Q="
KEY_WRAP_ALGORITHM = "example-algorithm"

CONTAINER_NAME = "client-side-local-key-to-microsoft-managed-key"
BLOB_NAME = "blobExample.txt"
LOCAL_KEY_NAME = "local-test-key"
# here put what you want the encrypted blob to be named
MIGRATED_BLOB_NAME = "mmk-" + BLOB_NAME

# if user wants to overwrite blob with the same name as migrated_blob_name in the migration.py, as well as the blob_name
# uploaded in the sampleDataCreator.py, change value of overwriter to True
OVERWRITER = False
