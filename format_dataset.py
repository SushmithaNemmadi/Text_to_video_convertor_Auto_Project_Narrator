from datasets import load_dataset

dataset = load_dataset("json", data_files="dataset/project_training.jsonl")

def format_example(example):
    text = f"""
Instruction: {example['instruction']}
Input: {example['input']}
Output: {example['output']}
"""
    return {"text": text}

dataset = dataset.map(format_example)

dataset["train"].to_json("dataset/formatted_data.json")

print("✅ Dataset formatted")