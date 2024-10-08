# import pyodbc
# import cohere
# from flask import Blueprint, request, jsonify
# from huggingface_hub import InferenceClient
# import random
# import io
# import requests
# import base64
# import json
# import logging

# # Database Connection Functions
# def get_db_connection(db_name='default'):
#     conn = pyodbc.connect(
#         "DRIVER={SQL Server};"
#         "SERVER=DESKTOP-CHL4PUV\\SQLEXPRESS;"  # Escaped the backslash
#         "DATABASE=smartforge;" if db_name == 'default' else "DATABASE=metadata;"
#         "Trusted_Connection=yes;"              # Using Windows Authentication
#     )
#     return conn

# def execute_db_query(query, params, db_name='default', return_id=False):
#     """Execute a database query with the given parameters."""
#     try:
#         with get_db_connection(db_name) as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             conn.commit()
#             if return_id:
#                 # Get the last inserted ID using SCOPE_IDENTITY()
#                 cursor.execute("SELECT SCOPE_IDENTITY()")
#                 return cursor.fetchone()[0]  # Return the ID of the last inserted row
#             return None
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         raise  # Re-raise the exception for handling at a higher level

# # Blueprint Setup
# image_gen_bp = Blueprint('image_gen', __name__)
# client = InferenceClient(model="stabilityai/stable-diffusion-2", token="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")

# # Cohere API setup
# cohere_client = cohere.Client('o27Gxwey2InsuP8nyWPOiqyH9csINEE0y4IpbyLc')  # Replace with your Cohere API key

# def generate_random_image(prompt):
#     """Generate a random image based on the given prompt."""
#     seed = random.randint(0, 100000)  # Generate a random seed
#     image = client.text_to_image(prompt, seed=seed)  # Generate image with the prompt and seed
#     return image

# def upload_to_ipfs(image_data):
#     """Upload the given image data to IPFS using Pinata."""
#     url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
#     headers = {
#         "pinata_api_key": "41be460e331d6290e13a",  # Replace with your actual Pinata API Key
#         "pinata_secret_api_key": "d988544381a73c9c39c1f10d351e662e012be7e6bed9024ff8191bff9060e894"  # Replace with your actual Pinata secret API key
#     }
#     files = {
#         'file': ('generated_image.png', image_data, 'image/png')
#     }
#     response = requests.post(url, files=files, headers=headers)
#     if response.status_code == 200:
#         return response.json()["IpfsHash"]
#     else:
#         raise Exception(f"Failed to upload to IPFS: {response.text}")

# @image_gen_bp.route('/generate-image', methods=['POST'])
# def generate_image():
#     """Generate an image based on the prompt provided in the request."""
#     data = request.json
#     prompt = data.get('prompt')
#     if not prompt:
#         return jsonify({'error': 'Prompt is required!'}), 400

#     image = generate_random_image(prompt)
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)

#     return jsonify({'image': base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')})

# @image_gen_bp.route('/get-better-suggestion', methods=['POST'])
# def get_better_suggestion():
#     """Get a better suggestion for the provided prompt."""
#     data = request.json
#     prompt = data.get('prompt')
#     if not prompt:
#         return jsonify({'error': 'Prompt is required!'}), 400

#     try:
#         instruction = "Please rewrite the following prompt to be concise and keep it under 250 characters:\n"
#         full_prompt = instruction + prompt

#         response = cohere_client.generate(
#             model='command-xlarge-nightly',
#             prompt=full_prompt,
#             max_tokens=50,
#             temperature=0.75,
#             k=0,
#             p=0.75
#         )

#         better_prompt = response.generations[0].text.strip()
#         return jsonify({'better_prompt': better_prompt})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @image_gen_bp.route('/create-nft', methods=['POST'])
# def create_nft():
#     """Create an NFT using the generated image and prompt."""
#     data = request.json
#     prompt = data.get('prompt')
#     image_base64 = data.get('image')

#     if not prompt or not image_base64:
#         return jsonify({'error': 'Prompt and image are required!'}), 400

#     try:
#         image_data = base64.b64decode(image_base64)
#         nft_cid = upload_to_ipfs(image_data)

#         # Save the CID and prompt into the images database
#         nft_id = execute_db_query("INSERT INTO images (prompt, cid) VALUES (?, ?)", (prompt, nft_cid), return_id=True)

#         return jsonify({'message': 'NFT created successfully!', 'cid': nft_cid, 'nft_id': nft_id})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @image_gen_bp.route('/create-metadata', methods=['POST'])
# def create_metadata():
#     """Create metadata for the NFT."""
#     data = request.json
#     name = data.get('name')
#     prompt = data.get('prompt')
#     nft_cid = data.get('nft_cid')

#     if not name or not prompt or not nft_cid:
#         return jsonify({'error': 'Name, prompt, and NFT CID are required!'}), 400

#     try:
#         metadata = {
#             "name": name,
#             "description": prompt,
#             "nft_cid": nft_cid
#         }
#         json_data = json.dumps(metadata)
#         json_cid = upload_to_ipfs(json_data.encode('utf-8'))

#         execute_db_query("INSERT INTO metadata (nft_cid, json_cid) VALUES (?, ?)", (nft_cid, json_cid))

#         return jsonify({'message': 'Metadata created successfully!', 'json_cid': json_cid})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

import pyodbc
import cohere
from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient
import random
import io
import requests
import base64
import json
import logging
import os

# Database Connection Functions
def get_db_connection(db_name='default'):
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-CHL4PUV\\SQLEXPRESS;"
        "DATABASE=smartforge;" if db_name == 'default' else "DATABASE=metadata;"
        "Trusted_Connection=yes;"
    )
    return conn

def execute_db_query(query, params, db_name='default', return_id=False):
    """Execute a database query with the given parameters."""
    try:
        with get_db_connection(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if return_id:
                cursor.execute("SELECT SCOPE_IDENTITY()")
                return cursor.fetchone()[0]
            return None
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        raise

# Blueprint Setup
image_gen_bp = Blueprint('image_gen', __name__)
client = InferenceClient(model="stabilityai/stable-diffusion-2", token="")
cohere_client = cohere.Client('')

def generate_random_image(prompt):
    """Generate a random image based on the given prompt."""
    seed = random.randint(0, 100000)
    image = client.text_to_image(prompt, seed=seed)
    return image

def upload_to_ipfs(image_data):
    """Upload the given image data to IPFS using Pinata."""
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": "",
        "pinata_secret_api_key": ""
    }
    files = {
        'file': ('generated_image.png', image_data, 'image/png')
    }
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception(f"Failed to upload to IPFS: {response.text}")

def write_metadata_to_json(name, description, cid, file_path='nft_metadata.json'):
    """Create a JSON file with the NFT metadata."""
    metadata = {
        "name": name,
        "description": description,
        "image": f"ipfs://{cid}"
    }
    
    with open(file_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    
    return file_path

@image_gen_bp.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate an image based on the prompt provided in the request."""
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required!'}), 400

    image = generate_random_image(prompt)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return jsonify({'image': base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')})

@image_gen_bp.route('/get-better-suggestion', methods=['POST'])
def get_better_suggestion():
    """Get a better suggestion for the provided prompt."""
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required!'}), 400

    try:
        instruction = "Please rewrite the following prompt to be concise and keep it under 250 characters:\n"
        full_prompt = instruction + prompt

        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=full_prompt,
            max_tokens=50,
            temperature=0.75,
            k=0,
            p=0.75
        )

        better_prompt = response.generations[0].text.strip()
        return jsonify({'better_prompt': better_prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@image_gen_bp.route('/create-nft', methods=['POST'])
def create_nft():
    """Create an NFT using the generated image and prompt."""
    data = request.json
    prompt = data.get('prompt')
    image_base64 = data.get('image')

    if not prompt or not image_base64:
        return jsonify({'error': 'Prompt and image are required!'}), 400

    try:
        image_data = base64.b64decode(image_base64)
        nft_cid = upload_to_ipfs(image_data)

        # Save the CID and prompt into the images database
        nft_id = execute_db_query("INSERT INTO images (prompt, cid) VALUES (?, ?)", (prompt, nft_cid), return_id=True)

        return jsonify({'message': 'NFT created successfully!', 'cid': nft_cid, 'nft_id': nft_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@image_gen_bp.route('/create-metadata', methods=['POST'])
def create_metadata():
    """Create metadata for the NFT and save it to a JSON file."""
    data = request.json
    name = data.get('name')
    prompt = data.get('prompt')
    nft_cid = data.get('nft_cid')

    if not name or not prompt or not nft_cid:
        return jsonify({'error': 'Name, prompt, and NFT CID are required!'}), 400

    try:
        # Create and save the metadata to JSON file
        json_file_path = write_metadata_to_json(name, prompt, nft_cid)

        # Upload the metadata JSON to IPFS
        with open(json_file_path, 'rb') as json_file:
            json_data = json_file.read()
            json_cid = upload_to_ipfs(json_data)

        # Save the CID and prompt into the metadata database
        execute_db_query("INSERT INTO metadata (nft_cid, json_cid) VALUES (?, ?)", (nft_cid, json_cid))

        return jsonify({'message': 'Metadata created successfully!', 'json_cid': json_cid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
