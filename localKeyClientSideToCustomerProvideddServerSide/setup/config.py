from azure.storage.blob import CustomerProvidedEncryptionKey

KEYVAULT_URL = ["your_keyvault_url"]
CLIENT_ID = ["your_client_id"]
CLIENT_SECRET = ["your_client_id"]
TENANT_ID = ["your_tenant_id"]
connection_str = ["your_azure_storage_account_connection_str"]

# items to make encryption scope
SUB_ID = ["your_subscription_id"]
RESOURCE_GROUP = ["your_resource_group_name"]
STORAGE_ACCOUNT = ["your_storage_account_name"]

# customer provided key for server side encryption
customer_key = CustomerProvidedEncryptionKey(key_value=["your_key_value"],

                                            key_hash=["your_key_hash"])
cont_name = ["your_blob_container_name"]
file = ["your_file_name.txt"]
local_key = ["your_client_side_encryption_key_value"]
# here put what you want the encrypted blob to be named
new_blob_name = ["name_for_your_serverside_encrypted_blob_upload"]
