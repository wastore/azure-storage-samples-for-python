import os
from localKeyClientSideToMicrosoftManagedServerSide.setup import config as cfg
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from cryptography.fernet import Fernet


def download_blob(filename, blob_service_client, cont_name):
    # download encrypted blob from azure storage
    # access specific container and blob to download from using blob client
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    print("\nDownloading blob from Azure Storage...")
    # write encrypted contents of blob to a file
    with open(filename, "wb+") as download_file:
        download_file.write(blob_client.download_blob().readall())


def get_local_key():
    # get client side encryption key by name and return it
    return open(cfg.local_key_path, "rb").read()


def cse_decrypt(filename, mykey):
    # REPLACE THIS WITH YOUR DECRYPTION ALGORITHM
    print("\nDecrypting client side encryption...")
    # access key for decryption
    f = Fernet(mykey)
    # read encrypted data
    with open(filename, "rb") as fn:
        encrypted_data = fn.read()
    # decrypt encrypted data
    decrypted_data = f.decrypt(encrypted_data)
    # write decrypted data to a file
    with open(filename, "wb") as fn:
        fn.write(decrypted_data)
    # return decrypted data content
    return decrypted_data


def encryption_scope():
    # makes a Microsoft managed-key encryption scope
    print("\nCreating Microsoft Managed Key Encryption Scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + cfg.STORAGE_ACCOUNT + ' --name ' + cfg.SERVER_SCOPE_NAME + ' --key-source Microsoft.Storage --resource-group ' + cfg.RESOURCE_GROUP + ' --subscription ' + cfg.SUB_ID + '"')


def upload_blob(filename, blob_service_client, cont_name, mydata):
    # upload decrypted blob back to azure storage and perform server side encryption
    # determine the blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    blobtype = properties.blob_type

    # upload and use server side encryption with Microsoft managed key through encryption scope
    server_scope_blob = cfg.new_blob_name
    print("\nPerforming server side encryption with Microsoft Managed Key Encryption Scope...")
    # access specific container and blob
    blob_client = bs_client.get_blob_client(container=cont_name, blob=server_scope_blob)
    # upload and perform server side encryption with Microsoft managed encryption scope
    blob_client.upload_blob(mydata, encryption_scope=cfg.SERVER_SCOPE_NAME, blob_type=blobtype)


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
    download_blob(cfg.file, bs_client, cfg.cont_name)
    key = get_local_key()
    data = cse_decrypt(cfg.file, key)
    encryption_scope()
    upload_blob(cfg.file, bs_client, cfg.cont_name, data)
