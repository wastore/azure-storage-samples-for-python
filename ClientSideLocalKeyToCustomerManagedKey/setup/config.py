KEYVAULT_URL = ["your_keyvault_url"]
CLIENT_ID = ["your_client_id"]
CLIENT_SECRET = ["your_client_id"]
TENANT_ID = ["your_tenant_id"]
connection_str = ["your_azure_storage_account_connection_str"]

# items to make encryption scope
SUB_ID = ["your_subscription_id"]
RESOURCE_GROUP = ["your_resource_group_name"]
STORAGE_ACCOUNT = ["your_storage_account_name"]

# replace with name for customer managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
CUSTOMER_SCOPE_NAME = ["your_encryption_scope_name"]
keyname = ["your_keyvault_key_name"]

cont_name = "client-side-local-key-to-customer-managed-key"
blob_name = "blobExample.txt"
local_key_name = "local-test-key"
# here put what you want the encrypted blob to be named
new_blob_name = "new" + blob_name

# this needs to be replaced with the value of the key used for local client side encryption
local_key = ["your_client_side_encryption_key_value"]