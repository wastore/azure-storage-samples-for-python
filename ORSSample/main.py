import os
import time
from settings import *
from azure.storage.blob import BlobServiceClient

source_connect_str = SOURCE_CONNECTION_STRING
dest_connect_str = DESTINATION_CONNECTION_STRING
source_container_name = SOURCE_CONTAINER_NAME
dest_container_name = DESTINATION_CONTAINER_NAME
blobs = BLOB_NAMES


def main():
    source_blob_service_client = BlobServiceClient.from_connection_string(source_connect_str)
    source_blob_container_client = source_blob_service_client.get_container_client(source_container_name)
    source_blob_client = source_blob_service_client.get_blob_client(container=source_container_name, blob=blobs[0])

    print("Uploading source blobs...")
    upload_blobs(source_blob_service_client, source_container_name, blobs)

    print("Replicating...")
    track_progress(source_blob_service_client, source_container_name, blobs)
    print("Replication Complete")

    dest_blob_service_client = BlobServiceClient.from_connection_string(dest_connect_str)
    dest_blob_client = dest_blob_service_client.get_blob_client(container=dest_container_name, blob=blobs[0])

    print_contents(source_blob_client, dest_blob_client)

    print("Updating source blob...")
    source_blob_client.upload_blob("Lorem Ipsum", overwrite=True)

    print("Replicating...")
    check_completion(source_blob_client)
    print("Replication Complete")
    print_contents(source_blob_client, dest_blob_client)

    print("Archiving...")
    archive_blobs(source_blob_container_client, blobs)
    print("Archived")


# Upload multiple blobs
def upload_blobs(source_blob_service_client, container_name, blobs):
    for blob_name in blobs:
        source_blob_client = source_blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        source_blob_client.upload_blob("Hello World!", overwrite=True)


# Tracks progress of replicating multiple blobs
def track_progress(source_blob_service_client, container_name, blobs):
    completed = 0
    length = len(blobs)
    incomplete_events = blobs.copy()
    completed_events = []

    while completed < length:
        for incomplete_event in incomplete_events:
            blob_client = source_blob_service_client.get_blob_client(container=container_name, blob=incomplete_event)
            props = blob_client.get_blob_properties()

            for replication_policy in props.object_replication_source_properties:
                for rule in replication_policy.rules:
                    if rule.status == "complete":
                        completed += 1
                        completed_events.append(incomplete_event)
                        incomplete_events.remove(incomplete_event)

                        percent = completed/length
                        print("Replication is at " + str(percent*100) + "%.")
                        print("Replicated " + str(completed) + "/" + str(length) + " blobs.")
                        if percent == 1:
                            break

                    if rule.status == "failed":
                        print("failed")
                        break


# Checks completion for a single blob
def check_completion(source_blob_client):
    completion = False
    while not completion:
        props = source_blob_client.get_blob_properties()
        for replication_policy in props.object_replication_source_properties:
            for rule in replication_policy.rules:
                if rule.status == "complete":
                    completion = True
                    break

        time.sleep(10)


# Compares the contents of a replicated blob
def print_contents(source_blob_client, dest_blob_client):
    print("Source Blob Contents:")
    download_source = open("download_source.txt", "wb")
    download_source.write(source_blob_client.download_blob().readall())
    download_source = open("download_source.txt", "r")
    print(download_source.read())
    download_source.close()

    print("Destination Blob Contents:")
    download_dest = open("download_dest.txt", "wb")
    download_dest.write(dest_blob_client.download_blob().readall())
    download_dest = open("download_dest.txt", "r")
    print(download_dest.read())
    download_dest.close()

    os.remove("download_source.txt")
    os.remove("download_dest.txt")


# Archive blobs individually
def archive_blobs(container_client, blobs):
    for blob_name in blobs:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.set_standard_blob_tier("Archive")


# Archive blobs using a batch
def archive_batch(container_client, blobs):
    container_client.set_standard_blob_tier_blobs("Archive", *blobs)


if __name__ == '__main__':
    main()
