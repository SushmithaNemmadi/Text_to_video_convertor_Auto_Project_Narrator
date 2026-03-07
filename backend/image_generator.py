import requests
import os

# CORRECT COLAB URL (IMPORTANT)
COLAB_URL = "https://saylor-semiautonomous-adelyn.ngrok-free.dev/generate"


def read_prompts():

    file_path = "data/visual_prompts.txt"

    with open(file_path, "r") as f:
        prompts = f.readlines()

    # Remove empty lines and unwanted text
    prompts = [p.strip() for p in prompts if p.strip() and "Scene" not in p and "**" not in p]

    return prompts


def clear_old_images(folder):
    """Delete all old images before generating new ones"""
    
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            
            # Remove only image files
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                os.remove(file_path)
                print("Deleted old image:", file_path)


def generate_images():

    prompts = read_prompts()

    # Save images in images folder
    output_folder = "images"

    os.makedirs(output_folder, exist_ok=True)

    # 🔥 Remove old images first
    clear_old_images(output_folder)

    for i, prompt in enumerate(prompts):

        print("Generating:", prompt)

        response = requests.post(
            COLAB_URL,
            json={"prompt": prompt}
        )

        image_path = os.path.join(output_folder, f"image_{i}.png")

        with open(image_path, "wb") as f:
            f.write(response.content)

        print("Saved:", image_path)


if __name__ == "__main__":
    generate_images()