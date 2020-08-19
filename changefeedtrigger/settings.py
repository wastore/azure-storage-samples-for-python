CONNECTION_STRING = ""

# these are the filters being used to filter out specific events
# these values represent what event characteristics you want to see
# for example, these filters will only return events with the event
# type of BlobCreated, and are in the container 
# testing-changefeed-container, and that are named blob2
# if event type filtering is not wanted, set EVENT_FILTER = None
# if blob filtering is not wanted, set BLOB_FILTER = None
# if neither is wanted, set both to None
EVENT_FILTER = "BlobCreated"
CONTAINER_FILTER = "test-changefeed-container"
BLOB_FILTER = "blob2"

EVENTS_PER_PAGE_QUANTITY = 50

