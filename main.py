import streamlit as st
import numpy as np
import pandas as pd
from zerve import variable

# ─────────────────────────────────────────────────────────────────────────────
# LOAD CANVAS VARIABLES
# ─────────────────────────────────────────────────────────────────────────────
clean_df       = variable(block_name="recommendation_engine", variable_name="clean_df")
EXP_RANK       = variable(block_name="recommendation_engine", variable_name="EXP_RANK")
PURPOSE_COMPAT = variable(block_name="recommendation_engine", variable_name="PURPOSE_COMPAT")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BikeFit – Find Your Perfect Ride",
    page_icon="🏍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS – modern dark/clean theme, no default Streamlit chrome
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ────────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0f0f12 !important;
    color: #f0f0f5 !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
footer { visibility: hidden; }

/* ── Main container ──────────────────────────────────────────────────────── */
.block-container {
    max-width: 760px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
}

/* ── Hero title ──────────────────────────────────────────────────────────── */
.bf-hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.bf-hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffd400 0%, #ff8c42 50%, #f04438 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}
.bf-hero p {
    color: #909094;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Form card ───────────────────────────────────────────────────────────── */
.bf-form-card {
    background: #1a1a20;
    border: 1px solid #2a2a35;
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 2rem;
}
.bf-section-label {
    color: #909094;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Sliders & selects ───────────────────────────────────────────────────── */
[data-testid="stSlider"] > label,
[data-testid="stSelectbox"] > label {
    color: #d4d4d8 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}
[data-testid="stSlider"] .st-ae { color: #ffd400 !important; }
[data-baseweb="slider"] [role="slider"] {
    background-color: #ffd400 !important;
    border-color: #ffd400 !important;
}
[data-baseweb="select"] [data-testid="stMarkdown"] { color: #f0f0f5 !important; }
[data-baseweb="select"] > div {
    background-color: #22222d !important;
    border-color: #3a3a48 !important;
    color: #f0f0f5 !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] svg { fill: #909094 !important; }
[data-baseweb="popover"] { background: #22222d !important; border-color: #3a3a48 !important; }
[role="option"] { background: #22222d !important; color: #f0f0f5 !important; }
[role="option"]:hover { background: #2e2e3f !important; }

/* ── CTA button ──────────────────────────────────────────────────────────── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 0.85rem 2rem;
    background: linear-gradient(135deg, #ffd400 0%, #ff8c42 100%);
    color: #0f0f12;
    font-size: 1.05rem;
    font-weight: 800;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: opacity 0.2s ease, transform 0.1s ease;
    margin-top: 0.75rem;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}
div[data-testid="stButton"] > button:active { transform: translateY(0); }

/* ── Results header ──────────────────────────────────────────────────────── */
.bf-results-header {
    text-align: center;
    margin: 2rem 0 1.5rem;
}
.bf-results-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f0f0f5;
}
.bf-results-header p { color: #909094; font-size: 0.9rem; margin-top: -0.3rem; }

/* ── Bike recommendation card ────────────────────────────────────────────── */
.bf-card {
    background: #1a1a20;
    border: 1px solid #2a2a35;
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.bf-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ffd400, #ff8c42);
    border-radius: 16px 16px 0 0;
}
.bf-card.rank-2::before { background: linear-gradient(90deg, #a1c9f4, #6baed6); }
.bf-card.rank-3::before { background: linear-gradient(90deg, #8de5a1, #2ca25f); }

.bf-rank-badge {
    display: inline-block;
    width: 28px; height: 28px;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 800;
    line-height: 28px;
    text-align: center;
    margin-right: 10px;
    color: #0f0f12;
    background: linear-gradient(135deg, #ffd400, #ff8c42);
    vertical-align: middle;
}
.bf-rank-badge.rank-2 { background: linear-gradient(135deg, #a1c9f4, #6baed6); }
.bf-rank-badge.rank-3 { background: linear-gradient(135deg, #8de5a1, #2ca25f); }

.bf-bike-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #f0f0f5;
    display: inline;
    vertical-align: middle;
}
.bf-price-tag {
    float: right;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffd400;
}
.bf-meta {
    margin-top: 0.7rem;
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}
.bf-tag {
    background: #22222d;
    border: 1px solid #3a3a48;
    border-radius: 6px;
    padding: 0.2rem 0.55rem;
    font-size: 0.76rem;
    color: #c4c4cf;
    font-weight: 500;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
.bf-score-row {
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.bf-score-label { font-size: 0.78rem; color: #909094; font-weight: 600; white-space: nowrap; }
.bf-score-track {
    flex: 1;
    height: 7px;
    background: #2a2a35;
    border-radius: 99px;
    overflow: hidden;
}
.bf-score-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #ffd400, #ff8c42);
}
.bf-score-fill.rank-2 { background: linear-gradient(90deg, #a1c9f4, #6baed6); }
.bf-score-fill.rank-3 { background: linear-gradient(90deg, #8de5a1, #2ca25f); }
.bf-score-value { font-size: 0.85rem; font-weight: 700; color: #f0f0f5; white-space: nowrap; }

/* ── Explanation ─────────────────────────────────────────────────────────── */
.bf-explanation {
    margin-top: 0.9rem;
    padding: 0.8rem 1rem;
    background: #13131a;
    border-left: 3px solid #3a3a48;
    border-radius: 0 8px 8px 0;
    font-size: 0.83rem;
    color: #c4c4cf;
    line-height: 1.55;
}

/* ── No results ──────────────────────────────────────────────────────────── */
.bf-no-results {
    text-align: center;
    padding: 3rem 2rem;
    background: #1a1a20;
    border: 1px solid #2a2a35;
    border-radius: 16px;
    color: #909094;
}
.bf-no-results span { font-size: 2.5rem; display: block; margin-bottom: 0.75rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE  (mirrors recommendation_engine block logic)
# ─────────────────────────────────────────────────────────────────────────────
def score_bikes(df, budget, rider_height_cm, purpose, experience, category):
    purpose    = purpose.lower().strip()
    experience = experience.lower().strip()
    category   = category.lower().strip()
    exp_rank   = EXP_RANK.get(experience, 1)

    # ── Category + budget filter ──────────────────────────────────────────────
    if category == "both":
        candidates = df[df["price"] <= budget].copy()
    else:
        candidates = df[
            (df["category"].astype(str).str.lower() == category) &
            (df["price"] <= budget)
        ].copy()

    if candidates.empty:
        return pd.DataFrame()

    # ── Budget fit (25%) ──────────────────────────────────────────────────────
    candidates["s_budget"] = (candidates["price"] / budget) ** 0.7

    # ── Seat height fit (20%) – Gaussian, σ=6 cm ─────────────────────────────
    est_inseam = rider_height_cm * 0.47
    sigma      = 6.0
    candidates["s_height"] = np.exp(
        -0.5 * ((candidates["seat_height_cm"] - est_inseam) / sigma) ** 2
    )

    # ── Purpose match (30%) ───────────────────────────────────────────────────
    def _pscore(bike_type):
        bt = str(bike_type).lower()
        if bt == purpose:
            return 1.0
        return PURPOSE_COMPAT.get((purpose, bt), 0.0)

    candidates["s_purpose"] = candidates["type"].astype(str).map(_pscore)

    # ── Experience / weight (15%) ─────────────────────────────────────────────
    candidates["_difficulty"] = (
        0.6 * candidates["weight_norm"] + 0.4 * candidates["cc_norm"]
    )
    if exp_rank == 0:
        candidates["s_exp"] = 1.0 - candidates["_difficulty"]
    elif exp_rank == 1:
        candidates["s_exp"] = 1.0 - 0.4 * candidates["_difficulty"]
    else:
        candidates["s_exp"] = 0.75

    # ── Category fit (10%) ────────────────────────────────────────────────────
    if category == "both":
        candidates["s_category"] = 1.0
    else:
        candidates["s_category"] = (
            candidates["category"].astype(str).str.lower() == category
        ).astype(float)

    # ── Weighted total ────────────────────────────────────────────────────────
    W = {"budget": 0.25, "height": 0.20, "purpose": 0.30, "exp": 0.15, "cat": 0.10}
    candidates["total_score"] = (
        W["budget"]  * candidates["s_budget"]  +
        W["height"]  * candidates["s_height"]  +
        W["purpose"] * candidates["s_purpose"] +
        W["exp"]     * candidates["s_exp"]     +
        W["cat"]     * candidates["s_category"]
    ).round(4)

    top3 = (
        candidates
        .sort_values("total_score", ascending=False)
        .head(3)
        .reset_index(drop=True)
    )
    return top3, est_inseam


def build_explanation(row, rank, budget, est_inseam, purpose, experience):
    price     = row["price"]
    seat_h    = row["seat_height_cm"]
    weight_kg = row["weight_kg"]
    engine_cc = row["engine_cc"]
    bike_type = str(row["type"]).lower()
    exp_rank  = EXP_RANK.get(experience.lower(), 1)

    pct = price / budget * 100
    if pct >= 90:
        price_frag = f"uses {pct:.0f}% of the ${budget:,} budget (excellent value)"
    elif pct >= 65:
        price_frag = f"priced at ${price:,.0f} ({pct:.0f}% of budget)"
    else:
        price_frag = f"well under budget at ${price:,.0f} — leaves room for gear"

    diff      = seat_h - est_inseam
    abs_diff  = abs(diff)
    direction = "above" if diff > 0 else "below"
    if abs_diff <= 2:
        height_frag = f"near-perfect seat height ({seat_h:.0f} cm ≈ inseam)"
    elif abs_diff <= 8:
        height_frag = f"comfortable seat height ({seat_h:.0f} cm, {abs_diff:.0f} cm {direction} ideal)"
    else:
        height_frag = f"seat height {seat_h:.0f} cm ({abs_diff:.0f} cm {direction} ideal)"

    if bike_type == purpose.lower():
        purpose_frag = f"exact {bike_type} match"
    else:
        purpose_frag = f"{bike_type} — compatible with {purpose.lower()}"

    if exp_rank == 0:
        if weight_kg <= 30:
            exp_frag = f"very light {weight_kg:.0f} kg — ideal for beginners"
        elif weight_kg <= 130:
            exp_frag = f"manageable {weight_kg:.0f} kg / {engine_cc:.0f} cc for beginners"
        else:
            exp_frag = f"{weight_kg:.0f} kg / {engine_cc:.0f} cc — approachable with care"
    elif exp_rank == 1:
        exp_frag = f"{weight_kg:.0f} kg / {engine_cc:.0f} cc suits intermediates well"
    else:
        exp_frag = f"{engine_cc:.0f} cc / {weight_kg:.0f} kg rewards experienced riders"

    return f"{price_frag}. {height_frag}. {purpose_frag}. {exp_frag}."


# ─────────────────────────────────────────────────────────────────────────────
# CARD HTML BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def render_card(rank, name, price, category, bike_type, experience_level,
                seat_h, weight_kg, engine_cc, score, explanation):
    rank_class = f"rank-{rank}" if rank <= 3 else ""
    bar_width  = int(round(score * 100))
    medal_map  = {1: "🥇", 2: "🥈", 3: "🥉"}
    medal      = medal_map.get(rank, f"#{rank}")

    cat_icon   = "🏍️" if str(category).lower() == "motorcycle" else "🚲"
    purpose_icons = {"commute": "🏙️", "sport": "⚡", "offroad": "🌲", "leisure": "☀️"}
    type_icon  = purpose_icons.get(str(bike_type).lower(), "🎯")

    html = f"""
<div class="bf-card {rank_class}">
  <span class="bf-price-tag">${price:,.0f}</span>
  <span class="bf-rank-badge {rank_class}">{rank}</span>
  <span class="bf-bike-name">{name}</span>

  <div class="bf-meta">
    <span class="bf-tag">{cat_icon} {str(category).title()}</span>
    <span class="bf-tag">{type_icon} {str(bike_type).title()}</span>
    <span class="bf-tag">⚙️ {engine_cc:.0f} cc</span>
    <span class="bf-tag">⚖️ {weight_kg:.0f} kg</span>
    <span class="bf-tag">📐 {seat_h:.0f} cm seat</span>
    <span class="bf-tag">🎓 {str(experience_level).title()}</span>
  </div>

  <div class="bf-score-row">
    <span class="bf-score-label">MATCH SCORE</span>
    <div class="bf-score-track">
      <div class="bf-score-fill {rank_class}" style="width:{bar_width}%"></div>
    </div>
    <span class="bf-score-value">{score:.1%}</span>
  </div>

  <div class="bf-explanation">
    {medal} {explanation}
  </div>
</div>
"""
    return html


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bf-hero">
  <h1>🏍️ BikeFit</h1>
  <p>Find Your Perfect Ride — personalized recommendations in seconds</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="bf-form-card">', unsafe_allow_html=True)

st.markdown('<div class="bf-section-label">💰 Budget</div>', unsafe_allow_html=True)
budget = st.slider(
    "Maximum budget (USD)",
    min_value=500, max_value=25000, value=8000, step=250,
    format="$%d",
    label_visibility="collapsed",
)

st.markdown('<div class="bf-section-label">📏 Rider Height</div>', unsafe_allow_html=True)
rider_height_cm = st.slider(
    "Rider height (cm)",
    min_value=140, max_value=210, value=175, step=1,
    format="%d cm",
    label_visibility="collapsed",
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown('<div class="bf-section-label">🎯 Riding Purpose</div>', unsafe_allow_html=True)
    purpose = st.selectbox(
        "Riding Purpose",
        options=["commute", "sport", "offroad", "leisure"],
        format_func=lambda x: {"commute": "🏙️ Commute", "sport": "⚡ Sport",
                                "offroad": "🌲 Off-Road", "leisure": "☀️ Leisure"}[x],
        label_visibility="collapsed",
    )

with col_b:
    st.markdown('<div class="bf-section-label">🎓 Experience Level</div>', unsafe_allow_html=True)
    experience = st.selectbox(
        "Experience Level",
        options=["beginner", "intermediate", "advanced"],
        format_func=lambda x: {"beginner": "🌱 Beginner", "intermediate": "🔧 Intermediate",
                                "advanced": "🏆 Advanced"}[x],
        label_visibility="collapsed",
    )

with col_c:
    st.markdown('<div class="bf-section-label">🚲 Bike Category</div>', unsafe_allow_html=True)
    category = st.selectbox(
        "Bike Category",
        options=["both", "motorcycle", "bicycle"],
        format_func=lambda x: {"both": "🔀 Both", "motorcycle": "🏍️ Motorcycle",
                                "bicycle": "🚲 Bicycle"}[x],
        label_visibility="collapsed",
    )

st.markdown('</div>', unsafe_allow_html=True)  # /bf-form-card

find_clicked = st.button("🔍 Find My Bike", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if find_clicked:
    result = score_bikes(clean_df, budget, rider_height_cm, purpose, experience, category)

    if isinstance(result, tuple):
        top3, est_inseam = result
    else:
        top3 = result
        est_inseam = rider_height_cm * 0.47

    if top3.empty:
        st.markdown("""
<div class="bf-no-results">
  <span>🔍</span>
  <strong>No bikes found</strong><br>
  Try increasing your budget or switching category to <em>Both</em>.
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="bf-results-header">
  <h2>Top Matches for You</h2>
  <p>Budget ${budget:,} · {rider_height_cm} cm · {purpose.title()} · {experience.title()} · {category.title()}</p>
</div>
""", unsafe_allow_html=True)

        for rank, (_, row) in enumerate(top3.iterrows(), start=1):
            explanation = build_explanation(
                row, rank, budget, est_inseam, purpose, experience
            )
            card_html = render_card(
                rank=rank,
                name=row["name"],
                price=row["price"],
                category=str(row["category"]),
                bike_type=str(row["type"]),
                experience_level=str(row["experience_level"]),
                seat_h=row["seat_height_cm"],
                weight_kg=row["weight_kg"],
                engine_cc=row["engine_cc"],
                score=row["total_score"],
                explanation=explanation,
            )
            st.markdown(card_html, unsafe_allow_html=True)