from azure.storage.blob import CustomerProvidedEncryptionKey
from azure.keyvault.keys.crypto import KeyWrapAlgorithm

# the below values are fake and need to be replaced

KEYVAULT_URL = "https://caromekeyvault.vault.azure.net/"
CLIENT_ID = "321522b8-e1b7-4866-8767-ef10dcc25d65"
CLIENT_SECRET = "ub-L_eR_-0nUoV0p8Uv.UZV~393dIhpL7g"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
connection_str = "DefaultEndpointsProtocol=https;AccountName=caromedevtest;AccountKey=ZFeoXH1cvuTpPCg4UYeQqZ0GEB9rK4QZhi8D0dyH7WEpb78BvtZ7xKBGbv85l3/yPMFC7NcPww1YrtT6be0OkQ==;EndpointSuffix=core.windows.net"

# items to make encryption scope
SUB_ID = "ba45b233-e2ef-4169-8808-49eb0d8eba0d"
RESOURCE_GROUP = "carmen_romero"
STORAGE_ACCOUNT = "caromedevtest"

# if using customer provided key, set values here
customer_key = CustomerProvidedEncryptionKey(key_value="MDEyMzQ1NjcwMTIzNDU2NzAxMjM0NTY3MDEyMzQ1Njc=",
                                             key_hash="3QFFFpRA5+XANHqwwbT4yXDmrT/2JaLt/FKHjzhOdoE=")

# keyvault key used for encryption
keyname = "migration-testkey"
secret = "sample-secret"
key_wrap_algorithm = KeyWrapAlgorithm.rsa_oaep #.rsa_oaep, .rsa_oaep_256, .rsa1_5, .aes_256

cont_name = "client-side-keyvault-key-to-customer-provided-key"
blob_name = "blobExample.txt"
new_blob_name = "new" + blob_name