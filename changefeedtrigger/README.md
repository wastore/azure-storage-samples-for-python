# README
The purpose of this sample is to create a log of all new events that occur in a storage account with multidimensional filtering that runs on a timer using an Azure Function.

## Prerequisites
[An Azure Subscription](https://azure.microsoft.com/en-us/free/)

[An Azure Storage Account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)

[A Timer Trigger Azure Function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-scheduled-function#:~:text=Create%20a%20timer%20triggered%20function%201%20Expand%20your,by%20viewing%20trace%20information%20written%20to%20the%20logs.)

[Visual Studio Code](https://visualstudio.microsoft.com/downloads/)

[Python 3.6 or above](https://www.python.org/downloads/)

## How to Use
This sample includes an changefeedSample.py file as the main program, a function.json to configure the timer trigger function, and a blobEventsSample.py file that represents a data creation sample by creating events to test the program on.

Please add all required personal information to settings.py

## Building An Azure Function
For help setting up an Azure Function follow these steps:

### Create a Function App
1. From the Azure portal home page select "Create a resource"
2. In the "New" page, select Compute > Function App
3. Fill out required information then select "Review + Create"

Python does not allow for creating function within the portal, so that function itself is in this sample rather than created in portal.

### Deploy the Function
1. Open this sample in Visual Studio Code
2. On the left had tab click the "Azure" symbol icon
3. At the top of the lefthand menu click the blue arrow that points upwards labeled "deploy to function app..."
4. Fill out required information and deploy application
5. Wait for function to successfully deploy to your function app

### Run the Function
1. In Visual Studio Code press F5 to run the function locally, this requires having Azure Functions Core Tools installed.

or

1. In Azure portal navigate to your function, found in "Functions" in the left hand menu of your function app
2. Select the function you created
3. Click "Code + Test" in the left hand menu
4. Click "Test/Run"
5. In the popup window click the blue button "Run"
6. When the portal terminal window says "Connected!" click the blue "Run" button again
7. Wait for function to trigger and view output in portal terminal window 


If more help is needed reference this documentation, but note that it references creating an HTTP trigger that is created in portal, which is not a compatible function creation method with Python:

https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function

## Viewing logs from Azure Function
To view logs from the deployed changefeedSample program, follow [these instructions.](https://docs.microsoft.com/en-us/azure/azure-functions/functions-monitoring?tabs=cmd)
