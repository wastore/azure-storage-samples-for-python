import os
from ClientSideLocalKeyToMicrosoftManagedKey import config as cfg
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient


def main():
    # credential required to access client account
    credential = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID, cfg.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credential)
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    # access your container-- this container must already exist to run this program
    cont_client = bs_client.get_container_client(cfg.cont_name)

    # call to run methods
    download_blob(cfg.blob_name, bs_client, cfg.cont_name)
    upload_blob(cfg.blob_name, bs_client, cfg.cont_name)


class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek):
        self.algorithm = cfg.key_wrap_algorithm
        self.kek = kek
        self.kid = kek

    def wrap_key(self, key):
        if self.algorithm == "example-algorithm":
            return key
        return key

    def unwrap_key(self, key, _):
        if self.algorithm == "example-algorithm":
            return key
        return key

    def get_key_wrap_algorithm(self):
        return self.algorithm

    def get_kid(self):
        return self.kid


def download_blob(filename, blob_service_client, cont_name):
    # download encrypted blob from azure storage
    kek = KeyWrapper(cfg.local_key)
    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    blob_client.key_encryption_key = kek
    print("\nReading blob from Azure Storage...")
    # write encrypted contents of blob to a file
    decrypted_message = open("decryptedcontentfile.txt", "wb+")
    decrypted_message.write(blob_client.download_blob().content_as_bytes())
    decrypted_message.close()


def upload_blob(filename, blob_service_client, cont_name, blob_data):
    # upload decrypted blob back to azure storage and perform server side encryption
    # determine the blob type for upload
    decrypted_message = open("decryptedcontentfile.txt", "r")
    file_content = decrypted_message.read()
    decrypted_message.close()

    # determine the blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    blobtype = properties.blob_type

    # upload and use server side encryption with Microsoft managed key through encryption scope
    print("\nPerforming server side encryption with Microsoft Managed Key Encryption Scope...")
    # access specific container and blob
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=cfg.migrated_blob_name)
    # upload and perform server side encryption with Microsoft managed encryption scope
    blob_client.upload_blob(file_content, encryption_scope=cfg.serverside_managed_encryption_scope, blob_type=blobtype, overwrite=True)

    print("\nBlob uploaded to Azure Storage Account.")

    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
