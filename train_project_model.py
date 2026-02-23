from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

print("🚀 Loading tiny model...")

# VERY SMALL MODEL (works fast on laptop)
model_name = "sshleifer/tiny-gpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

print("✅ Model loaded")

# --------------------
# Load dataset
# --------------------
print("📂 Loading dataset...")
dataset = load_dataset("json", data_files="dataset/formatted_data.json")

# --------------------
# Tokenization
# --------------------
def tokenize(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=64   # small = faster
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset = dataset.map(tokenize, batched=True)

print("✅ Dataset ready")

# --------------------
# Training settings
# --------------------
training_args = TrainingArguments(
    output_dir="./project_llm",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    logging_steps=1,
    remove_unused_columns=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

# --------------------
# Train model
# --------------------
print("🔥 Training started...")
trainer.train()

# --------------------
# Save model
# --------------------
print("💾 Saving model...")
model.save_pretrained("./project_llm")
tokenizer.save_pretrained("./project_llm")

print("✅ Training complete!")
print("📁 Model saved in project_llm/")