"""
Train custom flashcard model
Run this script separately to train your model
"""

import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import Dataset

print("=" * 60)
print("TRAINING CUSTOM FLASHCARD MODEL")
print("=" * 60)

# Create simple training data (you can add more)
training_data = [
    {"text": "Python variables store data values. You create them with the equals sign.", 
     "question": "What do Python variables store?", 
     "answer": "Data values"},
    {"text": "Functions in Python are defined using the def keyword.", 
     "question": "What keyword defines functions in Python?", 
     "answer": "def"},
    {"text": "Lists in Python are ordered, mutable collections.", 
     "question": "Are Python lists mutable?", 
     "answer": "Yes, they can be changed"},
]

# Prepare training examples
examples = []
for item in training_data:
    examples.append({
        "input": f"generate question: {item['text']}",
        "output": f"Question: {item['question']}\nAnswer: {item['answer']}"
    })

# Load model
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenize
def tokenize_function(examples):
    inputs = tokenizer(examples["input"], max_length=256, truncation=True, padding="max_length")
    outputs = tokenizer(examples["output"], max_length=256, truncation=True, padding="max_length")
    inputs["labels"] = outputs["input_ids"]
    return inputs

dataset = Dataset.from_dict({
    "input": [ex["input"] for ex in examples],
    "output": [ex["output"] for ex in examples]
})

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Train
training_args = TrainingArguments(
    output_dir="./models/flashcard_model",
    num_train_epochs=50,
    per_device_train_batch_size=2,
    learning_rate=3e-4,
    logging_steps=10,
    save_steps=100,
    fp16=False,
    no_cuda=True,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

print("Training started...")
trainer.train()

# Save model
model.save_pretrained("./models/flashcard_model/final")
tokenizer.save_pretrained("./models/flashcard_model/final")

print(" Model saved to ./models/flashcard_model/final")