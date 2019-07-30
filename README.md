# PostcodeSearchBuilderBlobTrigger - Python
=========================================
The postcode search builder creates and populates a postcode document into azure search containing a geographical location (latitutinal and longitudinal point). This is used to search for a course in the course search index using the retrieved latitudinal and longitudinal values for a postcode and using these two values plus the distance from postcode (e.g. 25miles) to find all courses within a given distance from the postcode inputted into a request to discoverUni's Search API.

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