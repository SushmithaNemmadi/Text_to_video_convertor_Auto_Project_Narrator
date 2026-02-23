from backend.storyboard_model import generate_storyboard

project = input("Enter project idea: ")

result = generate_storyboard(project)

print(result)