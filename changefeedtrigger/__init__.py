import time
import json
from subprocess import Popen, PIPE
from azure.storage.blob.changefeed import ChangeFeedClient
from azure.storage.blob import BlobServiceClient
import azure.functions as func
from datetime import timedelta, datetime
import logging
from predicate import where


def multidimensional_filtering(cf_client, b_filter, blob_client, cont_name, c_filter, e_filter):
    filter_event_service = blob_client.get_container_client(container=cont_name)
    blob_name = "continuation-token"

    # access blobs in container
    blob_list = filter_event_service.list_blobs()
    tokens = []
    for blob in blob_list:
        tokens.append(blob.name)
    
    # check if continuation token already exists
    if blob_name in tokens:
        cursor = filter_event_service.download_blob(blob_name).readall()
        # if value of token is None return None
        if cursor == b"None":
            return None
        # if value of token is a cursor initiate the changefeed with cursor
        elif cursor != b"" and cursor != b"None":
            change_feed = cf_client.list_changes(results_per_page=500).by_page(continuation_token=eval(cursor))
        # if token is empty initiate changefeed without cursor
        else:
            change_feed = cf_client.list_changes(results_per_page=500).by_page()
    # if token does not exist upload token as empty string placeholder as blob and initiate changefeed without cursor
    else:
        filter_event_service.upload_blob(blob_name, "") 
        change_feed = cf_client.list_changes(results_per_page=500).by_page()

    # iterate through change feed
    change_feed_page = next(change_feed)

    # get multidimensionally filtered events
    #filtered_events = list(filter(where(data__eventType__iexact=e_filter, data__subject__icontains=("/" + c_filter + "/blobs/" + b_filter)), events))
    filtered_events = []
    for event in change_feed_page:
        if (event["eventType"] == e_filter) and (("/" + c_filter + "/") in event["subject"]) and (("/" + b_filter) in event["subject"]):
            filtered_events.append(event)
        # set continuation token as last event in the filtered event list
        cursor = change_feed.continuation_token
    
    # update continuation token blob with new continuation token
    filter_event_service.upload_blob(blob_name, str(cursor), overwrite=True)

    # return filtered events
    return filtered_events
    

def main(mytimer: func.TimerRequest) -> None:
    # creating clients from storage account connection string
    connection_strs = ""

    bs_client = BlobServiceClient.from_connection_string(conn_str=connection_strs)
    change_feed_client = ChangeFeedClient.from_connection_string(conn_str=connection_strs)

    # create or get container to store cursor
    container_name = "cursor-container"
    try:
        cont_client = bs_client.create_container(container_name)
    except:
        cont_client = bs_client.get_container_client(container_name)

    event_filter = "BlobSnapshotCreated"
    container_filter = "testingchangefeed2"
    blob_filter = "IMG_8746.JPG"

    # filtering method
    events = multidimensional_filtering(change_feed_client, blob_filter, bs_client, container_name, container_filter, event_filter)
 
    if events == None:
        logging.info("\nChangefeed has iterated through all events...")
    elif len(events) == 0:
        logging.info("\nNo events matching filter in current page...")
    else:
        logging.info("\nRecents event(s):")
        count = 1
        for e in events:
            logging.info("%d: %s\n" % (count, e))
            count += 1