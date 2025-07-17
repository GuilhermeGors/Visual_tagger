# ⚙️ Backend Mock Mode for Vercel Deployment

This document outlines the modifications made to the project’s backend to enable free deployment on **Vercel**, using a **mocked AI inference** mode.

---

## 🚀 Overview

To overcome the **50MB serverless function limit** imposed by Vercel's free tier, the backend was adapted to simulate Machine Learning inference (e.g., CLIP and ViT). These changes allow the application to run successfully on Vercel while preserving the original backend architecture for use in more capable environments.

---

## 🔧 Changes Made

### 📁 `backend/requirements.txt`
- ❌ Removed heavy libraries: `transformers`, `torch`.
- ✅ Retained only lightweight dependencies required to run the API in mock mode.

---

### 📁 `backend/src/core/dependencies.py`
- 🧠 Removed logic responsible for loading real AI models.
- 🛠️ The `get_all_image_models_and_processors()` function now returns simulated (`None`) objects and logs a message indicating model loading was skipped.

---

### 📁 `backend/src/services/image_analysis.py`
- 🧪 Entire AI-based inference logic replaced with a **mock tag generation** system:
  - Random tag selection from a predefined `mock_tags_pool`.
  - Random confidence values assigned to each tag.
  - Tag source set to `"Mock AI"`.
- ✅ Updated API success message:  
  `"Image analysis completed (Mock AI for Vercel Free Tier)"`
- 📌 Always returns exactly 5 tags per image, even in mock mode.

---

### ⚙️ `vercel.json`
- 📦 `installCommand`: updated to install only remaining lightweight dependencies.
- 🚫 `maxLambdaSize`: set to `50mb`, the maximum allowed by Vercel’s free tier.

---

## ⚠️ Key Implications

| Environment | Behavior |
|-------------|----------|
| **Vercel (Free Tier)** | Runs with **mocked AI**, tags are not contextually accurate. |
| **Locally (with real dependencies)** | Runs with real AI models, providing accurate image analysis based on Machine Learning. |

---

## 💡 Conclusion

This approach ensures:
- ✅ Compatibility with **free-tier environments** (like Vercel).
- 🧱 Architecture ready for **future upgrades** to production-grade environments.
- 🔁 Flexibility to develop and test with real AI models locally without changing the core codebase.

---

To revert to real inference mode, simply restore:
- The full dependencies in `requirements.txt`.
- The original logic in `dependencies.py` and `image_analysis.py`.
