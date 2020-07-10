from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from keyVaultClientSideToCustomerManagedServerSide.setup import config as cfg


def make_key(k_client):
    # creates an rsa key by name and saves key to keyvault
    rsa_key = k_client.create_rsa_key(cfg.keyname, size=2048)  # replace with your keyname
    k_name = rsa_key.name
    # return keyvault keyname
    return k_name


def get_key(k_client, k_name):
    # retrieves key from keyvault by name provided in make_key()
    keyvault_key = k_client.get_key(k_name)
    # return keyvault key content
    return keyvault_key


def encrypt_blob(keyvault_key, my_credential):
    # encrypts blob in bytes using keyvault key from get_key() and credentials from environmental variables
    message = b"customer managed test"
    # use credentials and keyvault key to access a client account for encryption
    crypto_client = CryptographyClient(keyvault_key, credential=my_credential)
    encrypted = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, message)
    # convert to ciphertext to show the encrypted message
    encrypted_content = encrypted.ciphertext
    # return encrypted content in bytes
    return encrypted_content


def upload_blob(encrypted_content, blob_service_client, container_name, b_name):
    # upload content as blob to azure storage
    print("\nUploading to azure as blob...")
    # access blob client, access referenced container under referenced blob name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=b_name)
    # upload to azure storage in container and blob references assigned above
    blob_client.upload_blob(encrypted_content)


if __name__ == "__main__":
    # credential required to access client account
    credential = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID, cfg.CLIENT_SECRET)
    # access keyvault client using credentials and reference to client keyvault
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credential)
    # access blob service client using connection string as reference
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    # set container and blob names
    cont_name = cfg.cont_name
    blob_name = cfg.blob_name

    # create new container if container doesn't exist
    # if container exists, access that container
    try:
        cont_client = bs_client.create_container(cont_name)
    except:
        cont_client = bs_client.get_container_client(cont_name)

    # call to methods
    keyname = make_key(key_client)  # only use if no key exists, or if you want to create a new version of a key
    key = get_key(key_client, keyname)
    content = encrypt_blob(key, credential)
    upload_blob(content, bs_client, cont_name, blob_name)
