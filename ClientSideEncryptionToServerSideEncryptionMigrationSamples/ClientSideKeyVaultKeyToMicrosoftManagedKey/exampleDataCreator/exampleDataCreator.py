import base64
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient, KeyVaultKey, KeyType
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient
from ClientSideEncryptionToServerSideEncryptionMigrationSamples.ClientSideKeyVaultKeyToMicrosoftManagedKey.settings import *
from azure.keyvault.secrets import SecretClient


def main():
    # credential required to access client account
    credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    # access keyvault client using credentials and reference to client keyvault
    # access blob service client using connection string as reference
    bs_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    key_client = KeyClient(vault_url=KEYVAULT_URL, credential=credentials)
    secret_client = SecretClient(vault_url=KEYVAULT_URL, credential=credentials)

    # create or get container
    try:
        cont_client = bs_client.create_container(CONTAINER_NAME)
    except:
        cont_client = bs_client.get_container_client(CONTAINER_NAME)

    # call to methods
    key_vault_key = get_keyvault_key(key_client, secret_client)
    content = get_content(BLOB_NAME)
    upload_blob(BLOB_NAME, content, cont_client, key_vault_key, credentials)


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


def get_keyvault_key(k_client, s_client):
    # if using RSA algorithm, get asymmetric key
    if "RSA" in KEY_WRAP_ALGORITHM:
        keyvault_key = k_client.get_key(CLIENT_SIDE_KEYNAME)
    # if using AES algorithm, get symmetric key
    else:
        secret = s_client.get_secret(KEYVAULT_SECRET)
        key_bytes = base64.urlsafe_b64decode(secret.value)
        keyvault_key = KeyVaultKey(key_id=secret.id, key_ops=["unwrapKey", "wrapKey"], k=key_bytes, kty=KeyType.oct)

    return keyvault_key


def get_content(filename):
    file_content = open(filename, "rb+")
    data = file_content.read()

    return data


def upload_blob(b_name, data, container_client, kvk, credential):
    print("\nEncrypting blob...")
    print("\nUploading to azure as blob...")

    # create key encryption key using KeyWrapper()
    kek = KeyWrapper(kvk, credential)
    container_client.key_encryption_key = kek

    # upload blob to container
    container_client.upload_blob(b_name, data, overwrite=OVERWRITER)


if __name__ == "__main__":
    main()
