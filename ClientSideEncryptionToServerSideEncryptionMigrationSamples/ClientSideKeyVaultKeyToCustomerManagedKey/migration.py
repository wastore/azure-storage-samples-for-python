import base64
import os
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient, KeyVaultKey, KeyType
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient
from ClientSideEncryptionToServerSideEncryptionMigrationSamples.ClientSideKeyVaultKeyToCustomerManagedKey.settings import *
from azure.keyvault.secrets import SecretClient


def main():
    # credential required to access client account
    credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID,
                                         CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=KEYVAULT_URL, credential=credentials)
    # access blob client with connection string
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    # access container by name-- required that container already exists
    cont_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # create encryption scope
    if CREATE_ENCRYPTION_SCOPE:
        key_uri = get_key_uri(key_client)
        create_encryption_scope(key_uri)

    # call to methods
    key_vault_key = get_keyvault_key(credentials, key_client)
    download_blob(BLOB_NAME, cont_client, key_vault_key, credentials)
    upload_blob(blob_service_client, CONTAINER_NAME, BLOB_NAME)


class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek, credential):
        self.algorithm = KEY_WRAP_ALGORITHM
        self.kek = kek
        self.kid = kek.id
        self.client = CryptographyClient(kek, credential)

    def wrap_key(self, key):
        if self.algorithm != KEY_WRAP_ALGORITHM:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        wrapped = self.client.wrap_key(key=key, algorithm=self.algorithm)
        return wrapped.encrypted_key

    def unwrap_key(self, key, _):
        if self.algorithm != KEY_WRAP_ALGORITHM:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        unwrapped = self.client.unwrap_key(encrypted_key=key, algorithm=self.algorithm)
        return unwrapped.key

    def get_key_wrap_algorithm(self):
        return self.algorithm

    def get_kid(self):
        return self.kid


def get_key_uri(k_client):
    # get key uri from keyvault
    e_key = k_client.get_key(SERVER_SIDE_KEYNAME)
    k_uri = str(e_key.id)

    return k_uri


def create_encryption_scope(k_uri):
    # makes a customer managed-key encryption scope
    print("\nCreating encryption scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + STORAGE_ACCOUNT + ' --name ' + CUSTOMER_MANAGED_ENCRYPTION_SCOPE + ' --key-source Microsoft.KeyVault --resource-group ' + RESOURCE_GROUP + ' --subscription ' + SUBSCRIPTION_ID + ' --key-uri ' + k_uri + '"')


def get_keyvault_key(credential, k_client):
    # if using RSA algorithm, get asymmetric key
    if "RSA" in KEY_WRAP_ALGORITHM:
        keyvault_decryption_key = k_client.get_key(CLIENT_SIDE_KEYNAME)
    # if using AES algorithm, get symmetric key
    else:
        secret_client = SecretClient(vault_url=KEYVAULT_URL, credential=credential)

        secret = secret_client.get_secret(KEYVAULT_SECRET)
        key_bytes = base64.urlsafe_b64decode(secret.value)
        keyvault_decryption_key = KeyVaultKey(key_id=secret.id, key_ops=["unwrapKey", "wrapKey"], k=key_bytes, kty=KeyType.oct)

    return keyvault_decryption_key


def download_blob(blob_name, container_client, kvk, credential):
    print("\nDownloading and decrypting blob...")
    kek = KeyWrapper(kvk, credential)
    container_client.key_encryption_key = kek
    with open("decryptedcontentfile.txt", "wb+") as stream:
        container_client.get_blob_client(blob_name).download_blob().readinto(stream)


def upload_blob(bs_client, cont_name, blob_name):
    print("\nUploading to azure as blob...")

    # determine blob type for upload
    blob_client = bs_client.get_blob_client(container=cont_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    b_type = properties.blob_type

    # upload using customer managed encryption-scope
    print("\nPerforming server side encryption with customer managed key...")
    # access container and specified blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=MIGRATED_BLOB_NAME)
    # upload contents to that blob with customer managed key for server side encryption
    with open("decryptedcontentfile.txt", "rb") as stream:
        blob_client.upload_blob(stream, encryption_scope=CUSTOMER_MANAGED_ENCRYPTION_SCOPE,
                                blob_type=b_type, overwrite=OVERWRITER)

    os.remove("decryptedcontentfile.txt")


if __name__ == "__main__":
    main()
