#######################################################
# this is an example file of how a user would encrypt #
# privately using client side encryption              #
# this program requires that the connection string    #
# environmental variable, container name, existing    #
# file name, and key name are all set.                #
#######################################################
import os
import uuid
from PIL import Image
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
# python extension used for encryption
from cryptography.fernet import Fernet


def make_key():
    # creates a key using a python extension for encryption
    key = Fernet.generate_key()
    # writing key content to a file
    with open("privatekey1.key", "wb") as key_file:  # set keyname here
        key_file.write(key)


def get_key():
    # access file with key contents and return those contents
    return open("privatekey1.key", "rb").read()


def encrypt(filename, key):
    # perform encryption using python extension
    print("Client side encrypting...")
    # use key to encrypt
    f = Fernet(key)
    # read content from file
    with open(filename, "rb") as file:
        file_data = file.read()
    # encrypt content with extension
    encrypted_data = f.encrypt(file_data)
    # write encrypted content to file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def upload_blob(filename, bs_client, cont_client, cont_name):
    # upload encrypted content to Azure storage
    # imgFile = Image.open(filename)
    # access file with encrypted content
    file = open(filename, "r")
    file.close()

    # access specific container and blob with blob client
    blob_client = bs_client.get_blob_client(container=cont_name, blob=filename)
    print("\nUploading to azure as blob: " + filename)
    print("\nEncrypting blob on server...")

    # upload encrypted data to specified blob
    with open(filename, "rb") as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    # set connection string environmental variable
    connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(connection_str)
    # set container name
    cont_name = "privatecsetests"

    # create container by name if none exists
    # if container exists, access that container
    try:
        cont_client = bs_client.create_container(cont_name)
    except:
        cont_client = bs_client.get_container_client(cont_name)

    # call to methods
    make_key()
    key = get_key()
    file = "privatecsetest1.txt"
    encrypt(file, key)
    upload_blob(file, bs_client, cont_client, cont_name)
