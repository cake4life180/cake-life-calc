# Start building the Cake Life Calculator and Landing Page for Cake Life
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator
import streamlit as st
pip install matplotlib

# Initialize the uploaded illustration data (simplified for now)
# Each entry: (Start Age, Monthly Contribution, Age Milestone, Cash Value, Death Benefit)
master_data = []  # Will fill with parsed points from all uploads

# Create a placeholder DataFrame for the full user input simulation
df = pd.DataFrame(master_data, columns=["Start Age", "Monthly Contribution", "Milestone Age", "Cash Value", "Death Benefit"])

# Build the interpolators
def build_interpolators(df):
    points = df[["Start Age", "Monthly Contribution", "Milestone Age"]].values
    cash_values = df["Cash Value"].values
    death_benefits = df["Death Benefit"].values

    cash_value_interp = LinearNDInterpolator(points, cash_values)
    death_benefit_interp = LinearNDInterpolator(points, death_benefits)

    return cash_value_interp, death_benefit_interp

# Mock user input simulation
def predict_values(start_age, monthly_contribution):
    milestones = [18, 25, 45, 65, 85]
    user_points = np.array([[start_age, monthly_contribution, age] for age in milestones])

    cash_value_interp, death_benefit_interp = build_interpolators(df)
    predicted_cash = cash_value_interp(user_points)
    predicted_death = death_benefit_interp(user_points)

    results = pd.DataFrame({
        "Milestone Age": milestones,
        "Predicted Cash Value": predicted_cash,
        "Predicted Death Benefit": predicted_death
    })

    return results

# Create visualization of predicted growth over milestones
def plot_predictions(results):
    plt.figure(figsize=(10, 6))
    plt.plot(results["Milestone Age"], results["Predicted Cash Value"], label="Cash Value")
    plt.plot(results["Milestone Age"], results["Predicted Death Benefit"], label="Death Benefit")
    plt.xlabel("Milestone Age")
    plt.ylabel("Dollars")
    plt.title("Predicted Growth Over Life Milestones")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Summary text generator
def generate_summary(results):
    text = "\n\n".join([
        f"At age {row['Milestone Age']}, your projected cash value is ${row['Predicted Cash Value']:,.0f} and death benefit is ${row['Predicted Death Benefit']:,.0f}."
        for index, row in results.iterrows()
    ])
    return text

# Streamlit App - Cake Life Landing Page
st.set_page_config(page_title="Cake Life Calculator", layout="centered")

st.title("🍰 Cake Life Calculator")
st.subheader("Build a Future as Sweet as Cake")

st.markdown("""
Imagine giving your child the gift of a lifetime — a foundation of wealth, protection, and opportunity.

Use the Cake Life Calculator to see what a small monthly contribution today could turn into by the time they hit life’s biggest milestones.
""")

st.write("---")

start_age = st.slider("👶 Child's Current Age:", min_value=0, max_value=18, value=4)
monthly_contribution = st.selectbox("💵 Monthly Contribution:", [250, 300, 500, 1000])

if st.button("🎂 Calculate Their Future!"):
    if len(df) > 0:
        predictions = predict_values(start_age=start_age, monthly_contribution=monthly_contribution)
        st.write("### 🎯 Milestone Predictions:")
        st.dataframe(predictions)

        st.write("### 📈 Growth Chart:")
        plot_predictions(predictions)

        st.write("### 📝 Personalized Summary:")
        st.text(generate_summary(predictions))
    else:
        st.warning("🚧 Data not available yet. Please populate master_data!")

st.write("---")

st.markdown("""
**Ready to build a plan that's perfectly baked just for your family?**

➡️ [Schedule a Custom Cake Life Plan Session](#)

Because the sweetest moments deserve the strongest foundations.
""")

# (Once master_data is populated, this full app will be ready!)
# Next step: Parse the real uploaded data to fill master_data!
