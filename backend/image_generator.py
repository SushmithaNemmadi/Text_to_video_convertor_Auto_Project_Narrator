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

    prompts = []
    current_prompt = ""

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Detect new scene
        if line.lower().startswith("scene"):

            if current_prompt:
                prompts.append(current_prompt.strip())
                current_prompt = ""

            continue

        # Clean unwanted characters
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace("*", "")
        line = line.strip()

        # Build prompt
        if current_prompt:
            current_prompt += " " + line
        else:
            current_prompt = line

    # Add last prompt
    if current_prompt:
        prompts.append(current_prompt.strip())

    print(f"Loaded {len(prompts)} prompts")

    return prompts


# ==============================
# DELETE OLD IMAGES
# ==============================

def clear_old_images(folder):

    if not os.path.exists(folder):
        return

    deleted = 0

    for file in os.listdir(folder):

        file_path = os.path.join(folder, file)

        if file.endswith((".png", ".jpg", ".jpeg")):
            os.remove(file_path)
            deleted += 1

    if deleted > 0:
        print(f"Deleted {deleted} old images")


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

    # Remove previous images
    clear_old_images(output_folder)

    session = requests.Session()

    for i, prompt in enumerate(prompts):

        print(f"\nGenerating Image {i+1}/{len(prompts)}")

        enhanced_prompt = (
            prompt +
            ", flat vector infographic, educational diagram, "
            "white background, modern UI icons, minimal colors, "
            "professional explainer video style, clean vector illustration, 4k"
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