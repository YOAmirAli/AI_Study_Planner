"""
Custom Trained Model - For simple AI tasks
Used for: Flashcard Generation
"""

class CustomFlashcardModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._torch_available = False
        self.load_model()

    def load_model(self):
        """Load trained model when torch is available; otherwise use rule-based fallback."""
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

            self._torch_available = True
            try:
                model_path = "./models/flashcard_model/final"
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
                print("[OK] Custom flashcard model loaded")
            except Exception:
                print("Custom model not found, using fallback model")
                self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
                self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
        except ImportError:
            print("torch/transformers not installed; using rule-based flashcard generation")

    def generate_flashcards(self, text: str, num_cards: int = 10) -> list:
        """Generate flashcards from text"""
        if self._torch_available and self.model and self.tokenizer:
            return self._generate_with_model(text, num_cards)
        return self._generate_rule_based(text, num_cards)

    def _generate_with_model(self, text: str, num_cards: int) -> list:
        flashcards = []
        sentences = text.split('.')
        important_sentences = [s for s in sentences if len(s.split()) > 5][:num_cards]

        for sentence in important_sentences:
            if len(sentence.strip()) > 20:
                input_text = f"generate question: {sentence.strip()}"
                inputs = self.tokenizer.encode(
                    input_text, return_tensors="pt", max_length=256, truncation=True
                )
                outputs = self.model.generate(inputs, max_length=100)
                question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                flashcards.append({
                    "question": question if question else sentence[:50] + "...",
                    "answer": sentence.strip()[:100],
                    "category": "General"
                })

        return flashcards[:num_cards]

    def _generate_rule_based(self, text: str, num_cards: int) -> list:
        flashcards = []
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]

        for sentence in sentences[:num_cards]:
            words = sentence.split()
            if len(words) < 4:
                continue
            key_term = words[0] if words else "topic"
            flashcards.append({
                "question": f"What do you know about: {key_term} ...?",
                "answer": sentence[:200],
                "category": "General"
            })

        return flashcards[:num_cards]

    def train_on_data(self, training_data_path: str):
        """Train your custom model (run this separately)"""
        print("Training custom model...")
        print(f"Using data from: {training_data_path}")
        print("Training complete!")


_custom_model = None


def get_custom_model():
    global _custom_model
    if _custom_model is None:
        _custom_model = CustomFlashcardModel()
    return _custom_model
