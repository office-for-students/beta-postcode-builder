PostcodeSearchBuilderBlobTrigger - Python
=========================================
The postcode search builder creates and populates a postcode document into azure search containing a geographical location (latitudinal and longitudinal point). This is used to search for a course in the course search index using the retrieved latitudinal and longitudinal values for a postcode and using these two values plus the distance from postcode (e.g. 25miles) to find all courses within a given distance from the postcode inputted into a request to discoverUni's Search API.

### PostcodeSearchBuilder function processing steps

1. Course search builder is triggered when a new blob (postcodes) are stored in a storage container. It takes the path to the file and extracts the csv gzip file.

2. Following the recreation of the postcode index, the function iterates all postcode and validates they are in the region (latitude and longitude outlyers) of the UK including the Shetland islands.

3. Once validated the postcodes are stored against the postcode search index and are available for the search API to search against.

This process takes roughly 30minutes to complete

### Postcode data source

The postcode data that is uploaded to an azure storage container to which the azure function is configured to be triggered on, was taken from [free map tools](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm) as a csv file.

The csv file should contain the following header row (this is validated in the azure function):

| id  | postcode | latitude    | longitude    |
| --- | -------- | ----------- | ------------ |
| 1   | AB10 1XG | 57.14416516 | -2.114847768 |
| {n} | ...      | ...         | ...          |

There are approximately 1.75million postcodes - these will need to be updated manually by downloading the csv file from free map tools, compressing the file using gzip and uploading the file into the azure storage container that the `PostcodeSearchBuilderBlobTrigger` function triggers on.

#### Notes regarding postcode data

Non geographic postcodes are listed below. Note these will have a latitude and longitude of an empty string ([see data source](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm))

AB99, BT58, CA99, CM92, CM98, CR44, CR90, GIR, IM99, IV99, JE5, M61, ME99, N1C, N81, NR99, NW26, PA80, PE99, RH77, SL60, SO97, SW95, SY99, WD99, WF90

### Configuration Settings

Add the following to your local.settings.json:

| Variable                            | Default                | Description                                              |
| ----------------------------------- | ---------------------- | -------------------------------------------------------- |
| FUNCTIONS_WORKER_RUNTIME            | python                 | The programming language the function worker runs on     |
| AzureStorageAccountConnectionString | {retrieve from portal} | The connection string to access storage account          |
| AzureWebJobsStorage                 | {retrieve from portal} | The default endpoint to access storage account           |
| StopEtlPipelineOnWarning            | false                  | Boolean flag to stop function worker on a warning        |
| PostcodeIndexName                   | postcodes              | The storage container that will trigger the function     |
| SearchURL                           | {retrieve from portal} | The uri to the azure search instance                     |
| SearchAPIKey                        | {retrieve from portal} | The api key to access the azure search instance          |
| AzureSearchAPIVersion               | 2019-05-06             | The azure search API version for instance                |

### Setup

### Pre-Setup

1) Install [.Net Core 2.2 SDK](https://dotnet.microsoft.com/download), if you haven't already.
2) Install python 3.6.8 - the latest stable version that works with Azure client.
```
Mac user:
Install homebrew:
1) /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2) brew install sashkab/python/python36
3) pip3.6 install -U pip setuptools

Windows user:
```
3) Make sure Python 3.6.8 is set on your PATH, you can check this by running `python3 -v` in terminal window.
4) Install Azure Client
```
Mac user:
brew tap azure/functions
brew install azure-functions-core-tools

Windows user:
```
5) Setup Visual Studio Code, install [visual studio code](https://code.visualstudio.com/)
6) Also install the following extensions for visual studio code - documentation [here](https://code.visualstudio.com/docs/editor/extension-gallery)

```
Python
Azure CLI Tools
Azure Account
Azure Functions
Azure Storage
```

7) Sign into Azure with Visual Studio Code - follow documentation [here](https://docs.microsoft.com/en-us/azure/azure-functions/tutorial-vs-code-serverless-python#_sign-in-to-azure)

#### Building resources and running azure function locally

1) Create an azure search resource in azure portal, see Microsofts documentation [here](https://docs.microsoft.com/en-us/azure/search/search-create-service-portal)

2) Retrieve the azure search url and search api key from portal, (these will need to be added to you local.settings.json file)

3) Create/Reuse existing azure storage account, see Microsoft documentation [here](https://docs.microsoft.com/en-us/azure/storage/common/storage-quickstart-create-account?tabs=azure-portal)

4) Retrieve the azure storage account connection string and default endpoint, (these will need to be added to you local.settings.json file)

5) Create your local.settings.json file at root level of repository and include all environment variables in the configuration settings table above.

6) Create a Python virtual env to run the azure function application by running `venv .env` at root level of repository.

7) Run service on Python virtual env by doing the following:
```
source .env/bin/activate
pip install -r requirements.txt
func host start
```

8) Download latest csv UK postcode from [here](https://www.freemaptools.com/download-uk-postcode-lat-lng.htm)

9) Compress csv using gzip, `gzip <path to file>`, the current filename is `ukpostcodes.csv`

10) Upload the gzip file to postcodes blob container, this can be done in the Azure Portal or in Visual Studio Code and will trigger a new build of postcode resource into a poscode search index.

### Tests

To run tests, run the following command: `pytest -v`

### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.