import base64
import os
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient, KeyVaultKey, KeyType
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient
from ClientSideKeyVaultKeyToCustomerManagedKey import config as cfg
from azure.keyvault.secrets import SecretClient


def main():
    # credential required to access client account
    credentials = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID, cfg.CLIENT_SECRET)
    # access keyvault client using credentials and reference to client keyvault
    # access blob service client using connection string as reference
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credentials)
    secret_client = SecretClient(vault_url=cfg.KEYVAULT_URL, credential=credentials)

    # create or get container
    try:
        cont_client = bs_client.create_container(cfg.cont_name)
    except:
        cont_client = bs_client.get_container_client(cfg.cont_name)

    # call to methods
    key_uri = get_key_uri(key_client)
    create_encryption_scope(key_uri)
    key_vault_key = get_keyvault_key(key_client, secret_client)
    content = get_content(cfg.blob_name)
    upload_blob(cfg.blob_name, content, cont_client, key_vault_key, credentials)


class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek, credential):
        self.algorithm = cfg.key_wrap_algorithm
        self.kek = kek
        self.kid = kek.id
        self.client = CryptographyClient(kek, credential)

    def wrap_key(self, key):
        if self.algorithm != cfg.key_wrap_algorithm:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        wrapped = self.client.wrap_key(key=key, algorithm=self.algorithm)
        return wrapped.encrypted_key

    def unwrap_key(self, key, _):
        if self.algorithm != cfg.key_wrap_algorithm:
            raise ValueError('Unknown key wrap algorithm. {}'.format(self.algorithm))
        unwrapped = self.client.unwrap_key(encrypted_key=key, algorithm=self.algorithm)
        return unwrapped.key

    def get_key_wrap_algorithm(self):
        return self.algorithm

    def get_kid(self):
        return self.kid


def get_key_uri(k_client):
    # get key uri from keyvault
    e_key = k_client.get_key(cfg.serverside_encryption_keyname)
    k_uri = str(e_key.id)

    return k_uri


def create_encryption_scope(k_uri):
    # makes a customer managed-key encryption scope
    print("\nCreating encryption scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + cfg.STORAGE_ACCOUNT + ' --name ' + cfg.customer_managed_encryption_scope + ' --key-source Microsoft.KeyVault --resource-group ' + cfg.RESOURCE_GROUP + ' --subscription ' + cfg.SUB_ID + ' --key-uri ' + k_uri + '"')


def get_keyvault_key(k_client, s_client):
    # if using RSA algorithm, get asymmetric key
    if "RSA" in cfg.key_wrap_algorithm:
        keyvault_key = k_client.get_key(cfg.keyname)
    # if using AES algorithm, get symmetric key
    else:
        secret = s_client.get_secret(cfg.secret)
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
    container_client.upload_blob(b_name, data, overwrite=True)


if __name__ == "__main__":
    main()
