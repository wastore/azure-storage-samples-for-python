#Client Side Encryption to CPK-N Migration
#####Various Migration Samples From Client Side Encryption to Server Side Encryption

##General Info
These samples begin with an optional data creation process to create an example container and blob with client side encryption. The samples then migrate the specified blob to a specific type of server side encryption and uploads the server side encrypted blob in the same container.

##General Setup Requirements
All samples require users to enter their storage credentials in the config.py file. For more details on setup, refer to the README of the specific sample used.

The migration.py file can also be ran without running the exampleDataCreator.py file, however all components of the setup must be in place: container, blob uploaded with client side encryption, encryption scope where applicable, keyvault keys where applicable, keyvault secret where applicable, etc. All of these values can be inputted in the config.py file for each scenario.