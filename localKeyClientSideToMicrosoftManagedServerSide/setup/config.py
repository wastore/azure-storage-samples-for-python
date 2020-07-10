KEYVAULT_URL = ["your_keyvault_url"]
CLIENT_ID = ["your_client_id"]
CLIENT_SECRET = ["your_client_id"]
TENANT_ID = ["your_tenant_id"]
connection_str = ["your_azure_storage_account_connection_str"]

# items to make encryption scope
SUB_ID = ["your_subscription_id"]
RESOURCE_GROUP = ["your_resource_group_name"]
STORAGE_ACCOUNT = ["your_storage_account_name"]

# replace with name for microsoft managed encryption scope
# this will be made automatically in the main program, so just insert what you want the name to be
SERVER_SCOPE_NAME = ["name_for_your_customer_managed_encryption_scope"]

cont_name = ["your_blob_container_name"]
blob_name = ["your_blob_name.txt"]
local_key = ["your_client_side_encryption_key_value"]
local_key_name = ["your_local_key_name"]
# here put what you want the encrypted blob to be named
new_blob_name = ["name_for_your_serverside_encrypted_blob_upload"]
