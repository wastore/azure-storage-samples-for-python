# Object Replication Service Sample
This sample demonstrates ORS replicating the blobs in a source container to a destination container. The sample first uploads 1000 blobs to the source container
and tracks the replication of the blobs. Next, the sample uploads a blob and compares the contents of the blob to the replicated blob in the destination container. Then, the blob's
contents are updated and compared with the replicated blob. Finally, the sample sets access tier of the blobs in the destination container to Archive tier.

## Prerequisites
Requires installation of [Python 3.6 or above](https://www.python.org/downloads/), an [Azure subscription](https://azure.microsoft.com/en-us/free/),
two [storage accounts](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal) with [changefeed](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-change-feed?tabs=azure-portal)
and [blob versioning](https://docs.microsoft.com/en-us/azure/storage/blobs/versioning-enable?tabs=portal) enabled.

#### Setting up ORS
Before running the sample, ensure that [ORS is configured](https://docs.microsoft.com/en-us/azure/storage/blobs/object-replication-configure?tabs=portal) for the storage accounts.

## Code Setup
Before running the sample, enter values for the following variables in settings.py
* Source Connection String
* Destination Connection String
* Source Container Name
* Destination Container Name

## Step By Step Instructions
1. Verify that all prerequisites are complete
2. Enter values for variables in settings.py
3. Run main.py
