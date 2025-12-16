import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Decision Assessment Table", layout="wide")
st.title("Table-Based Decision Assessment Tool")
st.write("Enter multiple opportunities as rows and rate each sub-criteria (1–5). Final scores are calculated automatically.")

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

score_options = [1, 2, 3, 4, 5]

# -----------------------------
# Prepare columns for table
# -----------------------------
columns = ["Opportunity"]
for category in framework:
    for sub in framework[category]["subcriteria"]:
        columns.append(sub)

# Add columns for calculated scores
for category in framework:
    columns.append(f"{category} Score")
columns.append("Total Score")

# -----------------------------
# Initialize table
# -----------------------------
num_rows = st.number_input("Number of opportunities", min_value=1, max_value=20, value=3)

if "table_df" not in st.session_state:
    data = {col: ["" if "Score" not in col else 0 for _ in range(num_rows)] for col in columns}
    st.session_state.table_df = pd.DataFrame(data)

# -----------------------------
# Create column_config for dropdowns
# -----------------------------
column_config = {
    col: st.column_config.Column(
        label=col,
        type="categorical",
        options=score_options
    ) if col not in ["Opportunity"] and "Score" not in col else None
    for col in columns
}

# -----------------------------
# Display editable table
# -----------------------------
edited_df = st.data_editor(
    st.session_state.table_df,
    column_config=column_config,
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
st.dataframe(edited_df.sort_values("Total Score", ascending=False), use_container_width=True)

# Highlight the best opportunity
best_option = edited_df.loc[edited_df["Total Score"].idxmax(), "Opportunity"]
st.success(f"**Best Opportunity:** {best_option}")

# -----------------------------
# Visualization
# -----------------------------
st.write("### Total Scores Comparison")
fig, ax = plt.subplots(figsize=(8, 4))
edited_df_sorted = edited_df.sort_values("Total Score", ascending=True)
ax.barh(edited_df_sorted["Opportunity"], edited_df_sorted["Total Score"], color="skyblue")
ax.set_xlabel("Total Score")
ax.set_ylabel("Opportunity")
ax.set_title("Decision Scores Comparison")
st.pyplot(fig)

# -----------------------------
# Export table
# -----------------------------
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Table as CSV",
    data=csv,
    file_name="decision_framework_table.csv",
    mime='text/csv'
)

