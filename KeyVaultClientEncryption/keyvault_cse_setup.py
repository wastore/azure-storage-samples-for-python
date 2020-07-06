###############################################
# this is an example of how a user can do     #
# client side encryption using Azure KeyVault #
# variables that need to be updated are       #
# keyname in the make_key function,           #
# all environmental variables, container      #
# name and blob name                          #
###############################################

import os
import sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# environmental variables
KEYVAULT_URL = os.getenv('AZURE_KEYVAULT_DNS_NAME')
CLIENT_ID = os.getenv('ACTIVE_DIRECTORY_APPLICATION_ID')
CLIENT_SECRET = os.getenv('ACTIVE_DIRECTORY_APPLICATION_SECRET')
TENANT_ID = os.getenv('ACTIVE_DIRECTORY_TENANT_ID')


def make_key(key_client):
    # creates an rsa key by name and saves key to keyvault
    rsa_key = key_client.create_rsa_key("testkey1", size=2048)  # replace with your keyname
    keyname = rsa_key.name
    # return keyvault keyname
    return keyname


def get_key(key_client, keyname):
    # retrieves key from keyvault by name provided in make_key()
    key = key_client.get_key(keyname)
    # return keyvault key content
    return key


def encrypt_blob(key, credential):
    # encrypts blob in bytes using keyvault key from get_key() and credentials from environemental variables
    message = b"test file message keyvault"
    # use credentials and keyvault key to access a client account for encryption
    crypto_client = CryptographyClient(key, credential=credential)
    encrypted = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, message)
    # convert to ciphertext to show the encrypted message
    content = encrypted.ciphertext
    # return encrypted content in bytes
    return content


def upload_blob(content, bs_client, cont_name, blob_name):
    # upload content as blob to azure storage
    print("\nUploading to azure as blob...")
    # access blob client, access referenced container under referenced blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=blob_name)
    # upload to azure storage in container and blob references assigned above
    blob_client.upload_blob(content)


if __name__ == "__main__":
    # credential required to access client account
    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    # access keyvault client using credentials and reference to client keyvault
    key_client = KeyClient(vault_url=KEYVAULT_URL, credential=credential)
    # set connection string as environmental variable from Azure storage account
    connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # access blob service client using connection string as reference
    bs_client = BlobServiceClient.from_connection_string(connection_str)
    # set container and blob names
    cont_name = "keyvaultcsetests"
    blob_name = "keyvaulttest2.txt"

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
