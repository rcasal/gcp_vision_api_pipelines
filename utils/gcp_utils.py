import ndjson
from google.cloud import bigquery

def write_to_bq(bq_client, dataset_name, table_name, table_data, write_disposition):
    """
    Writes table data to BigQuery.

    Args:
        bq_client (object): BigQuery client object.
        dataset_name (str): Name of the dataset.
        table_name (str): Name of the table.
        table_data (list): List of table data.

    Returns:
        None
    """
    try:
        # Set the table file name
        table_file_name = f"{table_name}.json"

        # Write table data to a JSON file
        with open(table_file_name, 'w') as file:
            ndjson.dump(table_data, file)

        # Create dataset and table references
        dataset_ref = bq_client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)

        # Configure the job for loading data into BigQuery
        job_config = bigquery.LoadJobConfig()
        job_config.create_disposition = 'CREATE_IF_NEEDED'
        job_config.write_disposition = write_disposition
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.autodetect = True

        # Load the data from the file into the table
        with open(table_file_name, "rb") as source_file:
            job = bq_client.load_table_from_file(source_file, table_ref, job_config=job_config)
            job.result()

        print(f"Loaded {table_name} table")
    except Exception as e:
        print(f"ERROR - {table_name}: {e}")
