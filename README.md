# Python Pipeline

This project includes Azure Functions for Python and is configured for local development, specifically tailored for Macs with M1+ chips, which utilize the ARM64 architecture.

## Local Development Setup

Before running the functions locally, ensure you have set up your environment according to the official [Azure Functions local development documentation](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python).

Due to compatibility issues, Azure Functions may not work out-of-the-box on ARM64 architecture. Follow the instructions provided in this guide to [Run Python Azure Function Locally on an M1/M2 Mac](http://issamben.com/running-python-azure-function-locally-on-an-m1-m2/).

### Running Azurite for Blob Storage Emulation

To emulate Azure Blob Storage locally, start Azurite using the following command:

```shell
azurite-blob --silent
````

### Starting Azure Functions
To run Azure Functions locally after setting up your environment, use the following command:

````shell
func start
````

Ensure that your environment variables are properly configured and that the Azure Functions Core Tools are correctly installed before attempting to start the function app.

