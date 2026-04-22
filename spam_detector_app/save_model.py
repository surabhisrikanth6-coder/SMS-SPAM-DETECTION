"""
save_model.py  –  Run this ONCE in Google Colab BEFORE downloading the model.

Add this cell at the end of your Colab notebook and run it.
It saves both the model AND the vectorizer so the Streamlit app can use them.
"""

import joblib

# ── Save the trained model ────────────────────────────────────────────────────
model_path = 'spam_classifier_model.joblib'
joblib.dump(model, model_path)
print(f"✅ Model saved → {model_path}")

# ── Save the TF-IDF vectorizer ────────────────────────────────────────────────
vec_path = 'tfidf_vectorizer.joblib'
joblib.dump(vectorizer, vec_path)
print(f"✅ Vectorizer saved → {vec_path}")

# ── Download both files ───────────────────────────────────────────────────────
from google.colab import files
files.download(model_path)
files.download(vec_path)

print("\n🎉 Both files downloaded! Place them next to app.py in VS Code.")
