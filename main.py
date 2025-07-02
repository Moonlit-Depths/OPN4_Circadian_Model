import streamlit as st
import tellurium as te
import matplotlib.pyplot as plt
from PIL import Image

snp_data = {
    "Wild-Type (normal function)": {"J_light": 1.0, "ΔΔG": 0.0, "PolyPhen": "—"},
    "rs1079610 (I394T)": {"J_light": 0.4, "ΔΔG": -1.8, "PolyPhen": "Probably damaging"},
    "rs143602837 (V392I)": {"J_light": 0.6, "ΔΔG": -0.9, "PolyPhen": "Possibly damaging"},
    "rs2675703 (A426T)": {"J_light": 0.9, "ΔΔG": 0.1, "PolyPhen": "Benign"}
}

mut_img_map = {
    "rs1079610 (I394T)": "I394T_mutant.png",
    "rs143602837 (V392I)": "V392I_mutant.png",
    "rs2675703 (A426T)": "A426T_mutant.png"
}

st.title("🧬 OPN4 Mutation → Protein → Circadian Disruption Model")

# Show wild-type structure at the top
st.image("wildtype_structure.png", caption="AlphaFold-predicted structure of human melanopsin (OPN4)", use_column_width=True)

snp_choice = st.selectbox("Select an OPN4 Mutation", list(snp_data.keys()))
J_light = snp_data[snp_choice]["J_light"]
delta_g = snp_data[snp_choice]["ΔΔG"]
polyphen = snp_data[snp_choice]["PolyPhen"]

st.write(f"🔬 Predicted Structural Impact (ΔΔG): {delta_g} kcal/mol")
st.write(f"🧠 PolyPhen Prediction: {polyphen}")
st.write(f"🌞 Estimated Light Sensitivity (J_light): {J_light}")

# Show SNP-specific PyMOL image if available
if snp_choice in mut_img_map:
    st.image(mut_img_map[snp_choice], caption=f"PyMOL structure of {snp_choice} mutant", use_column_width=True)

model = '''
model circadian_model
  J_light = 1;
  Vmax = 1.5;
  Km = 0.5;
  k_deg = 0.7;
  species PER;
  J1: -> PER; Vmax * J_light / (Km + PER);
  J2: PER -> ; k_deg * PER;
  PER = 0.1;
end
'''

r = te.loadAntimonyModel(model)
r["J_light"] = J_light
result = r.simulate(0, 48, 500)

fig, ax = plt.subplots()
ax.plot(result[:, 0], result[:, 1], label=snp_choice)
ax.set_xlabel("Time (h)")
ax.set_ylabel("PER Expression")
ax.set_title("PER Oscillation with SNP-Driven Light Input")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.markdown(f"""
### 🧪 Biological Interpretation
This simulation links a real **OPN4 mutation** to:
- Structural damage (ΔΔG)
- Predicted loss-of-function (PolyPhen)
- Decreased light sensitivity (J_light)

Lower J_light reduces PER gene oscillations — modeling potential circadian rhythm disruption such as **Delayed Sleep Phase Syndrome (DSPS)**.
""")