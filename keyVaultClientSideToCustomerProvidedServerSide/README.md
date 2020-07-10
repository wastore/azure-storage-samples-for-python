# KeyVault Client Side Encryption Migration to Customer Provided Key Server Side Encryption

This program functions as a migration of data in Azure Storage from client side encryption with KeyVault to server side encryption using a Customer Provided Key for server side encryption.

## Getting Started
### Prerequisites
[add other requirements here]

## How to Use
###Setting Up the Program
#### setup.py
In the setup folder, please navigate to setup.py for a program example of what setup you should have completed before running the main program, migration.py. In this program, that means having performed client side encryption with a KeyVault key and having had uploaded it to Azure Storage as a blob.
####config.py
In the setup folder, please read through and update the config.py file with the required information before running the main program, migration.py. All of the information in the config.py file is required, or else the program will not function.

###Running the Main Program
####migration.py
After following the above steps under _Setting Up The Program_, all that is required to perform the migration is to run the file migration.py. This program will decrypt the KeyVault key client side encryption and re-upload the blob to Azure Storage with a Customer Provided Key for server side encryption.