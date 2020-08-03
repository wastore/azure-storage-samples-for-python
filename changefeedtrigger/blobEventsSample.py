from azure.storage.blob import BlobServiceClient
import azure.functions as func
import random

def create_event(blob_name, content, cont_client):
    index = random.randint(0,2)
    print("creating random blob events")
    try:
        container_client.delete_blob(blob_name[index])
    except:
        index = random.randint(0,2)
        cont_client.upload_blob(blob_name[index], content, overwrite=True)


if __name__ == "__main__":

    connection_string = "DefaultEndpointsProtocol=https;AccountName=caromechangefeed;AccountKey=gSm6zQqV4WHz6D68a+FZLJldRghOucLrI6p3ebg4i58jokwFF4G/lcCoReNEaUvv8Ezhasyxw2ktlX4+akCDIw==;EndpointSuffix=core.windows.net"
    container_name = "test-changefeed-container"
    blobs = ["blob1", "blob2", "blob3"]
    message = "blob content message"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    try:
        container_client = blob_service_client.create_container(container_name)
    except:
        container_client = blob_service_client.get_container_client(container_name)


    create_event(blobs, message, container_client)