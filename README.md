#Azure Storage Samples For Python
##README.md
#####This application functions as a migration tool from client side encryption to CPK-N
####Directory Layout
#####Each folder represents a different scenario from client side encryption to server side encryption. The two types of client side encryption provided in these samples are using a Keyvault Key or a local key. The three types of server side encryption in this sample are Microsoft managed key encryption scope, customer managed key encryption scope, and customer provided encryption key.
#####Each scenario folder has a folder in it named [], which contains the sample data [].py, the configuration file config.py, and a test text file, blobExample.py. Outside of the nested [] folder is a README.md specific to that scenario as well as the runnable application migration.py.

####Using This Application
#####To better understand which scenario is right for the type of migration you need, read the scenario specific README.md files, found in each scenario folder.
