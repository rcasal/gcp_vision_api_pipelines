# GCP Vision API  analysis pipelines

The `gcp-vision-api-analysis-pipelines` repository provides Python scripts and utilities for image analysis and processing in Google Cloud Platform (GCP) using the Vision API. It offers a comprehensive solution for leveraging the Vision API's capabilities, including label detection, face detection, among others, on images. You can find all the suported features [here](https://cloud.google.com/vision/docs/features-list). Additionally, it includes scripts for scraping images from Marketing DSPs such as DV360 and Campaign Manager [WIP]. The processed images and analysis results can be stored in Google Cloud Storage (GCS) and further integrated with BigQuery (BQ) for advanced analytics. This repository serves as a practical toolkit for building efficient image processing pipelines in GCP.

## Key Features

* Integration with the Vision API: Perform various image analysis tasks such as label detection, face detection, and landmark detection using the Vision API.
* DSP Image Scraping [WIP]: Retrieve and download images from Marketing DSPs like DV360 and Campaign Manager for further analysis.
* Google Cloud Storage (GCS) Integration: Access and process images stored in Google Cloud Storage (GCS) buckets. The repository offers two solutions for image processing: batch and streaming. For **batch processing**, the `gcs_to_bq_processing` script allows you to analyze all the images in a GCS bucket using the Vision API. For **streaming processing**, the repository provides code to deploy a Cloud Function that listens to a GCS bucket, triggering Vision API processing each time a new image is uploaded. This integration simplifies the handling of images stored in GCS and facilitates seamless integration with the Vision API.
* BigQuery (BQ) Integration: Ingest image analysis data into BQ, enabling powerful analytics and insights on the processed images.
* Well-documented: Detailed documentation, including usage guides, code samples, and example pipelines, to help you get started quickly.

## Prerequisites

Before using the scripts and utilities in this repository, ensure that you have the following prerequisites in place:

1. Access to a Google Cloud Platform (GCP) project.
2. Enabled Vision API: Enable the Vision API in your GCP project.
3. Set up authentication: Set up authentication to authenticate your requests to the Vision API using the service account method. Download the JSON credentials for your service account and make sure to securely store them. Refer to the [Google Cloud Authentication](https://cloud.google.com/docs/authentication) documentation for more details.
4. Python and required dependencies: Install Python (version 3.8 or above) and the necessary dependencies by running the following command:

    ```shell
    pip install -r requirements.txt
    ```

5. GCS Bucket and BQ Dataset: Ensure that you have a Google Cloud Storage (GCS) bucket containing the images you want to process. Additionally, create a BigQuery (BQ) dataset where the analysis results will be stored.

## Usage

### Batch Processing

To perform batch processing on all the images in a GCS bucket and store the analysis in a BigQuery (BQ) table, follow these steps:

1. Ensure you have the necessary Python dependencies installed.

2. Run the following command, replacing the fields with the appropriate values:

    ```shell
    python gcp_vision_api_pipelines/gcs_to_bq_processing.py \
        --project_id "PROJECT_ID" \
        --input_bucket_name "BUCKET_NAME" \
        --output_dataset_name "DATASET_NAME" \
        --auth_file "AUTH_FILE" \
        --write_disposition "WRITE_DISPOSITION"
    ```

* `PROJECT_ID`: The ID of your Google Cloud project.
* `BUCKET_NAME`: The name of the GCS bucket containing the images.
* `DATASET_NAME`: The name of the BQ dataset where the analysis results will be stored.
* `AUTH_FILE`: The path to the authentication file for your Google Cloud project.
* `WRITE_DISPOSITION`: The write disposition for the BQ table (e.g., `WRITE_TRUNCATE`, `WRITE_APPEND` or `WRITE_EMPTY` to overwrite existing data).

### Streaming Processing

[WIP: Work in Progress]

Streaming processing using Cloud Functions is currently under development. We are actively working on it and will provide an update as soon as it is available. Stay tuned for further updates on this feature.

Please note that the provided example and instructions are subject to change. Refer to the repository documentation for the latest usage guidelines and code samples.

### DSP Image Scraping

[WIP: Work in Progress]

Retrieve and download images from Marketing DSPs like DV360 and Campaign Manager for further analysis. This feature enables you to easily gather images from different advertising platforms and incorporate them into your image analysis workflows.

Please note that the DSP Image Scraping feature is currently under development and will be released soon. We are actively working on it to provide you with a seamless and efficient solution for retrieving and analyzing images from Marketing DSPs. Stay tuned for further updates on this feature.

Once released, detailed instructions and code examples will be provided in the repository documentation to guide you through the process of leveraging this powerful image scraping functionality.

## Output Schema

The analysis results from the image processing using the Vision API are stored in BigQuery (BQ) for further analysis and insights.

Below is an example of the output schema:

| Field Name                   | Field Type   | Description                                               |
|------------------------------|--------------|-----------------------------------------------------------|
| creative_uri                 | STRING       | The URI of the processed image.                           |
| creative_id                  | STRING       | The id of the processed image to map with DSP.            |
| text_annotations             | RECORD       | The text detected in the image.                           |
| label_annotations            | RECORD       | The labels detected in the image.                         |
| web_detections_annotations   | RECORD       | The web detection objects in the image.                   |
| logo_annotations             | RECORD       | The logo detected in the image.                           |
| dominant_color_annotations   | RECORD       | The dominant color annotations detected in the image.     |
| face_annotations             | RECORD       | The faces detected in the image.                          |
| localized_object_annotations | RECORD       | The objects detected in the image.                        |
| search_safe_annotations      | RECORD       | The search safe annotations in the image.                 |

The output schema of the BQ table includes the following fields:

* `creative_uri`: The URL of the processed image.
* `creative_id`: The ID of the processed image for join with DSP performance metrics.
* `text_annotations`: A repeated field containing the text annotations detected in the image, including the descriptions and boundaries.
* `label_annotations`: A repeated field containing the label annotations detected in the image, including the description, score, topicality and mid.
* `web_detection_annotations`: A repeated field containing the web annotations detected in the image, including the web entities, visually similar images and best guess labels.
* `logo_annotations`: A repeated field containing information about the logo detected in the image. It contains a description, score, mid and boundaries of the detected logos.
* `dominant_color_annotations`: A repeated field containing information about the dominant colors in the image.
* `face_annotations`: A repeated field containing information about the faces in the image. Contains boundaries of the faces, sentiment analysis on each face, and landmarks.
* `localized_object_annotations`: A repeated field containing information about the objects in the image, including the object name, the score and boundaries.
* `search_safe_annotations`: A repeated field containing information about the search safe annotations in the image. It provides scores for racy, violence, medical, spoof and adult content.

Please refer to the documentation or code samples provided in the repository for more details on the output schema and how to query and analyze the results in BigQuery.

## Contributing

Contributions to the `gcp-vision-api-pipelines` repository are welcome! If you have any questions or need support with using this repository, please feel free to open an issue in this repository or contact the Buenos Aires Data Science Team. We are here to help and provide assistance with any inquiries you may have.
