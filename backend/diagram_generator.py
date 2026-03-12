import os
import re
import spacy
from graphviz import Digraph

nlp = spacy.load("en_core_web_sm")

INPUT_FILE = "rag_output.txt"
OUTPUT_FOLDER = "images"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------------------
# Get next image number
# ---------------------------
def get_next_image_number():

    files = os.listdir(OUTPUT_FOLDER)

    numbers = []

    for f in files:
        match = re.match(r"image_(\d+)\.png", f)
        if match:
            numbers.append(int(match.group(1)))

    if numbers:
        return max(numbers) + 1
    else:
        return 11   # start numbering from image_11


# ---------------------------
# Extract workflow steps
# ---------------------------
def extract_workflow(text):

    steps = re.findall(r"\d+\.\s*(.*)", text)

    if not steps:
        sentences = text.split(".")
        steps = [s.strip() for s in sentences if len(s.strip()) > 20][:6]

    return steps


# ---------------------------
# Extract technologies
# ---------------------------
def extract_technologies(text):

    tech_keywords = [
        "python","java","c++","javascript","tensorflow","pytorch","keras",
        "react","angular","node","express","mongodb","mysql","aws","docker",
        "kubernetes","pandas","numpy","opencv","flask","django"
    ]

    found = []
    lower = text.lower()

    for tech in tech_keywords:
        if tech in lower:
            found.append(tech.title())

    return list(set(found))


# ---------------------------
# Extract modules
# ---------------------------
def extract_modules(text):

    module_keywords = {
        "frontend": "Frontend Interface",
        "backend": "Backend Server",
        "database": "Database System",
        "ai": "AI Engine",
        "data": "Data Processing",
        "visualization": "Visualization Module",
        "security": "Security Module"
    }

    modules = []
    lower = text.lower()

    for key, module in module_keywords.items():
        if key in lower:
            modules.append(module)

    if not modules:
        modules = [
            "User Interface",
            "Processing Engine",
            "Database",
            "Output"
        ]

    return modules[:6]


# ---------------------------
# Save diagram helper
# ---------------------------
def save_diagram(dot):

    img_num = get_next_image_number()
    filename = f"{OUTPUT_FOLDER}/image_{img_num}"

    dot.render(filename, format="png", cleanup=True)

    print(f"Generated image_{img_num}.png")


# ---------------------------
# Architecture Diagram
# ---------------------------
def architecture_diagram(modules):

    dot = Digraph()
    dot.attr(rankdir="LR")

    dot.node("User")
    prev = "User"

    for i, module in enumerate(modules):
        node = f"M{i}"
        dot.node(node, module)
        dot.edge(prev, node)
        prev = node

    dot.node("Output")
    dot.edge(prev, "Output")

    save_diagram(dot)


# ---------------------------
# Workflow Diagram
# ---------------------------
def workflow_diagram(steps):

    dot = Digraph()

    dot.node("Start")
    prev = "Start"

    for i, step in enumerate(steps):
        node = f"S{i}"
        dot.node(node, step)
        dot.edge(prev, node)
        prev = node

    dot.node("End")
    dot.edge(prev, "End")

    save_diagram(dot)


# ---------------------------
# Technology Diagram
# ---------------------------
def technology_diagram(techs):

    dot = Digraph()

    dot.node("System")

    for i, tech in enumerate(techs):
        node = f"T{i}"
        dot.node(node, tech)
        dot.edge("System", node)

    save_diagram(dot)


# ---------------------------
# Dataflow Diagram
# ---------------------------
def dataflow_diagram(modules):

    dot = Digraph()
    dot.attr(rankdir="LR")

    for i in range(len(modules)-1):
        dot.node(modules[i])
        dot.node(modules[i+1])
        dot.edge(modules[i], modules[i+1])

    save_diagram(dot)


# ---------------------------
# MAIN
# ---------------------------
def main():

    if not os.path.exists(INPUT_FILE):
        print("Input text file not found")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    modules = extract_modules(text)
    steps = extract_workflow(text)
    techs = extract_technologies(text)

    architecture_diagram(modules)
    workflow_diagram(steps)
    technology_diagram(techs)
    dataflow_diagram(modules)


if __name__ == "__main__":
    main()