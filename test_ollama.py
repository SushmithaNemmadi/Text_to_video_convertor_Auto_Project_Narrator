import ollama

response = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response["message"]["content"])