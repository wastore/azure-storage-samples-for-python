from ClientSideLocalKeyToCustomerManagedKey import config as cfg
from azure.storage.blob import BlobServiceClient
import os


def main():
    # use connection string to access client account
    bs_client = BlobServiceClient.from_connection_string(cfg.CONNECTION_STRING)

    # call to run methods
    download_blob(cfg.BLOB_NAME, bs_client, cfg.CONTAINER_NAME)
    upload_blob(cfg.BLOB_NAME, bs_client, cfg.CONTAINER_NAME)


class KeyWrapper:
    # key wrap algorithm for kek

    def __init__(self, kek):
        self.algorithm = cfg.KEY_WRAP_ALGORITHM
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
    kek = KeyWrapper(cfg.LOCAL_KEY_VALUE)
    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    blob_client.key_encryption_key = kek
    print("\nReading blob from Azure Storage...")
    # write encrypted contents of blob to a file
    with open("decryptedcontentfile.txt", "wb+") as stream:
        blob_client.download_blob().readinto(stream)


def upload_blob(filename, blob_service_client, cont_name):
    # upload decrypted blob back to azure storage and perform server side encryption

    # determine the blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=filename)
    properties = blob_client.get_blob_properties()
    blobtype = properties.blob_type

    # upload and use server side encryption with Microsoft managed key through encryption scope
    print("\nPerforming server side encryption with Microsoft Managed Key Encryption Scope...")
    # access specific container and blob
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=cfg.MIGRATED_BLOB_NAME)
    # upload and perform server side encryption with Microsoft managed encryption scope
    with open("decryptedcontentfile.txt", "rb") as stream:
        blob_client.upload_blob(stream, encryption_scope=cfg.CUSTOMER_MANAGED_ENCRYPTION_SCOPE, blob_type=blobtype,
                                overwrite=cfg.OVERWRITER)

    print("\nBlob uploaded to Azure Storage Account.")

    os.remove("decryptedcontentfile.txt")


if __name__ == '__main__':
    main()
