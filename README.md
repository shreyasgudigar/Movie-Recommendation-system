# CineMatch 🎬

> **Discover your next favourite film** — a content-based movie recommendation engine built with Python and Streamlit.

## Features

- 🔍 Search from thousands of movies
- 🎯 Content-based filtering using cosine similarity
- 🖼️ Live poster fetching via TMDB API
- ⭐ Ratings and release year for every recommendation
- 🌙 Modern dark glassmorphism UI

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate model artifacts
Open and run the Jupyter notebook to generate `artifacts/similarity.pkl`.

### 3. Run the app
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit + Custom CSS |
| ML | Scikit-learn (cosine similarity) |
| Data | TMDB Dataset |
| API | TMDB REST API |

## License

MIT License — see [LICENSE](LICENSE) for details.
