# 🧠 Visual Tagger – AI-Powered Image Analysis Tool

**Visual Tagger** is a full-stack prototype that extracts structured insights from images using advanced AI models. Ideal for use cases like product labeling and security footage analysis, the system focuses on accuracy, performance, and an intuitive user experience.

---

## 🚀 Features

### 🔧 Backend – FastAPI (Python)

Built with **FastAPI**, the backend enables high-performance, asynchronous image analysis via:

- **POST `/api/v1/analyze`**: Unified endpoint for single or multiple image uploads.
- **Hybrid AI Architecture**:
  - **ViT (Visual Transformer)**: General object classifier.
  - **CLIP (Zero-Shot)**: Handles abstract or custom tags via prompt-based classification.
- **Tag Aggregation Strategy**:
  - Tags are combined, deduplicated, and sorted by confidence.
  - The **Top 5** most relevant tags are returned.
  - Each tag includes its **source model**.
- **Performance Optimizations**:
  - AI models are cached after first load.
  - Fully asynchronous pipeline.
- **Local-Ready Deployment**: Simple environment setup.

---

### 🎨 Frontend – React + TypeScript

Modern, responsive UI built with **React**, **TypeScript**, and **Tailwind CSS**:

- **Multi-Image Upload**: Drag & drop or file selection.
- **Parallel Analysis**: Images processed concurrently.
- **Results Visualization**:
  - Thumbnails for uploaded images.
  - Tags with confidence percentages.
  - Color-coded feedback:
    - 🟢 High confidence
    - 🟡 Medium
    - 🔴 Low

---

## 🧠 Tagging Logic & AI Strategy

The system maximizes relevance and precision by running **ViT** and **CLIP** in parallel:

1. **Model Strengths**:
   - `ViT`: Precise, fast object recognition.
   - `CLIP`: Broad, contextual, zero-shot capabilities.
2. **Parallel Execution**:
   - Both models run simultaneously.
3. **Smart Aggregation**:
   - All tags above a global threshold are collected.
   - Deduplicated with priority for higher confidence.
   - Sorted and trimmed to Top 5 tags.

This ensures **fast**, **flexible**, and **contextually rich** results.

---

## 🛠 Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Hugging Face Transformers (ViT & CLIP)
- PyTorch
- Pillow (PIL)
- pydantic-settings
- pytest

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- uuid

---

## 📄 License

Licensed under the [MIT License](LICENSE).
