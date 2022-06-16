
import base64

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient, KeyVaultKey, KeyType
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

from key_wrapper import KeyWrapper
from settings import *


def main():
    # For more information on the usage of DefaultAzureCredential, see
    # https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential
    credentials = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    key_client = KeyClient(vault_url=KEYVAULT_URL, credential=credentials)
    secret_client = SecretClient(vault_url=KEYVAULT_URL, credential=credentials)

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Create container if it doesn't exist
    try:
        blob_service_client.create_container(CONTAINER_NAME)
    except:
        pass

    # Fetch the encryption key from KeyVault
    key_vault_key = get_keyvault_key(key_client, secret_client)

    # Upload 5 blobs into the container
    for i in range(5):
        blob_name = f'sample-blob-{i}'
        blob_content = b'This is sample content to be encrypted.'

        upload_blob(blob_content, blob_service_client, CONTAINER_NAME, blob_name, key_vault_key, credentials)


def get_keyvault_key(key_client: KeyClient, secret_client: SecretClient) -> KeyVaultKey:
    # If using RSA algorithm, get asymmetric key
    if "RSA" in KEY_WRAP_ALGORITHM:
        keyvault_key = key_client.get_key(CLIENT_SIDE_KEYNAME)

    # If using AES algorithm, get symmetric key
    else:
        secret = secret_client.get_secret(KEYVAULT_SECRET)
        key_bytes = base64.urlsafe_b64decode(secret.value)
        keyvault_key = KeyVaultKey(key_id=secret.id, key_ops=["unwrapKey", "wrapKey"], k=key_bytes, kty=KeyType.oct)

    return keyvault_key


def upload_blob(
        data: bytes,
        blob_service_client: BlobServiceClient,
        container_name: str,
        blob_name: str,
        key_vault_key: KeyVaultKey,
        credential: DefaultAzureCredential) -> None:

    # Create key encryption key using KeyWrapper()
    kek = KeyWrapper(key_vault_key, credential)

    # Access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.require_encryption = True
    blob_client.key_encryption_key = kek
    blob_client.encryption_version = '1.0'

    print(f"Uploading blob {blob_name} to Azure Storage...")

    # Upload blob to container
    blob_client.upload_blob(data, overwrite=OVERWRITE_EXISTING)


if __name__ == "__main__":
    main()
