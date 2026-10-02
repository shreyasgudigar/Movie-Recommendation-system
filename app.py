import pickle
import streamlit as st
import requests
import pandas as pd

# ─────────────────────────────────────────────
#  Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Discover Your Next Favourite Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  Custom CSS – Dark Glassmorphism Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');

/* ── Global Reset ── */
* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080818;
    font-family: 'Outfit', sans-serif;
    color: #e8e8f0;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #1a0533 0%, #080818 45%),
                radial-gradient(ellipse at 80% 90%, #0a1a40 0%, transparent 60%);
    min-height: 100vh;
}

/* Hide Streamlit default header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Section ── */
.hero-wrapper {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
}
.hero-logo {
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #bf5fff 0%, #5f8fff 50%, #5fffd4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-tagline {
    font-size: 1.1rem;
    font-weight: 300;
    color: #8888aa;
    letter-spacing: 0.5px;
    margin-bottom: 2.5rem;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #5f8fff44, #bf5fff44, transparent);
    margin: 0 auto 2.5rem;
    max-width: 600px;
}

/* ── Selectbox Override ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(191,95,255,0.3) !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.2rem 0.5rem !important;
    transition: border-color 0.3s ease !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(191,95,255,0.7) !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #8a2be2, #5f8fff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.65rem 2.5rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(138,43,226,0.4) !important;
    margin-top: 0.5rem !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(138,43,226,0.65) !important;
}

/* ── Section Title ── */
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #d0d0ee;
    margin: 2.5rem 0 1.2rem;
    text-align: center;
    letter-spacing: 0.3px;
}
.section-title span {
    color: #bf5fff;
}

/* ── Movie Card ── */
.movie-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}
.movie-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(191,95,255,0.07), rgba(95,143,255,0.07));
    opacity: 0;
    transition: opacity 0.35s ease;
    border-radius: 18px;
}
.movie-card:hover {
    transform: translateY(-6px);
    border-color: rgba(191,95,255,0.45);
    box-shadow: 0 12px 40px rgba(138,43,226,0.25);
}
.movie-card:hover::before { opacity: 1; }

.movie-poster {
    width: 100%;
    border-radius: 12px;
    object-fit: cover;
    aspect-ratio: 2/3;
    margin-bottom: 0.75rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
.movie-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8e8f0;
    margin-bottom: 0.35rem;
    line-height: 1.3;
    min-height: 2.4em;
}
.movie-meta {
    font-size: 0.78rem;
    color: #7777aa;
    margin-bottom: 0.25rem;
}
.movie-rating {
    font-size: 0.82rem;
    color: #f5c842;
    font-weight: 600;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 3rem 1rem 2rem;
    color: #44445a;
    font-size: 0.8rem;
    letter-spacing: 0.3px;
}
.footer strong { color: #6655aa; }

/* ── Spinner Override ── */
[data-testid="stSpinner"] { color: #bf5fff !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
POSTER_BASE   = "https://image.tmdb.org/t/p/w500"
FALLBACK_IMG  = "https://placehold.co/300x450/1a1a2e/8888aa?text=No+Poster"


def fetch_poster(movie_id: int) -> str:
    """Return the TMDB poster URL for a given movie_id."""
    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={TMDB_API_KEY}&language=en-US"
        )
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        path = resp.json().get("poster_path")
        if path:
            return f"{POSTER_BASE}{path}"
    except Exception:
        pass
    return FALLBACK_IMG


def star_rating(score: float) -> str:
    """Convert a 0-10 score to filled/empty stars (out of 5)."""
    filled = round(score / 2)
    return "★" * filled + "☆" * (5 - filled)


def recommend(movie: str):
    """Return top-5 similar movies for the given title."""
    try:
        idx = movies[movies["title"] == movie].index[0]
    except IndexError:
        return [], [], [], []

    distances = sorted(
        enumerate(similarity[idx]), key=lambda x: x[1], reverse=True
    )

    names, posters, years, ratings = [], [], [], []
    for i, _ in distances[1:6]:
        mid = movies.iloc[i].movie_id
        posters.append(fetch_poster(mid))
        names.append(movies.iloc[i].title)
        years.append(movies.iloc[i].get("year", None))
        ratings.append(movies.iloc[i].get("vote_average", 0.0))

    return names, posters, years, ratings


# ─────────────────────────────────────────────
#  Load Model Artifacts
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    movie_dict  = pickle.load(open("artifacts/movie_dict.pkl", "rb"))
    movies_df   = pd.DataFrame(movie_dict)
    try:
        sim = pickle.load(open("artifacts/similarity.pkl", "rb"))
    except FileNotFoundError:
        sim = None
    return movies_df, sim


try:
    movies, similarity = load_artifacts()
except FileNotFoundError:
    st.error("⚠️  Model files not found. Please generate the artifacts first.")
    st.stop()

if similarity is None:
    st.error("⚠️  similarity.pkl not found. Please run the data-processing notebook.")
    st.stop()


# ─────────────────────────────────────────────
#  Hero Section
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-logo">🎬 CineMatch</div>
    <div class="hero-tagline">Discover your next favourite film</div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Search Controls
# ─────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    selected_movie = st.selectbox(
        "🔍  Search for a movie",
        movies["title"].values,
        label_visibility="collapsed",
        placeholder="Type or select a movie…",
    )
    find_btn = st.button("✨  Find Similar Movies", use_container_width=True)


# ─────────────────────────────────────────────
#  Recommendation Results
# ─────────────────────────────────────────────
if find_btn:
    with st.spinner("Finding the perfect matches for you…"):
        names, posters, years, ratings = recommend(selected_movie)

    if not names:
        st.warning("No recommendations found. Please try a different title.")
    else:
        st.markdown(
            f'<div class="section-title">Movies similar to <span>{selected_movie}</span></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(5, gap="medium")
        for i, col in enumerate(cols):
            with col:
                year_str   = str(int(years[i])) if years[i] and pd.notna(years[i]) else "N/A"
                rating_val = ratings[i] if ratings[i] else 0.0
                stars      = star_rating(float(rating_val))

                st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" class="movie-poster" alt="{names[i]}">
                    <div class="movie-title">{names[i]}</div>
                    <div class="movie-meta">📅 {year_str}</div>
                    <div class="movie-rating">{stars} &nbsp;{rating_val:.1f}</div>
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <strong>CineMatch</strong> &nbsp;·&nbsp; Content-Based Movie Recommendation Engine<br>
    Powered by TMDB API &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
