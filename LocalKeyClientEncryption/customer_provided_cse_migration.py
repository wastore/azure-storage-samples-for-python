################################################################
# this application goes through the process of migration from   #
# private client side encryption to server side encryption     #
# this application includes three types of server side         #
# encryption: Microsoft managed keys through encryption        #
# scope, customer managed keys through encryption scope,       #
# and customer provided keys. This application requires that   #
# environmental variables, keys, and encryption scopes are set,#
# as well as private encryption keys, container, and blob names#
################################################################
import os
import uuid
import privateConfig
from PIL import Image
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerEncryptionScope, \
    CustomerProvidedEncryptionKey
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from cryptography.fernet import Fernet  # python extension for decryption


def download_blob(filename, bs_client, cont_name):
    # download encrypted blob from azure storage
    # access specific container and blob to download from using blob client
    blob_client = bs_client.get_blob_client(container=cont_name, blob=filename)
    print("\nDownloading blob from Azure storage...")
    # write encrypted contents of blob to a file
    with open(filename, "wb+") as download_file:
        download_file.write(blob_client.download_blob().readall())

def make_key(key_client):
    # this method creates a keyvault key to make a customer managed-key encryption scope for server side encryption
    # creates an rsa key by name and saves key to keyvault
    rsa_key = key_client.create_rsa_key(privateConfig.keyvault_keyname, size=2048)
    keyname = rsa_key.name
    # grab keyvault key
    keyvault_key = key_client.get_key(keyname)
    # get key_uri for encryption scope
    key_uri = str(keyvault_key.id)
    return key_uri

def get_key():
    # get client side encryption key by name and return it
    return open("privatekey1.key", "rb").read()


def cse_decrypt(filename, key):
    # REPLACE THIS WITH YOUR DECRYPTION ALGORITHM
    print("\nDecrypting client side encryption...")
    # access key for decryption
    f = Fernet(key)
    # read encrypted data
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    # decrypt encrypted data
    decrypted_data = f.decrypt(encrypted_data)
    # write decrypted data to a file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    # return decrypted data content
    return decrypted_data


def encryption_scope(key_uri):
    # DOES NOT CURRENTLY INCLUDE makes a customer managed-key encryption scope
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + privateConfig.STORAGE_ACCOUNT + ' --name ' + privateConfig.CUSTOMER_SCOPE_NAME + ' --key-source Microsoft.KeyVault --resource-group ' + privateConfig.RESOURCE_GROUP + ' --subscription ' + privateConfig.SUB_ID + ' --key-uri ' + key_uri + '"')
    # makes a Microsoft managed-key encryption scope
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + privateConfig.STORAGE_ACCOUNT + ' --name ' + privateConfig.SERVER_SCOPE_NAME + ' --key-source Microsoft.Storage --resource-group ' + privateConfig.RESOURCE_GROUP + ' --subscription ' + privateConfig.SUB_ID + '"')


def upload_blob(filename, bs_client, cont_name, data):
    # upload decrypted blob back to azure storage and perform server side encryption
    # determine the blob type for upload
    blob_client = bs_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    type = properties.blob_type

    # upload and use server side encryption with customer managed key through encryption scope
    customer_scope_blob = "customer-key-" + filename
    print("\nUploading to azure as blob...")
    print("\nPerforming server side encryption with customer managed key...")
    # access specific container and blob
    blob_client = bs_client.get_blob_client(container=cont_name, blob=customer_scope_blob)
    # upload and perform server side encryption with customer managed encryption scope
    blob_client.upload_blob(data, encryption_scope=privateConfig.CUSTOMER_SCOPE_NAME, blob_type=type)

    # upload and use server side encryption with Microsoft managed key through encryption scope
    server_scope_blob = "server-key-" + filename
    print("\nPerforming server side encryption with Microsoft managed key...")
    # access specific container and blob
    blob_client = bs_client.get_blob_client(container=cont_name, blob=server_scope_blob)
    # upload and perform server side encryption with Microsoft managed encryption scope
    blob_client.upload_blob(data, encryption_scope=privateConfig.SERVER_SCOPE_NAME, blob_type=type)

    # upload and use server side encryption with customer provided key
    customer_key_blob = "customer-provided-" + filename
    print("\nPerforming server side encryption with customer provided key...")
    # access specific container and blob
    blob_client = bs_client.get_blob_client(container=cont_name, blob=customer_key_blob)
    # upload and perform server side encryption with Microsoft managed encryption scope
    blob_client.upload_blob(data, cpk=privateConfig.customer_key, blob_type=type)


if __name__ == '__main__':
    # credential required to access client account
    credential = ClientSecretCredential(privateConfig.TENANT_ID, privateConfig.CLIENT_ID, privateConfig.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=privateConfig.KEYVAULT_URL, credential=credential)
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(privateConfig.connection_str)
    # access your container-- this container must already exist to run this program
    cont_client = bs_client.get_container_client(privateConfig.cont_name)

    # call to run methods
    download_blob(privateConfig.file, bs_client, privateConfig.cont_name)
    key_uri = make_key(key_client)
    key = get_key()
    data = cse_decrypt(privateConfig.file, key)
    encryption_scope(key_uri)
    upload_blob(privateConfig.file, bs_client, privateConfig.cont_name, data)
