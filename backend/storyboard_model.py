import re


# ---------- Extract important words ----------
def extract_keywords(text):
    words = text.lower().split()

    important = []

    tech_words = [
        "ai","machine learning","sensor","data","analytics",
        "traffic","health","prediction","monitoring",
        "detection","system","analysis","automation",
        "network","security","blockchain","database"
    ]

    for word in words:
        if word in tech_words:
            important.append(word)

    return list(set(important))


# ---------- Extract components ----------
def detect_components(text):

    components = []

    if "ai" in text.lower():
        components.append("AI Engine")

    if "sensor" in text.lower():
        components.append("Sensors")

    if "data" in text.lower():
        components.append("Data Processing Module")

    if "database" in text.lower():
        components.append("Database")

    if "app" in text.lower():
        components.append("Frontend Application")

    if len(components) == 0:
        components.append("Processing System")

    return components


# ---------- Generate dynamic storyboard ----------
def generate_storyboard(project_text):

    keywords = extract_keywords(project_text)
    components = detect_components(project_text)

    keyword_text = ", ".join(keywords) if keywords else "advanced technology"
    component_text = ", ".join(components)

    storyboard = f"""
=========== STORYBOARD ===========

Project: {project_text}

Scene 1 – Introduction
Narration: The project '{project_text}' aims to solve real-world problems using {keyword_text}. It improves efficiency, automation, and decision making. The system addresses challenges faced in existing manual processes.
Visual: Animated title screen showing project name.

Scene 2 – Problem Explanation
Narration: Traditional systems face limitations such as inefficiency, slow processing, and lack of automation. The project provides an intelligent solution using {keyword_text} to overcome these challenges.
Visual: Illustration showing real-world problem.

Scene 3 – System Architecture
Narration: The system architecture includes {component_text}. These components interact to collect data, process information, and generate results efficiently.
Visual: Block diagram showing system components connected.

Scene 4 – Workflow Demonstration
Narration: The system collects input data, processes it using internal modules, and produces optimized output. Users interact with the system to obtain results.
Visual: Data flow from input to output.

Scene 5 – Processing / AI Logic
Narration: The system processes data using {keyword_text}. It analyzes patterns, performs computations, and generates intelligent decisions.
Visual: Input → Processing → Output diagram.

Scene 6 – Conclusion & Benefits
Narration: The project improves efficiency, accuracy, and automation. It provides scalable solutions and has potential for future enhancements.
Visual: Benefits summary slide.
"""

    return storyboard