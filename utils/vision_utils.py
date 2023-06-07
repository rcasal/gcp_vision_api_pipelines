from google.cloud import storage, vision, bigquery
from google.oauth2 import service_account
from typing import List
import io
from utils.format_utils import format_json
from utils.gcp_utils import write_to_bq


def analyze_image_from_uri(image_uri: str, feature_types: List[str]) -> vision.AnnotateImageResponse:
    """
    Analyzes an image from the given URI using the specified feature types and returns the response.
    
    Args:
        image_uri (str): The URI of the image to analyze.
        feature_types (List[str]): A list of feature types to include in the analysis.
    
    Returns:
        vision.AnnotateImageResponse: The response from the Vision API containing the analysis results.
    """
    # Create a client for the Vision API
    client = vision.ImageAnnotatorClient()

    # Create an Image object and set the image URI
    image = vision.Image()
    image.source.image_uri = image_uri

    # Create a list of Feature objects based on the given feature types
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]

    # Create an AnnotateImageRequest with the image and features
    request = vision.AnnotateImageRequest(image=image, features=features)

    # Send the request to the Vision API and get the response
    response = client.annotate_image(request=request)

    return response


def process_images(input_bucket_name, output_dataset_name, project_id, auth_path, write_disposition):
    """
    Process images in a GCS bucket using the Cloud Vision API and save the output in another GCS bucket.
    
    Args:
        input_bucket_name (str): Name of the input GCS bucket containing the images.
        output_dataset_name (str): Name of the output BQ dataset.
        project_id (str): Name of the GCP project required for authentication.
        auth_path (str): Path to GCP authentication JSON file.
        write_disposition (str): BigQuery write disposition.
    """
    # Create the config file to avoid so many arguments
    config = {
        "project_id": project_id,
        "input_bucket_name": input_bucket_name,
        "output_dataset_name": output_dataset_name
    }

    # Initialize GCS client with the specified project ID
    storage_client = storage.Client()

    # Get the input and output buckets
    input_bucket = storage_client.get_bucket(config['input_bucket_name'])

    ## Get all blobs (images) in the input bucket
    blobs = input_bucket.list_blobs()

    # Create credentials for BigQuery
    credentials_bq = service_account.Credentials.from_service_account_file(auth_path)

    # Create a BigQuery client
    bq_client = bigquery.Client(project=config['project_id'], credentials=credentials_bq)

    # Define the output and table name
    table_name = f"gcp_vision_api_annotations"

    # Features
    features = [
        vision.Feature.Type.OBJECT_LOCALIZATION,
        vision.Feature.Type.FACE_DETECTION,
        # vision.Feature.Type.LANDMARK_DETECTION, # detects popular natural and human-made structures in the image, providing lat and long.
        vision.Feature.Type.LOGO_DETECTION, 
        vision.Feature.Type.LABEL_DETECTION,
        vision.Feature.Type.TEXT_DETECTION, 
        #vision.Feature.Type.DOCUMENT_TEXT_DETECTION, # for documents
        vision.Feature.Type.SAFE_SEARCH_DETECTION,
        vision.Feature.Type.IMAGE_PROPERTIES,
        vision.Feature.Type.CROP_HINTS,
        vision.Feature.Type.WEB_DETECTION,
        vision.Feature.Type.PRODUCT_SEARCH,
    ]
    
    response_list = []
    for blob in blobs:
        # Get the URI of the image blob
        image_uri = f"gs://{config['input_bucket_name']}/{blob.name}"

        response = analyze_image_from_uri(image_uri, features)

        # Save the analysis results to BQ
        creative_data = format_json(
            response=response, 
            creative_id=image_uri, # We need to change this!
            creative_uri=image_uri
        )

        response_list.append(creative_data)

    # Write the creative data to BigQuery
    write_to_bq(bq_client, config['output_dataset_name'], table_name, response_list, write_disposition)

    return 'OK'
