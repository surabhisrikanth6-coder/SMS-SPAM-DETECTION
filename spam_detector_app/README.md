# 🛡️ SpamShield – Streamlit Web App

A sleek, dark-themed spam detection web application powered by your Naïve Bayes + TF-IDF model.

---

## 📁 Project Structure

```
spam_detector_app/
├── app.py                      ← Main Streamlit app
├── save_model.py               ← Colab helper to export model files
├── requirements.txt            ← Python dependencies
├── spam_classifier_model.joblib  ← (you provide this)
└── tfidf_vectorizer.joblib       ← (you provide this)
```

---

## 🚀 Step-by-Step Setup

### Step 1 — Export model files from Google Colab

Open your Colab notebook and add a **new cell** at the very end with this code:

```python
import joblib
from google.colab import files

joblib.dump(model, 'spam_classifier_model.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

files.download('spam_classifier_model.joblib')
files.download('tfidf_vectorizer.joblib')
```

Run the cell — two `.joblib` files will be downloaded to your computer.

---

### Step 2 — Set up the project in VS Code

1. Create a folder called `spam_detector_app` anywhere on your computer.
2. Place these files inside it:
   - `app.py`
   - `requirements.txt`
   - `spam_classifier_model.joblib`   ← downloaded from Colab
   - `tfidf_vectorizer.joblib`        ← downloaded from Colab

---

### Step 3 — Create a virtual environment (recommended)

Open the `spam_detector_app` folder in VS Code terminal (`Ctrl+\``):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Run the app

```bash
streamlit run app.py
```

The browser will automatically open at **http://localhost:8501**

---

## 🎨 Features

- **Dark space-themed UI** with violet + teal accent palette
- **One-click sample messages** to test the model instantly
- **Animated result cards** — red for spam, green for safe
- **Confidence bar** showing model certainty
- **Recent checks history** panel (last 6 analyses)
- Fully responsive layout

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `Model files not found` warning | Make sure `.joblib` files are in the **same folder** as `app.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Port already in use | Run `streamlit run app.py --server.port 8502` |
| Old cached model | Press `Ctrl+C`, then re-run `streamlit run app.py` |
