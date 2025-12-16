import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Decision Framework Builder")
st.write("Create a custom framework to evaluate your key decisions and identify the best option.")

# -----------------------------
# 1. Decision Title
# -----------------------------
decision_title = st.text_input("Decision Title", "Example: Choosing a Job Offer")

# -----------------------------
# 2. Options
# -----------------------------
options_input = st.text_area("Enter options (one per line)", "Option A\nOption B\nOption C")
options = [o.strip() for o in options_input.splitlines() if o.strip()]

# -----------------------------
# 3. Criteria
# -----------------------------
criteria_input = st.text_area("Enter criteria (one per line)", "Salary\nGrowth\nCulture")
criteria = [c.strip() for c in criteria_input.splitlines() if c.strip()]

if options and criteria:
    st.write("### Assign weight to each criterion (1–10)")
    weights = []
    for c in criteria:
        w = st.slider(f"Weight for {c}", 1, 10, 5)
        weights.append(w)

    st.write("### Score each option against each criterion (1–10)")
    scores = []
    for o in options:
        st.write(f"#### Option: {o}")
        row = []
        for c in criteria:
            s = st.slider(f"Score for {c}", 1, 10, 5, key=f"{o}_{c}")
            row.append(s)
        scores.append(row)

    # -----------------------------
    # 4. Calculate Weighted Scores
    # -----------------------------
    df = pd.DataFrame(scores, columns=criteria, index=options)
    weighted_df = df.multiply(weights, axis=1)
    total_scores = weighted_df.sum(axis=1)

    st.write("### Weighted Scores")
    st.dataframe(total_scores.sort_values(ascending=False))

    best_option = total_scores.idxmax()
    st.success(f"Best option: {best_option}")

    # -----------------------------
    # 5. Visualization
    # -----------------------------
    st.write("### Comparison Chart")
    fig, ax = plt.subplots()
    total_scores.sort_values(ascending=True).plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel("Weighted Score")
    ax.set_ylabel("Options")
    ax.set_title("Decision Scores")
    st.pyplot(fig)

    # -----------------------------
    # 6. Export Option
    # -----------------------------
    st.write("### Export Results")
    export_df = weighted_df.copy()
    export_df['Total Score'] = total_scores
    csv = export_df.to_csv().encode('utf-8')

    st.download_button(
        label="Download Framework as CSV",
        data=csv,
        file_name=f"{decision_title.replace(' ','_')}_framework.csv",
        mime='text/csv'
    )

