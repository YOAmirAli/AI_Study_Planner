"""
Custom T5-small model for flashcard generation.
Loads fine-tuned weights from backend/models/flashcard_model/final/
Falls back to base t5-small, then rule-based cards if torch is unavailable.
"""

import os
import re

BACKEND_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
MODEL_DIR = os.path.join(BACKEND_ROOT, "models", "flashcard_model", "final")


class CustomFlashcardModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._torch_available = False
        self.provider_label = "Rule-based fallback"
        self.load_model()

    def load_model(self):
        try:
            import torch
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

            self._torch_available = True

            if os.path.isdir(MODEL_DIR) and os.path.isfile(
                os.path.join(MODEL_DIR, "config.json")
            ):
                self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
                self.provider_label = "Custom T5 fine-tuned model"
                print(f"[OK] Flashcard model loaded from {MODEL_DIR}")
            else:
                print("[INFO] Fine-tuned model not found; using t5-small base")
                self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
                self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
                self.provider_label = "T5-small (base, not fine-tuned)"
        except ImportError:
            print("[INFO] torch/transformers not installed; rule-based flashcards only")

    def generate_flashcards(self, text: str, num_cards: int = 10) -> list:
        if self._torch_available and self.model and self.tokenizer:
            cards = self._generate_with_model(text, num_cards)
            if len(cards) >= min(3, num_cards):
                return cards[:num_cards]
        return self._generate_rule_based(text, num_cards)

    def _generate_with_model(self, text: str, num_cards: int) -> list:
        import torch

        flashcards = []
        sentences = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", text)
            if len(s.split()) >= 6
        ][: max(num_cards * 2, num_cards)]

        for sentence in sentences:
            if len(flashcards) >= num_cards:
                break
            input_text = f"generate flashcard: {sentence[:400]}"
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                max_length=256,
                truncation=True,
            )
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_length=128,
                    num_beams=2,
                    early_stopping=True,
                )
            decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            card = self._parse_card_output(decoded, sentence)
            if card:
                flashcards.append(card)

        return flashcards[:num_cards]

    def _parse_card_output(self, decoded: str, fallback_sentence: str) -> dict | None:
        decoded = decoded.strip()
        if not decoded:
            return None

        q_match = re.search(r"Question:\s*(.+?)(?:\nAnswer:|$)", decoded, re.I | re.S)
        a_match = re.search(r"Answer:\s*(.+)$", decoded, re.I | re.S)

        if q_match and a_match:
            return {
                "question": q_match.group(1).strip(),
                "answer": a_match.group(1).strip(),
                "category": "Generated",
            }

        if "?" in decoded:
            parts = decoded.split("?", 1)
            return {
                "question": parts[0].strip() + "?",
                "answer": parts[1].strip() or fallback_sentence[:150],
                "category": "Generated",
            }

        return {
            "question": decoded[:120],
            "answer": fallback_sentence[:200],
            "category": "General",
        }

    def _generate_rule_based(self, text: str, num_cards: int) -> list:
        flashcards = []
        sentences = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", text)
            if len(s.strip()) > 25
        ]

        for sentence in sentences[:num_cards]:
            words = sentence.split()
            key_term = words[min(3, len(words) - 1)] if words else "topic"
            flashcards.append(
                {
                    "question": f"Explain: {key_term} (from this topic)",
                    "answer": sentence[:250],
                    "category": "General",
                }
            )

        return flashcards[:num_cards]


_custom_model = None


def get_custom_model() -> CustomFlashcardModel:
    global _custom_model
    if _custom_model is None:
        _custom_model = CustomFlashcardModel()
    return _custom_model
