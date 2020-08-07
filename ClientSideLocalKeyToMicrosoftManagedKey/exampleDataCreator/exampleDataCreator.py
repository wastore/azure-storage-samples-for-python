import os
from azure.storage.blob import BlobServiceClient
from ClientSideLocalKeyToMicrosoftManagedKey import config as cfg


def main():
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(cfg.CONNECTION_STRING)

    # create container by name
    try:
        bs_client.create_container(cfg.CONTAINER_NAME)
    except:
        bs_client.get_container_client(cfg.CONTAINER_NAME)

    # call to methods
    create_encryption_scope()
    content = get_content(cfg.BLOB_NAME)
    upload_blob(content, bs_client, cfg.CONTAINER_NAME, cfg.BLOB_NAME)


class KeyWrapper:
    # REPLACE WITH YOUR PREFERRED KEYWRAPPING ALGORITHMS AND METHODS

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


def create_encryption_scope():
    print("\nCreating Microsoft Managed Key Encryption Scope...\n")
    os.system(
        'cmd /c "az storage account encryption-scope create --account-name ' + cfg.STORAGE_ACCOUNT + ' --name ' + cfg.SERVER_MANAGED_ENCRYPTION_SCOPE + ' --key-source Microsoft.KeyVault --resource-group ' + cfg.RESOURCE_GROUP + ' --subscription ' + cfg.SUBSCRIPTION_ID + '"')


def get_content(filename):
    file_content = open(filename, "rb+")
    data = file_content.read()

    return data


def upload_blob(data, blob_service_client, container_name, b_name):
    # upload encrypted content to Azure storage
    kek = KeyWrapper(cfg.LOCAL_KEY_VALUE)

    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=b_name)
    blob_client.key_encryption_key = kek

    print("\nUploading blob to Azure Storage...")
    print("\nEncrypting blob on server...")

    blob_client.upload_blob(data, overwrite=cfg.OVERWRITER)


if __name__ == "__main__":
    main()
