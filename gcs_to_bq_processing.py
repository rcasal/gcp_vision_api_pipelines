import argparse
from utils.vision_utils import process_images

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Project ID")
    parser.add_argument("--input_bucket_name", help="Input bucket name")
    parser.add_argument("--output_dataset_name", help="Output dataset name")
    parser.add_argument("--auth_file", help="Path to GCP authentication JSON file")
    parser.add_argument("--write_disposition", help="BigQuery write disposition. WRITE_TRUNCATE, WRITE_APPEND or WRITE_EMPTY.")
    return parser.parse_args()

def main():
    args = parse_args()

    project_id = args.project_id
    input_bucket_name = args.input_bucket_name
    output_dataset_name = args.output_dataset_name
    auth_file = args.auth_file
    write_disposition = args.write_disposition

    process_images(input_bucket_name, 
                   output_dataset_name, 
                   project_id, 
                   auth_file,
                   write_disposition
    )

if __name__ == "__main__":
    main()
