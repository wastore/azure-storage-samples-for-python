import os
from localKeyClientSideToCustomerProvideddServerSide.setup import config as cfg
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from cryptography.fernet import Fernet


def get_blob(filename, blob_service_client, cont_name):
    # download encrypted blob from azure storage
    # access specific container and blob to download from using blob client
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    print("\nReading blob from Azure Storage...")
    # write encrypted contents of blob to a file
    blob_content = blob_client.download_blob().readall()

    return blob_content


def get_local_key():
    # get client side encryption key by path and return it
    local_key = cfg.local_key

    return local_key


def decryption(my_key, encrypted_data):
    # a method to decrypt client side encryption
    print("\nDecrypting client side encryption...")
    # REPLACE THIS PART WITH YOU DECRYPTION METHOD
    # access key for decryption
    f = Fernet(my_key)
    # decrypt encrypted data
    decrypted_data = f.decrypt(encrypted_data)

    # return decrypted content in bytes
    return decrypted_data


def upload_blob(filename, blob_service_client, cont_name, blob_data):
    # upload decrypted blob back to azure storage and perform server side encryption
    # determine the blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    blobtype = properties.blob_type

    # upload and use server side encryption with customer provided key
    customer_key_blob = cfg.new_blob_name
    print("\nPerforming server side encryption with customer provided key...")
    # access specific container and blob
    blob_client = bs_client.get_blob_client(container=cont_name, blob=customer_key_blob)
    # upload and perform server side encryption with Microsoft managed encryption scope
    blob_client.upload_blob(data, cpk=cfg.customer_key, blob_type=blobtype)

    print("\nBlob uploaded to Azure Storage Account.")


if __name__ == '__main__':
    # credential required to access client account
    credential = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID, cfg.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credential)
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    # access your container-- this container must already exist to run this program
    cont_client = bs_client.get_container_client(cfg.cont_name)

    # call to run methods
    content = get_blob(cfg.file, bs_client, cfg.cont_name)
    key = get_local_key()
    data = decryption(key, content)
    upload_blob(cfg.file, bs_client, cfg.cont_name, data)
