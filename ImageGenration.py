import asyncio
import os
import logging
import requests
import time
import cv2 as cv
from random import choice
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API Key
API_KEY = os.getenv("HuggingFaceAPIKey")
if not API_KEY:
    logging.error(" API Key not found. Set it in environment variables.")

# Hugging Face API URL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Image Prompt Variations
VARIATIONS = [
    "cinematic lighting, ultra-realistic, 8K details",
    "digital painting, concept art, vibrant colors",
    "realistic photography, studio lighting, depth of field",
    "cyberpunk style, neon glow, futuristic theme",
    "fantasy art, mystical ambiance, high fantasy",
    "black and white, dramatic contrast, moody lighting"
]

def open_image(prompt):
    """Opens generated images from the Data folder."""
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}_v{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            logging.info(f"Opening image: {image_path}")
            img.show()
            time.sleep(1)
        except IOError:
            logging.error(f" Unable to open {image_path}")

async def query(payload):
    """Makes an API request to Hugging Face for image generation."""
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)

        # Handle rate limit (429 Too Many Requests)
        if response.status_code == 429:
            logging.warning("⚠ Too many requests! Retrying in 10 seconds...")
            await asyncio.sleep(10)
            response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)

        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None  # Handle failed requests properly

async def generate_image(prompt: str):
    """Generates 4 variations of an image asynchronously."""
    tasks = []
    for i in range(4):
        variation = choice(VARIATIONS)
        full_prompt = f"{prompt}, {variation}"  # Add style variations
        payload = {
            "inputs": full_prompt,
            "parameters": {"num_inference_steps": 50}
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}_v{i+1}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            logging.info(f" Image saved: {file_path}")
        else:
            logging.error(f"Skipping image {i+1} due to failed API response.")

def generate_images(prompt: str):
    """Runs the image generation process and displays images."""
    asyncio.run(generate_image(prompt))
    open_image(prompt)

def images_to_video(prompt, frame_rate=10):
    """Converts generated images into a smooth video and plays it."""
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")

    # Collect all images
    image_files = sorted([img for img in os.listdir(folder_path) if img.endswith(".jpg")])
    image_paths = [os.path.join(folder_path, img) for img in image_files]

    if not image_paths:
        logging.error("No images found for video generation!")
        return None

    # Open first image to get dimensions
    first_image = Image.open(image_paths[0])
    width, height = first_image.size

    # Define Video Codec & Create Video Writer
    video_filename = os.path.join("Data", f"{prompt}.mp4")
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_writer = cv.VideoWriter(video_filename, fourcc, frame_rate, (width, height))

    # Add images to the video
    for img_path in image_paths:
        img = cv.imread(img_path)
        if img is None:
            logging.warning(f" Skipping missing image: {img_path}")
            continue
        video_writer.write(img)

    video_writer.release()
    logging.info(f" Video saved: {video_filename}")
    return video_filename

def play_video(video_path):
    """Plays the generated video automatically using OpenCV."""
    if not os.path.exists(video_path):
        logging.error(" Video Not Found!")
        return

    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(" OpenCV Cannot Read the Video!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  
        
        cv.imshow(" Playing Video", frame)

        if cv.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()

def generate_video_from_images():
    """Runs the entire process: AI Image Generation → Video Creation → Auto Play"""
    file_path = "/home/my/nova/frontend/Files/ImageGeneration.data"

    while True:
        try:
            if not os.path.exists(file_path):
                logging.warning(" File ImageGeneration.data not found, waiting...")
                time.sleep(2)
                continue
            
            with open(file_path, "r") as f:
                data = f.read().strip()
            
            if not data:
                logging.warning("⚠ Empty file content, retrying...")
                time.sleep(2)
                continue

            prompt, status = data.split(",")

            if status.strip().lower() == "true":
                logging.info(f" Generating image for prompt: {prompt.strip()}...")
                generate_images(prompt.strip())

                # Now create video
                logging.info(f" Creating video from images...")
                video_path = images_to_video(prompt.strip())

                if video_path:
                    logging.info(f"Playing video automatically...")
                    play_video(video_path)  # 🔹 **Added for Auto Play**
                
                # Update status in file
                with open(file_path, "w") as f:
                    f.write("False,False")
                break
            else:
                time.sleep(1)

        except FileNotFoundError:
            logging.error(" File not found. Retrying...")
            time.sleep(2)
        except Exception as e:
            logging.error(f"⚠Unexpected error: {e}")
            time.sleep(2)

# Run the Full AI Pipeline
if __name__ == "__main__":
    generate_video_from_images()
