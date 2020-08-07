from azure.storage.blob import BlobServiceClient
import azure.functions as func
import random
import time


def main():
    connection_string = ""
    container_name = "test-changefeed-container"
    blobs = ["blob1", "blob2", "blob3"]
    message = "Lorem ipsum"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    try:
        container_client = blob_service_client.create_container(container_name)
    except:
        container_client = blob_service_client.get_container_client(container_name)


    simulate_account_activity(blobs, message, container_client)


def simulate_account_activity(blob_name, content, cont_client):

    # this method creates events at random in a container, either deleting or creating a blob

    index = random.randint(0,2)
    print("creating random blob events")
    try:
        cont_client.delete_blob(blob_name[index])
    except:
        index = random.randint(0,2)
        cont_client.upload_blob(blob_name[index], content, overwrite=True)


if __name__ == "__main__":
    while (True):
        main()
        time.sleep(2700)



    