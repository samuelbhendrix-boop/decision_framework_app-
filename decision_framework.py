import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Multi-Option Decision Assessment Framework")
st.write("Compare multiple options using weighted categories and sub-criteria.")

# -----------------------------
# Define framework
# -----------------------------
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

rating_map = {
    "Very Low": 1,
    "Low": 2,
    "Medium": 3,
    "Medium-high": 4,
    "High": 5,
    "Very High": 6
}

# -----------------------------
# 1. Input Options
# -----------------------------
options_input = st.text_area("Enter options (one per line)", "Option A\nOption B\nOption C")
options = [o.strip() for o in options_input.splitlines() if o.strip()]

if options:
    # -----------------------------
    # 2. Collect scores for each option
    # -----------------------------
    option_scores = {}

    for opt in options:
        st.write(f"### Scores for {opt}")
        option_scores[opt] = {}
        for category, data in framework.items():
            st.write(f"#### {category}")
            option_scores[opt][category] = {}
            for sub, weight in data["subcriteria"].items():
                option_scores[opt][category][sub] = st.selectbox(
                    f"{sub} ({category})",
                    list(rating_map.keys()),
                    index=2,
                    key=f"{opt}_{category}_{sub}"
                )

    # -----------------------------
    # 3. Calculate weighted scores
    # -----------------------------
    total_scores = {}
    breakdown = {}
    for opt in options:
        breakdown[opt] = {}
        total = 0
        for category, data in framework.items():
            cat_score = sum(rating_map[option_scores[opt][category][sub]] * weight 
                            for sub, weight in data["subcriteria"].items())
            cat_score_weighted = cat_score * data["weight"]
            breakdown[opt][category] = cat_score_weighted
            total += cat_score_weighted
        total_scores[opt] = total

    # -----------------------------
    # 4. Display results
    # -----------------------------
    st.write("### Weighted Scores by Category")
    df_breakdown = pd.DataFrame.from_dict(breakdown, orient="index")
    st.dataframe(df_breakdown)

    st.write("### Total Scores")
    df_total = pd.DataFrame.from_dict(total_scores, orient="index", columns=["Total Score"])
    df_total = df_total.sort_values("Total Score", ascending=False)
    st.dataframe(df_total)

    best_option = df_total.index[0]
    st.success(f"**Best Option:** {best_option}")

    # -----------------------------
    # 5. Visualization
    # -----------------------------
    st.write("### Comparison Chart")
    fig, ax = plt.subplots()
    df_total.plot(kind='bar', y="Total Score", legend=False, ax=ax, color='skyblue')
    ax.set_ylabel("Total Score")
    ax.set_xlabel("Options")
    ax.set_title("Decision Scores Comparison")
    st.pyplot(fig)

    # -----------------------------
    # 6. Export results
    # -----------------------------
    export_df = df_breakdown.copy()
    export_df['Total Score'] = df_total['Total Score']
    csv = export_df.to_csv().encode('utf-8')

    st.download_button(
        label="Download Full Framework CSV",
        data=csv,
        file_name="decision_framework_results.csv",
        mime='text/csv'
    )
