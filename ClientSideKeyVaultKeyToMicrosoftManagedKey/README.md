# KeyVault Client Side Encryption Migration to Microsoft Managed Server Side Encryption

This program functions as a migration of data in Azure Storage from client side encryption with KeyVault to server side encryption using a Microsoft Managed key through encryption scope.

## Getting Started
### Prerequisites
Requires installation of [Python](https://www.python.org/downloads/) and [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest). Requires an [Azure subscription](https://azure.microsoft.com/en-us/free/) and an [Azure storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal).

## How to Use
###Setting Up the Program
#### exampleDataCreator.py
In the exampleDataCreator folder, please navigate to exampleDataCreator.py for a program example of what setup you should have completed before running the main program, migration.py. In this program, that means having performed client side encryption with a KeyVault key and having had uploaded it to Azure Storage as a blob.

It is not required to run this file in order to run migration.py
####settings.py
In the setup folder, please read through and update the settings.py file with the required information before running the main program, migration.py. All of the information in the settings.py file is required, or else the program will not function.

###Running the Main Program
####migration.py
After following the above steps under _Setting Up The Program_, all that is required to perform the migration is to run the file migration.py. This program will decrypt the KeyVault key client side encryption and re-upload the blob to Azure Storage with Microsoft Managed Server Side Encryption.