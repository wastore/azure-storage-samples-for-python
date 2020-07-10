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

# if using customer provided key, set values here
customer_key = CustomerProvidedEncryptionKey(key_value="MDEyMzQ1NjcwMTIzNDU2NzAxMjM0NTY3MDEyMzQ1Njc=",
                                             key_hash="3QFFFpRA5+XANHqwwbT4yXDmrT/2JaLt/FKHjzhOdoE=")

# keyvault key used for encryption
keyname = ["keyvault_key_for_serverside_encryption_name"]

cont_name = ["your_blob_container_name"]
blob_name = ["your_blob_name.txt"]
new_blob_name = ["name_for_your_serverside_encrypted_blob"]