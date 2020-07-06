#################################################################
# this is an example of the migration process                   #
# from client side to server side encryption                    #
# using Azure KeyVault, including three methods                 #
# of server side encryption                                     #
#################################################################

import os
import sys
import keyvaultConfig
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerEncryptionScope, \
    CustomerProvidedEncryptionKey, BlobType, BlobProperties
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def get_key(key_client, keyname):
    # get key from keyvault using name of the key
    # this key must already exist in keyvault
    key = key_client.get_key(keyname)
    # return keyvault key
    return key


def download_blob(bs_client, cont_name, blob_name):
    # download blob and contents of blob-- return contents in bytes
    print("Downloading blob from azure...\n")
    # access specific container and blob using blob client that you want to download from
    blob_client = bs_client.get_blob_client(container=cont_name, blob=blob_name)
    # write contents from blob into a file as bytes and download
    with open(blob_name, "wb+") as download_file:
        download_file.write(blob_client.download_blob().readall())
    # access contents from file and read
    file = open(blob_name, "rb")
    content = file.read()
    file.close()

    # return contents from file in bytes
    return content


def decrypt_blob(key, credential, content, blob_name):
    # decrypt blob-- requires data in form of bytes
    print("Decrypting blob...")
    # use keyvault key and credential to access account client for decryption
    crypto_client = CryptographyClient(key, credential=credential)
    # decrypt content
    decrypted = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, content)
    # convert decrypted content to plaintext to make it readable
    message = decrypted.plaintext

    # write decrypted content to a file
    file = open(blob_name, "wb+")
    file.write(message)
    file.close()

    # return decrypted content
    return message


def encryption_scope(key_uri):
    # makes a customer managed-key encryption scope
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + keyvaultConfig.STORAGE_ACCOUNT + ' --name ' + keyvaultConfig.CUSTOMER_SCOPE_NAME + ' --key-source Microsoft.KeyVault --resource-group ' + keyvaultConfig.RESOURCE_GROUP + ' --subscription ' + keyvaultConfig.SUB_ID + ' --key-uri ' + key_uri + '"')
    # makes a Microsoft managed-key encryption scope
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + keyvaultConfig.STORAGE_ACCOUNT + ' --name ' + keyvaultConfig.SERVER_SCOPE_NAME + ' --key-source Microsoft.Storage --resource-group ' + keyvaultConfig.RESOURCE_GROUP + ' --subscription ' + keyvaultConfig.SUB_ID + '"')


# reupload blob without client side encryption
# this should upload as three different files
# one that utilizes a customer managed key
# with encryption scope, one that uses a
# Microsoft managed key with encryption-scope,
# and one that uses a customer provided key
def reupload_blob(bs_client, cont_name, blob_name, message):
    print("\nUploading to azure as blob...")

    # determine blob type for upload
    blob_client = bs_client.get_blob_client(container=cont_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    type = properties.blob_type

    # upload using customer managed encryption-scope
    print("\nPerforming server side encryption with customer managed key...")
    customer_scope_blob = "customer-managed-" + blob_name
    # access container and specified blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=customer_scope_blob)
    # upload contents to that blob with customer managed key for server side encryption
    blob_client.upload_blob(message, encryption_scope=keyvaultConfig.CUSTOMER_SCOPE_NAME,
                            blob_type=type)

    # upload using Microsoft managed encryption-scope
    print("\nPerforming server side encryption with Microsoft managed key...")
    server_scope_blob = "server-managed-" + blob_name
    # access container and specified blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=server_scope_blob)
    # upload contents to that blob with Microsoft managed key for server side encryption
    blob_client.upload_blob(message, encryption_scope=keyvaultConfig.SERVER_SCOPE_NAME,
                            blob_type=type)

    # upload using customer provided key
    print("\nPerforming server side encryption with customer provided key...")
    customer_key_blob = "customer-provided-" + blob_name
    # access container and specified blob name
    blob_client = bs_client.get_blob_client(container=cont_name, blob=customer_key_blob)
    # upload contents to that blob with customer provided key for server side encryption
    blob_client.upload_blob(message, cpk=keyvaultConfig.customer_key,
                            blob_type=type)


if __name__ == "__main__":
    # credential required to access client account
    credential = ClientSecretCredential(keyvaultConfig.TENANT_ID, keyvaultConfig.CLIENT_ID,
                                        keyvaultConfig.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=keyvaultConfig.KEYVAULT_URL, credential=credential)
    # access blob client with connection string
    bs_client = BlobServiceClient.from_connection_string(keyvaultConfig.connection_str)
    # access container by name-- required that container already exists
    cont_client = bs_client.get_container_client(keyvaultConfig.cont_name)

    # call to methods
    key = get_key(key_client, keyvaultConfig.keyname)
    content = download_blob(bs_client, keyvaultConfig.cont_name, keyvaultConfig.blob_name)
    message = decrypt_blob(key, credential, content, keyvaultConfig.blob_name)
    key_uri = str(key.id)  # get key-uri for encryption scope
    encryption_scope(key_uri)
    reupload_blob(bs_client, keyvaultConfig.cont_name, keyvaultConfig.blob_name, message)
