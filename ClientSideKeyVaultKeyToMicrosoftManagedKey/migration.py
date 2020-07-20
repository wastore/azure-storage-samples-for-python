import os
import base64
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient, KeyVaultKey, KeyType
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm
from ClientSideKeyVaultKeyToMicrosoftManagedKey.setup import config as cfg
from azure.keyvault.secrets import SecretClient


class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek, credential):
        self.algorithm = KeyWrapAlgorithm.aes_256
        self.kek = kek
        self.kid = kek.id
        self.client = CryptographyClient(kek, credential)

    def wrap_key(self, key):
        if self.algorithm != KeyWrapAlgorithm.aes_256:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        wrapped = self.client.wrap_key(key=key, algorithm=self.algorithm)
        return wrapped.encrypted_key

    def unwrap_key(self, key, _):
        if self.algorithm != KeyWrapAlgorithm.aes_256:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        unwrapped = self.client.unwrap_key(encrypted_key=key, algorithm=self.algorithm)
        return unwrapped.key

    def get_key_wrap_algorithm(self):
        return self.algorithm

    def get_kid(self):
        return self.kid


def get_key_uri():
    # get key uri from keyvault
    e_key = key_client.get_key(cfg.keyname)
    k_uri = str(e_key.id)

    return k_uri


def get_keyvault_key(credential, k_client):
    # if using RSA algorithm, get asymmetric key
    if "RSA" in cfg.key_wrap_algorithm:
        keyvault_key = k_client.get_key(cfg.keyname)
    # if using AES algorithm, get symmetric key
    else:
        secret_client = SecretClient(vault_url=cfg.KEYVAULT_URL, credential=credential)

        secret = secret_client.get_secret(cfg.secret)
        key_bytes = base64.urlsafe_b64decode(secret.value)
        keyvault_key = KeyVaultKey(key_id=secret.id, key_ops=["unwrapKey", "wrapKey"], k=key_bytes, kty=KeyType.oct)

    return keyvault_key


def download_blob(blob_name, container_client):
    print("\nDownloading and decrypting blob...")
    kek = KeyWrapper(kvk, credentials)
    container_client.key_encryption_key = kek
    decrypted_message = container_client.get_blob_client(blob_name).download_blob().content_as_bytes()

    return decrypted_message


def create_encryption_scope(k_uri):
    # makes a customer managed-key encryption scope
    print("\nCreating encryption scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + cfg.STORAGE_ACCOUNT + ' --name ' + cfg.SERVER_SCOPE_NAME + ' --key-source Microsoft.KeyVault --resource-group ' + cfg.RESOURCE_GROUP + ' --subscription ' + cfg.SUB_ID + ' --key-uri ' + k_uri + '"')


def upload_blob(blob_service_client, cont_name, blob_name, my_message):
    print("\nUploading to azure as blob...")

    # determine blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    b_type = properties.blob_type

    # upload using customer managed encryption-scope
    print("\nPerforming server side encryption with customer managed key...")
    # access container and specified blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=cfg.new_blob_name)
    # upload contents to that blob with customer managed key for server side encryption
    blob_client.upload_blob(my_message, encryption_scope=cfg.SERVER_SCOPE_NAME,
                            blob_type=b_type)


if __name__ == "__main__":
    # credential required to access client account
    credentials = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID,
                                         cfg.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credentials)
    # access blob client with connection string
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    # access container by name-- required that container already exists
    cont_client = bs_client.get_container_client(cfg.cont_name)

    # call to methods
    key_uri = get_key_uri()
    kvk = get_keyvault_key(credentials, key_client)
    message = download_blob(cfg.blob_name, cont_client)
    create_encryption_scope(key_uri)
    upload_blob(bs_client, cfg.cont_name, cfg.blob_name, message)
