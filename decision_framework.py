import streamlit as st
import pandas as pd

st.title("Decision Assessment Table with Dropdown Scores")
st.write("Enter opportunities and rate each sub-criteria (1–5). Final scores are calculated automatically.")

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
# Prepare table columns
# -----------------------------
score_options = [1, 2, 3, 4, 5]
columns = ["Opportunity"]
for category in framework:
    for sub in framework[category]["subcriteria"]:
        columns.append(sub)

# Add columns for weighted scores (calculated later)
for category in framework:
    columns.append(f"{category} Score")
columns.append("Total Score")

# -----------------------------
# Initialize editable table
# -----------------------------
num_rows = st.number_input("Number of opportunities", min_value=1, max_value=20, value=3)

if "table_df" not in st.session_state:
    # Initialize empty table with NaNs for subcriteria
    data = {col: ["" if "Score" not in col else 0 for _ in range(num_rows)] for col in columns}
    st.session_state.table_df = pd.DataFrame(data)

# -----------------------------
# Display table for editing
# -----------------------------
edited_df = st.data_editor(
    st.session_state.table_df,
    column_config={
        col: st.column_config.Selectbox(
            label=col, options=score_options
        ) if col not in ["Opportunity"] and "Score" not in col else None
        for col in columns
    },
    num_rows="dynamic"
)

# -----------------------------
# Calculate scores
# -----------------------------
for idx, row in edited_df.iterrows():
    total_score = 0
    for category, data in framework.items():
        cat_score = 0
        for sub, weight in data["subcriteria"].items():
            val = row[sub]
            val_num = int(val) if val != "" else 0
            cat_score += val_num * weight
        cat_score_weighted = cat_score * data["weight"]
        edited_df.at[idx, f"{category} Score"] = round(cat_score_weighted, 2)
        total_score += cat_score_weighted
    edited_df.at[idx, "Total Score"] = round(total_score, 2)

# -----------------------------
# Display final table
# -----------------------------
st.write("### Decision Table with Calculated Scores")
st.dataframe(edited_df.sort_values("Total Score", ascending=False))

# Highlight the best opportunity
best_option = edited_df.loc[edited_df["Total Score"].idxmax(), "Opportunity"]
st.success(f"**Best Opportunity:** {best_option}")

# -----------------------------
# Export table as CSV
# -----------------------------
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Table as CSV",
    data=csv,
    file_name="decision_table.csv",
    mime='text/csv'
)

