import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Table-Based Decision Assessment Tool")
st.write("Enter multiple opportunities as rows, and fill in scores for each sub-criteria (1–6).")

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

# -----------------------------
# Prepare columns for table
# -----------------------------
columns = ["Opportunity"]
for category in framework:
    for sub in framework[category]["subcriteria"]:
        columns.append(sub)

# -----------------------------
# Create editable table
# -----------------------------
st.write("### Enter Opportunities and Scores")
num_rows = st.number_input("Number of opportunities", min_value=1, max_value=20, value=3)
if "table_df" not in st.session_state:
    # Initialize empty table
    data = {col: [""]*num_rows for col in columns}
    st.session_state.table_df = pd.DataFrame(data)

edited_df = st.data_editor(st.session_state.table_df, num_rows="dynamic")

# -----------------------------
# Map textual ratings to numeric
# -----------------------------
rating_map = {
    "Very Low": 1,
    "Low": 2,
    "Medium": 3,
    "Medium-high": 4,
    "High": 5,
    "Very High": 6
}

# -----------------------------
# Calculate weighted scores if table filled
# -----------------------------
if st.button("Calculate Scores"):
    total_scores = {}
    breakdown = {}

    for idx, row in edited_df.iterrows():
        opportunity_name = row["Opportunity"]
        breakdown[opportunity_name] = {}
        total = 0
        for category, data in framework.items():
            cat_score = 0
            for sub, weight in data["subcriteria"].items():
                val = row[sub]
                # If user entered text rating, convert to number
                if isinstance(val, str):
                    val_num = rating_map.get(val, 0)
                else:
                    val_num = float(val) if val != "" else 0
                cat_score += val_num * weight
            cat_score_weighted = cat_score * data["weight"]
            breakdown[opportunity_name][category] = cat_score_weighted
            total += cat_score_weighted
        total_scores[opportunity_name] = total

    # Display breakdown
    st.write("### Weighted Scores by Category")
    df_breakdown = pd.DataFrame.from_dict(breakdown, orient="index")
    st.dataframe(df_breakdown)

    st.write("### Total Scores")
    df_total = pd.DataFrame.from_dict(total_scores, orient="index", columns=["Total Score"])
    df_total = df_total.sort_values("Total Score", ascending=False)
    st.dataframe(df_total)

    best_option = df_total.index[0]
    st.success(f"**Best Opportunity:** {best_option}")

    # -----------------------------
    # Visualization
    # -----------------------------
    st.write("### Comparison Chart")
    fig, ax = plt.subplots()
    df_total.plot(kind='bar', y="Total Score", legend=False, ax=ax, color='skyblue')
    ax.set_ylabel("Total Score")
    ax.set_xlabel("Opportunities")
    ax.set_title("Decision Scores Comparison")
    st.pyplot(fig)

    # -----------------------------
    # Export results
    # -----------------------------
    export_df = df_breakdown.copy()
    export_df["Total Score"] = df_total["Total Score"]
    csv = export_df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Full Table CSV",
        data=csv,
        file_name="decision_framework_table.csv",
        mime='text/csv'
    )

