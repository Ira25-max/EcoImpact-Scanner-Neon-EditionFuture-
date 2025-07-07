import streamlit as st
import time
import base64
import pandas as pd
import plotly.express as px
#from fpdf import FPDF
#import tempfile

# --- Emission Factors in kg CO2 per kg ---
EMISSION_FACTORS = {
    "PET": 2.15,
    "HDPE": 1.8,
    "LDPE": 2.0,
    "PVC": 1.9,
    "PP": 1.7,
    "PS": 2.4
}


# --- Function to Get Emission Factor ---
def get_emission_factor(plastic_type):
    return EMISSION_FACTORS.get(plastic_type.upper(), 2.0)

# --- Main Analyzer Function ---
def analyze_impact(product_name, plastic_type, weight_grams, recyclable):
    weight_kg = weight_grams / 1000
    emission_factor = get_emission_factor(plastic_type)
    total_emission = weight_kg * emission_factor

    recyclability_score = 1 if recyclable.lower() == 'yes' else 0
    suggestions = []

    if not recyclability_score:
        suggestions.append("Switch to recyclable plastic type.")
    if plastic_type.upper() == "PVC":
        suggestions.append("Avoid PVC due to high toxicity.")

    return {
        "Product": product_name,
        "Plastic Type": plastic_type,
        "Weight (g)": weight_grams,
        "Recyclable": recyclable,
        "Carbon Footprint (kg CO2)": round(total_emission, 2),
        "Suggestions": suggestions
    }

# --- Suggest Lower Emission Alternatives ---
def suggest_alternatives(current_type, weight_grams):
    weight_kg = weight_grams / 1000
    alternatives = {
        p: round(weight_kg * get_emission_factor(p), 2)
        for p in EMISSION_FACTORS if p != current_type
    }
    return sorted(alternatives.items(), key=lambda x: x[1])[:3]

# --- Suggest Packaging Tip ---
def suggest_packaging_tips(plastic_type):
    if plastic_type == "PVC":
        return "✅ Replace PVC with PET or HDPE for lower toxicity and better recycling."
    elif plastic_type == "PS":
        return "💡 Consider using molded pulp or bioplastics instead of polystyrene."
    return "TIP: Try reducing wall thickness or using refillable formats."

# --- Streamlit UI ---
st.set_page_config(page_title="🧬 EcoImpact Scanner 2.0", layout="wide")

# Stylish CyberEco Neon Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
        background: radial-gradient(circle at center, #101820, #0b1419);
        color: #00ffb3;
    }
    .main-title {
        font-size: 3.5em;
        text-align: center;
        color: #00ffb3;
        margin-bottom: 30px;
        text-shadow: 0px 0px 10px #00ffb3;
    }
    .stButton>button {
        background: #00ffb3;
        color: #101820;
        border: none;
        padding: 12px 30px;
        font-size: 1.2em;
        border-radius: 8px;
        box-shadow: 0 0 15px #00ffb3;
    }
    .stButton>button:hover {
        background: #00e6a2;
        box-shadow: 0 0 20px #00ffb3;
    }
    .footer {
        text-align: center;
        font-size: 0.85em;
        color: #88ffe3;
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧬 EcoImpact Scanner: Neon Future Edition</div>', unsafe_allow_html=True)
st.write("Visualize and optimize your plastic packaging in a sleek neon dashboard.")

# --- Interactive Form ---
with st.expander("🧪 Input Product Details", expanded=True):
    with st.form("impact_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("🔤 Product Name", placeholder="e.g., Sports Drink Bottle")
            weight = st.number_input("⚖️ Plastic Weight (grams)", min_value=0.0, step=0.1, value=20.0)
        with col2:
            plastic_type = st.selectbox("🧪 Plastic Type", list(EMISSION_FACTORS.keys()))
            recyclable = st.radio("♻️ Is it recyclable?", ["Yes", "No"])

        submitted = st.form_submit_button("🚀 Launch Analysis")



# def generate_pdf(result, alt_data, packaging_tip):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", "B", 16)
#     pdf.set_text_color(0, 102, 102)
#
#     pdf.cell(200, 10, "EcoImpact Analysis Report", ln=True, align='C')
#     pdf.ln(10)
#
#     pdf.set_font("Arial", "", 12)
#     pdf.set_text_color(0, 0, 0)
#     pdf.cell(0, 10, f"Product: {result['Product']}", ln=True)
#     pdf.cell(0, 10, f"Plastic Type: {result['Plastic Type']}", ln=True)
#     pdf.cell(0, 10, f"Weight: {result['Weight (g)']} grams", ln=True)
#     pdf.cell(0, 10, f"Recyclable: {result['Recyclable']}", ln=True)
#     pdf.cell(0, 10, f"Carbon Footprint: {result['Carbon Footprint (kg CO2)']} kg CO2", ln=True)
#     pdf.ln(5)
#
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 10, "Packaging Tip:", ln=True)
#     pdf.set_font("Arial", "", 12)
#     pdf.multi_cell(0, 10, packaging_tip)
#     pdf.ln(5)
#
#     if result['Suggestions']:
#         pdf.set_font("Arial", "B", 12)
#         pdf.cell(0, 10, "Sustainability Suggestions:", ln=True)
#         pdf.set_font("Arial", "", 12)
#         for s in result['Suggestions']:
#             pdf.multi_cell(0, 10, f"- {s}")
#         pdf.ln(5)
#
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 10, "Alternative Materials (Lower Emissions):", ln=True)
#     pdf.set_font("Arial", "", 12)
#     for alt_type, alt_emission in alt_data:
#         savings = round(result['Carbon Footprint (kg CO2)'] - alt_emission, 2)
#         if savings > 0:
#             pdf.cell(0, 10, f"{alt_type}: {alt_emission} kg CO₂ → Save {savings} kg CO₂", ln=True)
#
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     pdf.output(temp_file.name)
#     return temp_file.name


# --- Display Results ---
if submitted:
    with st.spinner("Engaging carbon calculator engines..."):
        time.sleep(1.8)
        result = analyze_impact(product_name, plastic_type, weight, recyclable)
        # --- Suggested Alternatives ---
        st.markdown("### 🔄 Suggested Alternatives (Lower Emissions)")
        alt_data = suggest_alternatives(plastic_type, weight)
        for p, e in alt_data:
            st.info(f"✅ **{p}** → Emission: `{e} kg CO₂`")

    st.markdown("---")
    st.markdown("## 🔍 Environmental Impact Snapshot")

    colA, colB = st.columns([1, 2])
    with colA:
        st.metric(label="🌍 Carbon Footprint (kg CO₂)", value=result['Carbon Footprint (kg CO2)'])
        st.metric(label="♻️ Recyclable", value=result['Recyclable'])
    # --- Biodegradability Indicator ---
    BIODEGRADABLE = {
        "PET": "❌ Not Biodegradable",
        "HDPE": "❌ Not Biodegradable",
        "LDPE": "❌ Not Biodegradable",
        "PVC": "❌ Not Biodegradable",
        "PP": "❌ Not Biodegradable",
        "PS": "❌ Not Biodegradable"
    }
    biodegradability = BIODEGRADABLE.get(plastic_type, "Unknown")
    st.markdown("### 🌱 Biodegradability")
    st.warning(f"{plastic_type} → {biodegradability}")

    with colB:
        st.markdown(f"**Product**: `{result['Product']}`")
        st.markdown(f"**Plastic Type**: `{result['Plastic Type']}`")
        st.markdown(f"**Weight**: `{result['Weight (g)']} g`")

    st.markdown("### 📦 Packaging Tip")
    st.info(suggest_packaging_tips(plastic_type))

    if result['Suggestions']:
        st.markdown("### ⚠️ Suggestions for Sustainability")
        for s in result['Suggestions']:
            st.error(s)
    else:
        st.success("🌈 Ultra Clean: Your packaging is optimized!")
        st.snow()

    # --- Suggested Alternatives ---
    st.markdown("### 🔄 Suggested Alternatives (Lower Emissions)")
    alt_data = suggest_alternatives(plastic_type, weight)
    for p, e in alt_data:
        st.info(f"✅ **{p}** → Emission: `{e} kg CO₂`")

        # --- Carbon Savings if Switched to Alternatives ---
        st.markdown("### 💚 Potential Carbon Savings")
        st.markdown("See how much CO₂ you could save by switching to a more sustainable plastic alternative:")

        for alt_type, alt_emission in alt_data:
            savings = round(result['Carbon Footprint (kg CO2)'] - alt_emission, 2)
            if savings > 0:
                st.success(f"🔁 Switching to **{alt_type}** can save **{savings} kg CO₂** for this product.")
            else:
                st.info(f"ℹ️ {alt_type} has equal or higher emissions than the current material.")

    # --- Emission Comparison Chart ---
    st.markdown("### 📊 Emission Comparison Chart")
    chart_data = alt_data + [(plastic_type, result['Carbon Footprint (kg CO2)'])]
    df = pd.DataFrame(chart_data, columns=["Plastic Type", "Emission"])
    fig = px.bar(df, x="Emission", y="Plastic Type", orientation="h", color="Plastic Type",
                 title="Carbon Emission Comparison by Plastic Type")
    st.plotly_chart(fig, use_container_width=True)

    # --- Material Comparison Mode ---
    st.markdown("### 🧪 Material Comparison Mode")
    st.markdown("Compare materials based on multiple sustainability metrics:")

    comparison_data = [
        {"Plastic": "PET", "Emission (kg CO₂/kg)": 2.15, "Recyclable": "Yes", "Biodegradable": "No", "Decomposition Time": "450 years"},
        {"Plastic": "HDPE", "Emission (kg CO₂/kg)": 1.8, "Recyclable": "Yes", "Biodegradable": "No", "Decomposition Time": "100 years"},
        {"Plastic": "LDPE", "Emission (kg CO₂/kg)": 2.0, "Recyclable": "Yes", "Biodegradable": "No", "Decomposition Time": "500+ years"},
        {"Plastic": "PVC", "Emission (kg CO₂/kg)": 1.9, "Recyclable": "No", "Biodegradable": "No", "Decomposition Time": "1000 years"},
        {"Plastic": "PP", "Emission (kg CO₂/kg)": 1.7, "Recyclable": "Yes", "Biodegradable": "No", "Decomposition Time": "20–30 years"},
        {"Plastic": "PS", "Emission (kg CO₂/kg)": 2.4, "Recyclable": "Rarely", "Biodegradable": "No", "Decomposition Time": "500 years"},
    ]

    comp_df = pd.DataFrame(comparison_data)

    selected = st.multiselect(
        "🔍 Select plastics to compare:",
        options=comp_df["Plastic"],
        default=["PET", "HDPE", "PP"]
    )

    filtered_df = comp_df[comp_df["Plastic"].isin(selected)]
    st.dataframe(filtered_df, use_container_width=True)

    # --- PDF Export ---
    # pdf_path = generate_pdf(result, alt_data, suggest_packaging_tips(plastic_type))
    #
    # with open(pdf_path, "rb") as f:
    #     st.download_button(
    #         label="📄 Download Report as PDF",
    #         data=f,
    #         file_name=f"{result['Product'].replace(' ', '_')}_EcoImpact_Report.pdf",
    #         mime="application/pdf"
    #     )

# --- Plastic Lifecycle Visualizer ---
st.markdown("### ♻️ Plastic Lifecycle Visualizer")
st.markdown("Understand the journey of plastic — from raw material to end-of-life.")
st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Plastic_lifecycle.png", caption="Typical lifecycle of plastic materials", use_container_width=True)

# --- Global Context Insights ---
st.markdown("### 🌍 Global Context Insights")
st.markdown("""
Plastic pollution is a global crisis. Here's how your product fits into the bigger picture:
""")

col1, col2 = st.columns(2)
with col1:
    st.info("🌐 **Global Plastic Production**\nOver 400 million tons of plastic are produced each year.")

    st.warning("♻️ **Recycling Rate**\nOnly 9% of plastic ever produced has been recycled.")

    st.success("🌊 **Ocean Pollution**\nAn estimated 11 million tons of plastic enter oceans annually.")

with col2:
    st.metric("🌍 Average Carbon Footprint of 1 Plastic Bottle", "0.5 kg CO₂")
    st.metric("📈 Projected Plastic Waste by 2050", "12 billion tons")
    st.metric("🏭 Contribution to Global Emissions", "3.4% of total CO₂ emissions")

if submitted:
    st.markdown("""
    > 🌟 **Did you know?** Your product emits **{:.2f} kg CO₂**, which is {:.1f}% of the average emission from a single-use plastic bottle.
    """.format(
        result['Carbon Footprint (kg CO2)'], (result['Carbon Footprint (kg CO2)'] / 0.5) * 100
    ))





st.markdown("""
- 🔍 **Extraction:** Plastic starts with crude oil/natural gas.
- 🏭 **Production:** Processed into polymer resins.
- 🛍️ **Usage:** Formed into packaging/products.
- 🚮 **Disposal:** Landfill, incineration, or recycling.
- 🌊 **Leakage:** Some escapes into environment/ocean.
""")

# --- Footer ---
st.markdown('<div class="footer">🔬 Developed by EcoTech Labs • Powered by Streamlit • Neon UX Design</div>', unsafe_allow_html=True)
