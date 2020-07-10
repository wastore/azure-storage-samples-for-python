import os
from keyVaultClientSideToCustomerProvidedServerSide.setup import config as cfg
from azure.storage.blob import BlobServiceClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def get_key(k_client, k_name):
    # get key from keyvault
    encryption_key = k_client.get_key(k_name)

    # return keyvault key
    return encryption_key


def get_blob(blob_service_client, cont_name, blob_name):
    # get blob contents and return in bytes
    print("Reading blob from Azure Storage...\n")
    # access specific container and blob using blob client that you want to download from
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=blob_name)
    # write contents from blob into a file as bytes and download
    blob_content = blob_client.download_blob().readall()

    # return contents from file in bytes
    return blob_content


def decrypt_blob(encryption_key, my_credential, encrypted_content):
    # decrypt blob-- requires data in form of bytes
    print("Decrypting blob...")
    # use keyvault key and credential to access account client for decryption
    crypto_client = CryptographyClient(encryption_key, credential=my_credential)
    # decrypt content
    decrypted = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_content)
    # convert decrypted content to plaintext to make it readable
    decrypted_message = decrypted.plaintext

    # return decrypted content
    return decrypted_message


def reupload_blob(blob_service_client, cont_name, blob_name, encrypted_message):
    print("\nUploading to azure as blob...")

    # determine blob type for upload
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    b_type = properties.blob_type

    # upload using customer provided key
    print("\nPerforming server side encryption with customer provided key...")
    customer_key_blob = cfg.new_blob_name
    # access container and specified blob name
    blob_client = blob_service_client.get_blob_client(container=cont_name, blob=customer_key_blob)
    # upload contents to that blob with customer provided key for server side encryption
    blob_client.upload_blob(message, cpk=cfg.customer_key,
                            blob_type=b_type)


if __name__ == "__main__":
    # credential required to access client account
    credential = ClientSecretCredential(cfg.TENANT_ID, cfg.CLIENT_ID,
                                        cfg.CLIENT_SECRET)
    # access keyvault key client using keyvault url and credentials
    key_client = KeyClient(vault_url=cfg.KEYVAULT_URL, credential=credential)
    # access blob client with connection string
    bs_client = BlobServiceClient.from_connection_string(cfg.connection_str)
    # access container by name-- required that container already exists
    cont_client = bs_client.get_container_client(cfg.cont_name)

    # call to methods
    key = get_key(key_client, cfg.keyname)
    content = get_blob(bs_client, cfg.cont_name, cfg.blob_name)
    message = decrypt_blob(key, credential, content)
    reupload_blob(bs_client, cfg.cont_name, cfg.blob_name, message)
