from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet


def make_key():
    # creates a key using a python extension for encryption
    key = Fernet.generate_key()
    # writing key content to a file
    with open("localkey.key", "wb") as key_file:  # set keyname here
        key_file.write(key)


def get_key():
    # access file with key contents and return those contents
    return open("localkey.key", "rb").read()


def encrypt(encryption_key, my_message):
    # perform encryption using python extension
    print("Client side encrypting...")
    # use key to encrypt
    f = Fernet(encryption_key)
    # encrypt content with extension
    encrypted_data = f.encrypt(my_message)

    return encrypted_data


def upload_blob(my_data, blob_service_client, container_name, bname):
    # upload encrypted content to Azure storage

    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=bname)
    print("\nUploading blob to Azure Storage...")
    print("\nEncrypting blob on server...")

    blob_client.upload_blob(my_data)


if __name__ == "__main__":
    # set connection string environmental variable
    connection_str = "DefaultEndpointsProtocol=https;AccountName=caromedevtest;AccountKey=/IaVQtMqKb0qO1C" \
                     "/miYYAHbyjIla/O3f1kXxMhksgCfa/KDDcdkd1x2iaFGu4tFY3LlR4xYNXMLFrlQOhWZpig==;EndpointSuffix=core" \
                     ".windows.net"
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(connection_str)
    # set container name
    cont_name = "privatecsetests"
    message = b"customer managed test"

    # create container by name
    try:
        cont_client = bs_client.create_container(cont_name)
    except:
        con_client = bs_client.get_container_client(cont_name)

    # call to methods
    make_key()
    mykey = get_key()
    blob_name = "cm-localtest.txt"
    data = encrypt(mykey, message)
    upload_blob(data, bs_client, cont_name, blob_name)
