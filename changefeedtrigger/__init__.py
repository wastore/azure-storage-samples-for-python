from azure.storage.blob.changefeed import ChangeFeedClient
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import logging

#!!!TODO: values to fill in:

# creating clients from storage account connection string
# make sure connection string is also in local.settings.json
connection_strs = ""

events_per_page_quantity = 5

# these are the filters being used to filter out specific events
# these values represent what event characteristics you want to see
# for example, these filters will only return events with the event
# type of BlobCreated, and are in the container 
# testing-changefeed-container, and that are named blob2
event_filter = "BlobCreated"
container_filter = "test-changefeed-container"
blob_filter = "blob2"

# if filtering of events is unwanted, the method filter_events can be commented out and changefeed will iterate on all events


def main(mytimer: func.TimerRequest) -> None:

    # create blob service client to access connection string
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_strs)
    change_feed_client = ChangeFeedClient.from_connection_string(conn_str=connection_strs)

    # create or get container to store cursor
    container_name = "cursorstoragecontainer"
    try:
        token_container_client = blob_service_client.create_container(container_name)
    except:
        token_container_client = blob_service_client.get_container_client(container_name)

    # call to method
    cursor = get_cursor(token_container_client)
    events = get_events(cursor, token_container_client, change_feed_client)
    events = filter_events(events) # if filtering events is unwanted this method can be commented out
 
    # log filtered event output
    if len(events) == 0:
        logging.info("\nNo events matching filters on current page...")
    else:
        logging.info("\nRecents event(s) matching filters on current page:")
        count = 1
        for e in events:
            logging.info("%d: %s\n" % (count, e))
            count += 1


def get_cursor(token_client):
    # this method is to grab and return the cursor
    
    # access blobs in container
    blob_list = token_client.list_blobs()
    tokens = []
    for blob in blob_list:
        tokens.append(blob.name)

    return tokens


def get_events(tokens, token_client, cf_client):
    # this method uses the continuation token to iterate on events and updates the token

    # check if continuation token already exists
    blob_name = "cursorBlob"
    if blob_name in tokens:
        cursor = token_client.download_blob(blob_name).readall()

        # initiate the changefeed with cursor
        change_feed = cf_client.list_changes(results_per_page=events_per_page_quantity).by_page(continuation_token=eval(cursor))

    # if token does not exist upload token as empty string placeholder as blob and initiate changefeed without cursor
    else: 
        change_feed = cf_client.list_changes(results_per_page=events_per_page_quantity).by_page()

    # iterate through change feed
    change_feed_page = next(change_feed)

    all_events = []
    for event in change_feed_page:
        all_events.append(event)

    # check if new iteration reaches end of events
    if change_feed.continuation_token is None:
        logging.info("\nNo new matching events... program will output last set of matching events until new events are added...")
    # set continuation token as last event in the filtered event list
    else:
        cursor = change_feed.continuation_token
        # update continuation token blob with new continuation token
        token_client.upload_blob(blob_name, str(cursor), overwrite=True)

    return all_events


def filter_events(events):
    # this method filters the changefeed events

    # get multidimensionally filtered events
    filtered_events = []
    for event in events:
        if (event["eventType"] == event_filter) and (("/" + container_filter + "/") in event["subject"]) and (("/" + blob_filter) in event["subject"]):
            filtered_events.append(event) 

    # return filtered events
    return filtered_events
