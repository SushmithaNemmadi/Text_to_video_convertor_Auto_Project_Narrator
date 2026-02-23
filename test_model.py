from transformers import pipeline

pipe = pipeline("text-generation", model="./project_llm")

result = pipe(
    "Generate project storyboard for smart irrigation system",
    max_length=200
)

print(result[0]["generated_text"])