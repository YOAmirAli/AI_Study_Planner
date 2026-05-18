"""
Verify hybrid AI setup. Run from backend folder:
  python verify_hybrid_ai.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv()

BACKEND = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BACKEND, "models", "flashcard_model", "final")


def check(name, ok, detail=""):
    status = "OK" if ok else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    return ok


def main():
    print("=" * 60)
    print("HYBRID AI VERIFICATION")
    print("=" * 60)
    all_ok = True

    print("\n1. Files")
    files = [
        "app/ai/openai_client.py",
        "app/ai/custom_model.py",
        "app/ai/video_recommender.py",
        "app/services/ai_service.py",
        "train_flashcard_model.py",
    ]
    for f in files:
        path = os.path.join(BACKEND, f)
        all_ok &= check(f, os.path.isfile(path))

    print("\n2. Configuration")
    key = os.getenv("OPENAI_API_KEY", "")
    all_ok &= check("OPENAI_API_KEY", bool(key and not key.startswith("your-")))
    all_ok &= check(
        "Trained flashcard model",
        os.path.isfile(os.path.join(MODEL_DIR, "config.json")),
        MODEL_DIR,
    )

    print("\n3. Imports")
    try:
        from app.services.ai_service import AIService
        from app.ai.openai_client import get_openai_client
        from app.ai.custom_model import get_custom_model
        from app.ai.video_recommender import get_video_recommender

        all_ok &= check("AIService import", True)
        all_ok &= check("OpenAI client import", True)
        all_ok &= check("Custom model import", True)
        all_ok &= check("Video recommender import", True)
    except Exception as e:
        all_ok &= check("Imports", False, str(e))

    print("\n4. Flashcard smoke test (local model)")
    try:
        from app.ai.custom_model import get_custom_model

        m = get_custom_model()
        sample = (
            "Python lists are ordered collections. The append method adds items. "
            "A for loop iterates over sequences in Python programming."
        )
        cards = m.generate_flashcards(sample, 3)
        all_ok &= check(
            "Flashcard generation",
            len(cards) >= 1,
            f"{len(cards)} cards via {m.provider_label}",
        )
    except Exception as e:
        all_ok &= check("Flashcard generation", False, str(e))

    print("\n" + "=" * 60)
    if all_ok:
        print("All checks passed. Hybrid AI is ready.")
    else:
        print("Some checks failed. Fix items marked FAIL before demo.")
    print("=" * 60)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
