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


def encrypt(filename, encryption_key):
    # perform encryption using python extension
    print("Client side encrypting...")
    # use key to encrypt
    f = Fernet(encryption_key)
    # read content from file
    with open(filename, "rb") as fn:
        file_data = fn.read()
    # encrypt content with extension
    encrypted_data = f.encrypt(file_data)
    # write encrypted content to file
    with open(filename, "wb") as fn:
        fn.write(encrypted_data)


def upload_blob(filename, blob_service_client, container_name):
    # upload encrypted content to Azure storage
    # access file with encrypted content
    fn = open(filename, "r")
    fn.close()

    # access specific container and blob with blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    print("\nUploading to azure as blob: " + filename)
    print("\nEncrypting blob on server...")

    # upload encrypted data to specified blob
    with open(filename, "rb") as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    # set connection string environmental variable
    connection_str = "DefaultEndpointsProtocol=https;AccountName=caromedevtest;AccountKey=/IaVQtMqKb0qO1C" \
                     "/miYYAHbyjIla/O3f1kXxMhksgCfa/KDDcdkd1x2iaFGu4tFY3LlR4xYNXMLFrlQOhWZpig==;EndpointSuffix=core" \
                     ".windows.net"
    # access a container using connection string
    bs_client = BlobServiceClient.from_connection_string(connection_str)
    # set container name
    cont_name = "privatecsetests"

    # create container by name
    try:
        cont_client = bs_client.create_container(cont_name)
    except:
        con_client = bs_client.get_container_client(cont_name)

    # call to methods
    make_key()
    mykey = get_key()
    file = "privatecsetest2.txt"
    encrypt(file, mykey)
    upload_blob(file, bs_client, cont_name)
