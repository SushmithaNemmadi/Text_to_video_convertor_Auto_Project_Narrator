import ollama
import os
import re

print("=== ProjVision Part 1: Universal Explainer Storyboard Generator ===")


def generate_storyboard(project_text):

    prompt = f"""
You are a professional technical explainer script writer.

Create a 6-scene animated explainer storyboard for the following project.

The storyboard must ALWAYS follow this structure:

Scene 1 – Introduction
Narration:
Introduce the project name, its purpose, and the main problem it addresses.

Visual:
Animated title screen showing the project name and a short problem statement.

Scene 2 – Problem Explanation
Narration:
Explain the real-world problem in detail and why it needs a solution.

Visual:
Illustration clearly representing the real-world problem related to the project.

Scene 3 – System Architecture
Narration:
Explain the overall system architecture including main components such as frontend, backend, AI engine, database, APIs, sensors, or modules depending on the project.

Visual:
Clear block diagram showing system components connected with arrows.

Scene 4 – Workflow Demonstration
Narration:
Explain step-by-step how the system works from user input to final output.

Visual:
User interacting with the system, data being processed, and output generated.

Scene 5 – Processing / AI Logic
Narration:
Explain how the AI, machine learning model, or internal processing logic solves the problem.

Visual:
Simplified processing flow diagram showing input, processing, and output.

Scene 6 – Conclusion & Benefits
Narration:
Summarize the project’s benefits, innovation, practical applications, and future scope.

Visual:
Clean summary slide highlighting key benefits and impact.

Project Description:
{project_text}

IMPORTANT RULES:
- Narration must contain 3 to 4 informative sentences per scene.
- Narration must clearly explain what the system does and how it solves the problem.
- Visual must be short, clear, and suitable for animated or diagram-style image generation.
- Visual should not be artistic or cinematic.
- Adapt explanations specifically to the given project.
- Do NOT generate generic text.

FORMAT EXACTLY LIKE:

Scene 1:
Narration:
Visual:

Scene 2:
Narration:
Visual:

Scene 3:
Narration:
Visual:

Scene 4:
Narration:
Visual:

Scene 5:
Narration:
Visual:

Scene 6:
Narration:
Visual:
"""

    response = ollama.chat(
        model="mistral:7b-instruct-q4_0",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def save_files(storyboard):

    os.makedirs("data", exist_ok=True)

    # Save full storyboard
    with open("data/storyboard.txt", "w", encoding="utf-8") as f:
        f.write(storyboard)

    # Extract narration lines
    narrations = re.findall(r"Narration:\s*(.+)", storyboard)

    with open("data/narration.txt", "w", encoding="utf-8") as f:
        for i, line in enumerate(narrations, start=1):
            f.write(f"Scene {i}: {line}\n")

    # Extract visual lines
    visuals = re.findall(r"Visual:\s*(.+)", storyboard)

    with open("data/visual_prompts.txt", "w", encoding="utf-8") as f:
        for line in visuals:
            f.write(line + "\n")

    print("\n✅ storyboard.txt saved")
    print("✅ narration.txt saved")
    print("✅ visual_prompts.txt saved")


if __name__ == "__main__":

    user_input = input("Enter your project idea: ")

    print("\nGenerating structured universal storyboard...\n")

    result = generate_storyboard(user_input)

    print("\n========== GENERATED STORYBOARD ==========\n")
    print(result)

    save_files(result)
