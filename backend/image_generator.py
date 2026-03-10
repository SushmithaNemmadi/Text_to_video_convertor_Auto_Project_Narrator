import requests
import os

# ==============================
# COLAB SERVER URL
# ==============================

COLAB_URL = "https://saylor-semiautonomous-adelyn.ngrok-free.dev/generate"


# ==============================
# READ VISUAL PROMPTS
# ==============================

def read_prompts():

    file_path = "data/visual_prompts.txt"

    if not os.path.exists(file_path):
        print("visual_prompts.txt not found")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    prompts = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("Scene"):
            continue

        if "**" in line:
            continue

        prompts.append(line)

    print(f"Loaded {len(prompts)} prompts")

    return prompts


# ==============================
# DELETE OLD IMAGES
# ==============================

def clear_old_images(folder):

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):

        file_path = os.path.join(folder, file)

        if file.endswith((".png", ".jpg", ".jpeg")):
            os.remove(file_path)
            print("Deleted:", file_path)


# ==============================
# IMAGE GENERATION
# ==============================

def generate_images():

    prompts = read_prompts()

    if not prompts:
        print("No prompts found")
        return

    output_folder = "images"
    os.makedirs(output_folder, exist_ok=True)

    # remove old images
    clear_old_images(output_folder)

    session = requests.Session()

    for i, prompt in enumerate(prompts):

        print(f"\nGenerating Image {i+1}/{len(prompts)}")

        # small prompt enhancement
        enhanced_prompt = (
            prompt
            + ", ultra detailed, cinematic lighting, dramatic shadows, professional illustration, sharp focus"
        )

        try:

            response = session.post(
                COLAB_URL,
                json={"prompt": enhanced_prompt},
                timeout=300
            )

            if response.status_code != 200:
                print("Server error:", response.text)
                continue

            image_path = os.path.join(output_folder, f"image_{i+1}.png")

            with open(image_path, "wb") as f:
                f.write(response.content)

            print("Saved:", image_path)

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n==============================")
    print("AI IMAGE GENERATOR")
    print("==============================\n")

    generate_images()

    print("\nImage generation finished!")