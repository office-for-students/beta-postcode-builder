"""Contains the entry point for Create Postode Search
Azure Function implementation"""
import logging
import io
import gzip
import os
import traceback
from datetime import datetime

import azure.functions as func
from . import search


def main(postcodeblob: func.InputStream):
    """Create the postcode search index"""

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {postcodeblob.name}\n"
                 f"Blob Size: {postcodeblob.length} bytes")

    api_key = os.environ['SearchAPIKey']
    search_url = os.environ['SearchURL']
    api_version = os.environ['AzureSearchAPIVersion']
    index_name = os.environ['PostcodeIndexName']

    try:
        # Read the compressed Blob into a BytesIO object
        compressed_file = io.BytesIO(postcodeblob.read())

        # Read the compressed file into a GzipFile object
        compressed_gzip = gzip.GzipFile(fileobj=compressed_file)

        # Decompress the data
        decompressed_file = compressed_gzip.read()

        # Decode the bytes into a string
        csv_string = decompressed_file.decode("utf-8")

        rows = csv_string.splitlines()
        number_of_postcodes = len(rows)

        # Create postcode search index
        search.build_index(search_url, api_key, api_version, index_name)

        # Add postcode documents to postcode search index
        logging.info(f'attempting to load postcodes to azure search\n\
                        number_of_postcodes: {number_of_postcodes}\n')
        search.load_index(search_url, api_key, api_version, index_name, rows)

        pipeline_end_datetime = datetime.today().strftime("%Y%m%d %H%M%S")
        logging.info(
            "PostcodeSearchBuilderBlobTrigger successfully finished on "
            + pipeline_end_datetime
        )

    except Exception as e:
        # Unexpected exception
        logging.error('Unexpected extension')
        logging.error(traceback.format_exc())

        # Raise to Azure
        raise e
