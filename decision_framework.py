import streamlit as st
import pandas as pd

st.title("Decision Assessment Framework")

# Define sub-criteria and weights for each category
framework = {
    "Market Attractiveness": {
        "weight": 0.5,
        "subcriteria": {
            "Market growth rate": 0.10,
            "Market profitability": 0.25,
            "Regulatory risks": 0.20,
            "Competitive intensity": 0.15,
            "Revenue/membership potential": 0.30
        }
    },
    "Strategic Fit": {
        "weight": 0.5,
        "subcriteria": {
            "Potential to provide competitive advantage": 0.20,
            "Fit with strategy, vision, and purpose": 0.25,
            "Channels to market": 0.15,
            "Fit with strengths": 0.15,
            "Ease of implementation": 0.25
        }
    }
}

# Mapping qualitative ratings to numeric
rating_map = {
    "Very Low": 1,
    "Low": 2,
    "Medium": 3,
    "Medium-high": 4,
    "High": 5,
    "Very High": 6
}

st.write("### Enter scores for each sub-criteria:")

scores = {}
for category, data in framework.items():
    st.write(f"#### {category}")
    scores[category] = {}
    for sub, w in data["subcriteria"].items():
        scores[category][sub] = st.selectbox(f"{sub} (weight {w*100}%)", list(rating_map.keys()), index=2)

# Calculate weighted scores
category_scores = {}
for category, data in framework.items():
    total = 0
    for sub, weight in data["subcriteria"].items():
        total += rating_map[scores[category][sub]] * weight
    category_scores[category] = total * data["weight"]

total_score = sum(category_scores.values())
st.write("### Results")
st.write(pd.DataFrame.from_dict(category_scores, orient="index", columns=["Weighted Category Score"]))
st.success(f"**Total Score:** {total_score:.2f}")
