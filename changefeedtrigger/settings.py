CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=changefeedtester;AccountKey=u9JE+P4QTyakAUmsCawmMtxXiCTbnKUoPjglZ3kn2sq203bvasVZSTqaIEyVJyxfYi9mhAV5va3LHX0ALImHvA==;EndpointSuffix=core.windows.net"

EVENTS_PER_PAGE_QUANTITY = 5

# these are the filters being used to filter out specific events
# these values represent what event characteristics you want to see
# for example, these filters will only return events with the event
# type of BlobCreated, and are in the container 
# testing-changefeed-container, and that are named blob2
EVENT_FILTER = "BlobCreated"
CONTAINER_FILTER = "test-changefeed-container"
BLOB_FILTER = "blob2"