"""
Train T5-small for flashcard Q/A generation.
Run from backend folder: python train_flashcard_model.py

Saves model to: models/flashcard_model/final/
"""

import json
import os

from datasets import Dataset
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments

BACKEND_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_OUTPUT = os.path.join(BACKEND_ROOT, "models", "flashcard_model")
FINAL_DIR = os.path.join(MODEL_OUTPUT, "final")
DATA_PATH = os.path.join(MODEL_OUTPUT, "training_data.json")

TRAINING_DATA = [
    {
        "text": "Python variables store data values. You assign them with the equals sign.",
        "question": "How do you assign a value to a variable in Python?",
        "answer": "Using the equals sign (=)",
    },
    {
        "text": "Functions in Python are defined using the def keyword followed by a name and parentheses.",
        "question": "What keyword defines a function in Python?",
        "answer": "def",
    },
    {
        "text": "Lists in Python are ordered collections that can be changed after creation.",
        "question": "Are Python lists mutable?",
        "answer": "Yes, lists are mutable",
    },
    {
        "text": "A for loop in Python iterates over items in a sequence such as a list or range.",
        "question": "What does a for loop do in Python?",
        "answer": "Iterates over each item in a sequence",
    },
    {
        "text": "Dictionaries in Python store key-value pairs and use curly braces.",
        "question": "What syntax do Python dictionaries use?",
        "answer": "Curly braces with key-value pairs",
    },
    {
        "text": "SQL SELECT statements retrieve data from database tables.",
        "question": "Which SQL command retrieves data?",
        "answer": "SELECT",
    },
    {
        "text": "The WHERE clause in SQL filters rows based on a condition.",
        "question": "What is the purpose of the SQL WHERE clause?",
        "answer": "To filter rows by a condition",
    },
    {
        "text": "A primary key in a relational database uniquely identifies each row in a table.",
        "question": "What is a primary key?",
        "answer": "A column that uniquely identifies each row",
    },
    {
        "text": "JOIN operations in SQL combine rows from two or more tables.",
        "question": "What do SQL JOINs do?",
        "answer": "Combine rows from multiple tables",
    },
    {
        "text": "Normalization reduces data redundancy in database design.",
        "question": "Why normalize a database?",
        "answer": "To reduce redundancy and improve integrity",
    },
    {
        "text": "The Pomodoro Technique uses 25-minute focused work sessions followed by short breaks.",
        "question": "How long is a Pomodoro work session?",
        "answer": "25 minutes",
    },
    {
        "text": "Spaced repetition schedules reviews at increasing intervals to improve long-term memory.",
        "question": "What is spaced repetition?",
        "answer": "Reviewing material at increasing time intervals",
    },
    {
        "text": "Active recall tests yourself without looking at notes, strengthening memory.",
        "question": "What is active recall?",
        "answer": "Retrieving information from memory without cues",
    },
    {
        "text": "Interleaving mixes different topics or problem types in one study session.",
        "question": "What is interleaving in studying?",
        "answer": "Mixing different topics or skills in one session",
    },
    {
        "text": "A growth mindset believes abilities can improve with effort and practice.",
        "question": "What is a growth mindset?",
        "answer": "Belief that abilities improve through effort",
    },
    {
        "text": "Object-oriented programming uses classes and objects to model real-world entities.",
        "question": "What are the main units in OOP?",
        "answer": "Classes and objects",
    },
    {
        "text": "Inheritance allows a child class to reuse attributes and methods from a parent class.",
        "question": "What is inheritance in OOP?",
        "answer": "A child class reusing parent class features",
    },
    {
        "text": "Encapsulation hides internal object details and exposes only necessary interfaces.",
        "question": "What is encapsulation?",
        "answer": "Hiding internal details behind a public interface",
    },
    {
        "text": "An API is an interface that lets applications communicate and exchange data.",
        "question": "What is an API?",
        "answer": "An interface for software to communicate",
    },
    {
        "text": "HTTP GET requests retrieve data from a server without changing server state.",
        "question": "What does an HTTP GET request do?",
        "answer": "Retrieves data from the server",
    },
    {
        "text": "Version control systems like Git track changes to code over time.",
        "question": "What is the purpose of Git?",
        "answer": "Track and manage code changes over time",
    },
    {
        "text": "A commit in Git saves a snapshot of your project at a point in time.",
        "question": "What is a Git commit?",
        "answer": "A saved snapshot of the project",
    },
    {
        "text": "Big O notation describes how algorithm runtime or space grows with input size.",
        "question": "What does Big O notation describe?",
        "answer": "How resource usage scales with input size",
    },
    {
        "text": "A binary search requires a sorted array and halves the search space each step.",
        "question": "What condition does binary search require?",
        "answer": "The data must be sorted",
    },
    {
        "text": "Photosynthesis converts light energy into chemical energy in plants.",
        "question": "What does photosynthesis produce in plants?",
        "answer": "Chemical energy (glucose) from light",
    },
    {
        "text": "Mitochondria are organelles that produce ATP, the cell's energy currency.",
        "question": "What is the main function of mitochondria?",
        "answer": "Produce ATP for cellular energy",
    },
]


def build_examples(data):
    examples = []
    for item in data:
        examples.append(
            {
                "input": f"generate flashcard: {item['text']}",
                "output": f"Question: {item['question']}\nAnswer: {item['answer']}",
            }
        )
    return examples


def main():
    print("=" * 60)
    print("TRAINING CUSTOM FLASHCARD MODEL (T5-small)")
    print("=" * 60)

    os.makedirs(MODEL_OUTPUT, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(TRAINING_DATA, f, indent=2)
    print(f"Saved {len(TRAINING_DATA)} training examples to {DATA_PATH}")

    examples = build_examples(TRAINING_DATA)
    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def tokenize_function(batch):
        model_inputs = tokenizer(
            batch["input"],
            max_length=256,
            truncation=True,
            padding="max_length",
        )
        labels = tokenizer(
            batch["output"],
            max_length=128,
            truncation=True,
            padding="max_length",
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    dataset = Dataset.from_dict(
        {"input": [e["input"] for e in examples], "output": [e["output"] for e in examples]}
    )
    tokenized = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir=MODEL_OUTPUT,
        num_train_epochs=8,
        per_device_train_batch_size=4,
        learning_rate=3e-4,
        logging_steps=5,
        save_strategy="no",
        report_to="none",
        use_cpu=True,
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized)
    print("Training started...")
    trainer.train()

    os.makedirs(FINAL_DIR, exist_ok=True)
    model.save_pretrained(FINAL_DIR)
    tokenizer.save_pretrained(FINAL_DIR)
    print(f"[OK] Model saved to {FINAL_DIR}")


if __name__ == "__main__":
    main()
