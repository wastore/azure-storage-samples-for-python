from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet
from ClientSideLocalKeyToCustomerManagedKey.setup import config as cfg


def make_key():
    # creates a key using a python extension for encryption
    key = Fernet.generate_key()
    # writing key content to a file
    with open(cfg.local_key_name, "wb") as key_file:  # set keyname here
        key_file.write(key)

    return open(cfg.local_key_name, "rb").read()


def get_content(filename):
    file_content = open(filename, "rb+")
    data = file_content.read()

    return data


def encrypt(encryption_key, data):
    # perform encryption using python extension
    print("Client side encrypting...")
    # use key to encrypt
    f = Fernet(encryption_key)
    # encrypt content with extension
    encrypted_content = f.encrypt(data)

    return encrypted_content


def upload_blob(my_data, blob_service_client, container_name, b_name):
    # upload encrypted content to Azure storage

    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=b_name)
    print("\nUploading blob to Azure Storage...")
    print("\nEncrypting blob on server...")

    blob_client.upload_blob(my_data)


if __name__ == "__main__":
    # set connection string environmental variable
    connection_str = cfg.connection_str
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(connection_str)
    # set container name
    cont_name = cfg.cont_name
    blob_name = cfg.blob_name

    # create container by name
    try:
        cont_client = bs_client.create_container(cont_name)
    except:
        cont_client = bs_client.get_container_client(cont_name)

    # call to methods
    my_key = make_key()
    content = get_content(blob_name)
    encrypted_data = encrypt(my_key, content)
    upload_blob(encrypted_data, bs_client, cont_name, blob_name)
