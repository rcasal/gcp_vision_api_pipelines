from google.cloud import vision
from typing import List, Dict, Any
import math


def format_json(response, creative_id, creative_uri):
    """
    Formats the response and writes it to BigQuery.

    Args:
        response (object): Response object from the Vision API.
        creative_id (str): ID of the creative.
        creative_uri (str): URI of the creative.
        config (dict): Configuration dictionary containing project_id and dataset_name.

    Returns:
        None
    """
    # Format the creative data
    creative_data = {
        "creative_id": str(creative_id),
        "creative_uri": str(creative_uri),
        "localized_object_annotations": format_localized_object_annotations(response),
        "face_annotations": format_face_annotations(response),
        "logo_annotations": format_logo_annotations(response),
        "label_annotations": format_label_annotations(response),
        "text_annotations": format_text_annotations(response),
        "search_safe_annotations": format_safe_search_annotations(response),
        "dominant_color_annotations": format_dominant_color_annotations(response),
        "web_detection_annotations": format_web_detection_annotations(response)
    }

    return creative_data


# web detection annotations
def format_web_detection_annotations(response):
    """
    Formats the web detection annotations from the response object.

    Args:
        response (object): Response object containing text.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each best guess label in the response
    best_guess_label_annotations = []
    for label in response.web_detection.best_guess_labels:
        # Extract relevant information and convert to appropriate types
        data = {
            "label": str(label.label),
            "language_code": str(label.language_code),
        }

        # Append the formatted data to the list
        best_guess_label_annotations.append(data)

    best_guess_label_annotations = best_guess_label_annotations if best_guess_label_annotations else fill_empty_best_guess_label_annotations()

    # Iterate over each visual similar image in the response
    visually_similar_images_annotations = []
    for url in response.web_detection.visually_similar_images:
        # Extract relevant information and convert to appropriate types
        data = {
            "url": str(url.url),
        }

        # Append the formatted data to the list
        visually_similar_images_annotations.append(data)

    visually_similar_images_annotations = visually_similar_images_annotations if visually_similar_images_annotations else fill_empty_visually_similar_images_annotations()
    
    # Iterate over each web entitie in the response
    web_entities_annotations = []
    for entity in response.web_detection.web_entities:
        # Extract relevant information and convert to appropriate types
        data = {
            "entity_id": str(entity.entity_id),
            "score": float(entity.score),
            "description": str(entity.description)
        }

        # Append the formatted data to the list
        web_entities_annotations.append(data)

    web_entities_annotations = web_entities_annotations if web_entities_annotations else fill_empty_web_entities_annotations()
    
    # Package the subresponses in the web detection response
    web_detection_annotations = {
        "best_guess_label_annotations": best_guess_label_annotations,
        "visually_similar_images_annotations": visually_similar_images_annotations,
        "web_entities_annotations": web_entities_annotations
    }

    return web_detection_annotations



# dominant color annotations
def format_dominant_color_annotations(response):
    """
    Formats the dominant color annotations from the response object.

    Args:
        response (object): Response object containing text.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each element in the response
    dominant_color_annotations = []
    for color in response.image_properties_annotation.dominant_colors.colors:
        # Extract relevant information and convert to appropriate types
        data = {
            "red": float(color.color.red),
            "green": float(color.color.green),
            "blue": float(color.color.blue),
            "score": float(color.score),
            "pixel_fraction": float(color.pixel_fraction),
        }

        # Append the formatted data to the list
        dominant_color_annotations.append(data)

    return dominant_color_annotations


# safe search annotations
def format_safe_search_annotations(response):
    """
    Formats the search safe annotations from the response object.

    Args:
        response (object): Response object containing text.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    safe_search_annotations = []
    # Extract relevant information and convert to appropriate types
    data = {
        "adult": float(response.safe_search_annotation.adult.value),
        "spoof": float(response.safe_search_annotation.spoof.value),
        "medical": float(response.safe_search_annotation.medical.value),
        "violence": float(response.safe_search_annotation.violence.value),
        "racy": float(response.safe_search_annotation.racy.value),
    }

    # Append the formatted data to the list
    safe_search_annotations.append(data)

    return safe_search_annotations


# text annotations
def format_text_annotations(response):
    """
    Formats the text annotations from the response object.

    Args:
        response (object): Response object containing text.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each element in the response
    text_annotations = []
    for text in response.text_annotations:
        # Extract relevant information and convert to appropriate types
        data = {
            "description": str(text.description),
            "x0": float(text.bounding_poly.vertices[0].x),
            "y0": float(text.bounding_poly.vertices[0].y),
            "x1": float(text.bounding_poly.vertices[1].x),
            "y1": float(text.bounding_poly.vertices[1].y),
            "x2": float(text.bounding_poly.vertices[2].x),
            "y2": float(text.bounding_poly.vertices[2].y),
            "x3": float(text.bounding_poly.vertices[3].x),
            "y3": float(text.bounding_poly.vertices[3].y),
        }

        # Append the formatted data to the list
        text_annotations.append(data)

    text_annotations = text_annotations if text_annotations else fill_empty_text_annotations()

    return text_annotations


# label annotations
def format_label_annotations(response):
    """
    Formats the label annotations from the response object.

    Args:
        response (object): Response object containing label.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each element in the response
    label_annotations = []
    for label in response.label_annotations:
        # Extract relevant information and convert to appropriate types
        data = {
            "description": str(label.description),
            "score": float(label.score),
            "mid": str(label.mid),
            "topicality": float(label.topicality),
        }

        # Append the formatted data to the list
        label_annotations.append(data)

    label_annotations = label_annotations if label_annotations else fill_empty_label_annotations()

    return label_annotations


# Logo annotations
def format_logo_annotations(response):
    """
    Formats the logo annotations from the response object.

    Args:
        response (object): Response object containing logo.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each element in the response
    logo_annotations = []
    for logo in response.logo_annotations:
        # Extract relevant information and convert to appropriate types
        data = {
            "description": str(logo.description),
            "score": float(logo.score),
            "mid": str(logo.mid),
            "x0": float(logo.bounding_poly.vertices[0].x),
            "y0": float(logo.bounding_poly.vertices[0].y),
            "x1": float(logo.bounding_poly.vertices[1].x),
            "y1": float(logo.bounding_poly.vertices[1].y),
            "x2": float(logo.bounding_poly.vertices[2].x),
            "y2": float(logo.bounding_poly.vertices[2].y),
            "x3": float(logo.bounding_poly.vertices[3].x),
            "y3": float(logo.bounding_poly.vertices[3].y),
        }

        # Append the formatted data to the list
        logo_annotations.append(data)

    logo_annotations = logo_annotations if logo_annotations else fill_empty_logo_annotations()

    return logo_annotations


# Face annotations
def format_face_annotations(response):
    """
    Formats the face annotations from the response object.

    Args:
        response (object): Response object containing face annotations.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    face_annotations = []

    # Iterate over each element in the response
    for count, face in enumerate(response.face_annotations, start=1):
        # bounding_poly
        bounding_poly = {
            "x_0": float(face.bounding_poly.vertices[0].x),
            "y_0": float(face.bounding_poly.vertices[0].y),
            "x_1": float(face.bounding_poly.vertices[1].x),
            "y_1": float(face.bounding_poly.vertices[1].y),
            "x_2": float(face.bounding_poly.vertices[2].x),
            "y_2": float(face.bounding_poly.vertices[2].y),
            "x_3": float(face.bounding_poly.vertices[3].x),
            "y_3": float(face.bounding_poly.vertices[3].y),
        }
        
        #fd bounding_poly
        fd_bounding_poly = {
            "x_0": float(face.fd_bounding_poly.vertices[0].x),
            "y_0": float(face.fd_bounding_poly.vertices[0].y),
            "x_1": float(face.fd_bounding_poly.vertices[1].x),
            "y_1": float(face.fd_bounding_poly.vertices[1].y),
            "x_2": float(face.fd_bounding_poly.vertices[2].x),
            "y_2": float(face.fd_bounding_poly.vertices[2].y),
            "x_3": float(face.fd_bounding_poly.vertices[3].x),
            "y_3": float(face.fd_bounding_poly.vertices[3].y),
        }
        
        #landmarks
        landmarks = []
        for l in face.landmarks:
            landmark = {
                "type": str(l.type_.name),
                "x": float(l.position.x),
                "y": float(l.position.y),
                "z": float(l.position.z)
                
            }
            landmarks.append(landmark)
            
        # format json    
        data = {
            "name": f"face{count}",
            "bounding_poly": bounding_poly,
            "fd_bounding_poly": fd_bounding_poly,
            "landmarks": landmarks,
            "roll_angle": float(face.roll_angle),
            "pan_angle": float(face.pan_angle),
            "tilt_angle": float(face.tilt_angle),
            "detection_confidence": float(face.detection_confidence),
            "landmarking_confidence": float(face.landmarking_confidence),
            "joy_likelihood": float(face.joy_likelihood.value),
            "sorrow_likelihood": float(face.sorrow_likelihood.value),
            "anger_likelihood": float(face.anger_likelihood.value),
            "surprise_likelihood": float(face.surprise_likelihood.value),
            "under_exposed_likelihood": float(face.under_exposed_likelihood.value),
            "blurred_likelihood": float(face.blurred_likelihood.value),
            "headwear_likelihood": float(face.headwear_likelihood.value)
        }

        # Append the formatted data to the list
        face_annotations.append(data)

    face_annotations = face_annotations if face_annotations else fill_empty_face_annotations()

    return face_annotations

# Localized object annotations
def format_localized_object_annotations(response):
    """
    Formats the localized object annotations from the response object.

    Args:
        response (object): Response object containing localized object annotations.

    Returns:
        list: List of dictionaries containing formatted annotations.
    """
    # Iterate over each element in the response
    localized_object_annotations = []
    for element in response.localized_object_annotations:
        # Extract relevant information and convert to appropriate types
        data = {
            "name": str(element.name),
            "score": float(element.score),
            "normalized_x0": float(element.bounding_poly.normalized_vertices[0].x),
            "normalized_y0": float(element.bounding_poly.normalized_vertices[0].y),
            "normalized_x1": float(element.bounding_poly.normalized_vertices[1].x),
            "normalized_y1": float(element.bounding_poly.normalized_vertices[1].y),
            "normalized_x2": float(element.bounding_poly.normalized_vertices[2].x),
            "normalized_y2": float(element.bounding_poly.normalized_vertices[2].y),
            "normalized_x3": float(element.bounding_poly.normalized_vertices[3].x),
            "normalized_y3": float(element.bounding_poly.normalized_vertices[3].y),
        }

        # Append the formatted data to the list
        localized_object_annotations.append(data)

    localized_object_annotations = localized_object_annotations if localized_object_annotations else fill_empty_localized_object_annotations()

    return localized_object_annotations


# Fill empty functions
def fill_empty_web_entities_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty web entities annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty web entities annotations.
    """     
    # format json    
    empty_data = {
        "entity_id": str('Not Found'),
        "score": float(0),
        "description": str('Not Found')
    }

    return [empty_data]


def fill_empty_visually_similar_images_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty visually similar images annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty visually similar images annotations.
    """     
    # format json    
    empty_data = {
        "url": str('Not Found'),
    }

    return [empty_data]
    

def fill_empty_best_guess_label_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty best guest label annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty best guest label annotations.
    """     
    # format json    
    empty_data = {
        "label": str('Not Found'),
        "language_code": str('Not Found'),
    }

    return [empty_data]


def fill_empty_text_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty text annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty text annotations.
    """     
    # format json    
    empty_data = {
        "description": str('Not Found'),
        "x0": float(0),
        "y0": float(0),
        "x1": float(0),
        "y1": float(0),
        "x2": float(0),
        "y2": float(0),
        "x3": float(0),
        "y3": float(0),
    }

    return [empty_data]


def fill_empty_label_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty label annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty label annotations.
    """     
    # format json    
    empty_data = {
        "description": str('Not Found'),
        "score": float(0),
        "mid": str(''),
        "topicality": float(0),
    }

    return [empty_data]


def fill_empty_logo_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty logo annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty logo annotations.
    """     
    # format json    
    empty_data = {
        "description": str('Not Found'),
        "score": float(0),
        "mid": str(''),
        "x0": float(0),
        "y0": float(0),
        "x1": float(0),
        "y1": float(0),
        "x2": float(0),
        "y2": float(0),
        "x3": float(0),
        "y3": float(0),
    }

    return [empty_data]


def fill_empty_face_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty face annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty face annotations.
    """
    # bounding_poly
    bounding_poly_empty = {
        "x_0": float(0),
        "y_0": float(0),
        "x_1": float(0),
        "y_1": float(0),
        "x_2": float(0),
        "y_2": float(0),
        "x_3": float(0),
        "y_3": float(0)
    }
    
    #landmarks 
    landmark_empty = {
        "type": str('Not Found'),
        "x": float(0),
        "y": float(0),
        "z": float(0)
        
    }
       
    # format json    
    empty_data = {
        "bounding_poly": bounding_poly_empty,
        "fd_bounding_poly": bounding_poly_empty,
        "landmarks": [landmark_empty],
        "roll_angle": float(0),
        "pan_angle": float(0),
        "tilt_angle": float(0),
        "detection_confidence": float(0),
        "landmarking_confidence": float(0),
        "joy_likelihood": float(0),
        "sorrow_likelihood": float(0),
        "anger_likelihood": float(0),
        "surprise_likelihood": float(0),
        "under_exposed_likelihood": float(0),
        "blurred_likelihood": float(0),
        "headwear_likelihood": float(0),
    }

    return [empty_data]


def fill_empty_localized_object_annotations() -> List[Dict[str, Any]]:
    """
    Creates a list with a dictionary representing empty localized object annotations.

    Returns:
        List[Dict[str, Any]]: List containing a dictionary with empty localized object annotations.
    """
    empty_data = {
        "name": str('Not Found'),
        "score": float(0),
        "normalized_x0": float(0),
        "normalized_y0": float(0),
        "normalized_x1": float(0),
        "normalized_y1": float(0),
        "normalized_x2": float(0),
        "normalized_y2": float(0),
        "normalized_x3": float(0),
        "normalized_y3": float(0),
    }

    return [empty_data]


#######


def print_labels(response: vision.AnnotateImageResponse):
    """
    Prints the label annotations from the given Vision API response.
    
    Args:
        response (vision.AnnotateImageResponse): The response from the Vision API containing the label annotations.
    """
    print("=" * 80)
    for label in response.label_annotations:
        print(f"{label.score:4.0%}", f"{label.description:5}", sep=" | ")


def print_text(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for annotation in response.text_annotations:
        vertices = [f"({v.x},{v.y})" for v in annotation.bounding_poly.vertices]
        print(
            f"{repr(annotation.description):42}",
            ",".join(vertices),
            sep=" | ",
        )


def print_landmarks(response: vision.AnnotateImageResponse, min_score: float = 0.5):
    print("=" * 80)
    for landmark in response.landmark_annotations:
        if landmark.score < min_score:
            continue
        vertices = [f"({v.x},{v.y})" for v in landmark.bounding_poly.vertices]
        lat_lng = landmark.locations[0].lat_lng
        print(
            f"{landmark.description:18}",
            ",".join(vertices),
            f"{lat_lng.latitude:.5f}",
            f"{lat_lng.longitude:.5f}",
            sep=" | ",
        )


def print_objects(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for obj in response.localized_object_annotations:
        nvertices = obj.bounding_poly.normalized_vertices
        print(
            f"{obj.score:4.0%}",
            f"{obj.name:15}",
            f"{obj.mid:10}",
            ",".join(f"({v.x:.1f},{v.y:.1f})" for v in nvertices),
            sep=" | ",
        )

    
def print_faces(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for face_number, face in enumerate(response.face_annotations, 1):
        vertices = ",".join(f"({v.x},{v.y})" for v in face.bounding_poly.vertices)
        print(f"# Face {face_number} @ {vertices}")
        print(f"Joy:     {face.joy_likelihood.name}")
        print(f"Exposed: {face.under_exposed_likelihood.name}")
        print(f"Blurred: {face.blurred_likelihood.name}")
        print("-" * 80)