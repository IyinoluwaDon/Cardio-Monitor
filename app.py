"""Cardio Monitor - Streamlit edition.

Streamlit rewrite by Iyinoluwa Don-Taiwo of the original Flask app by
Sarvesh Kumar Sharma. No database: the model is trained from heart.csv.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import model as cm

BASE = Path(__file__).parent
STATIC = BASE / "static"

st.set_page_config(
    page_title="Cardio Monitor",
    page_icon=str(STATIC / "heartlogo.png"),
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    .footer {text-align:center; padding:1rem; margin-top:2rem;
             background:teal; color:white; border-radius:8px; font-weight:600;}
    .footer a {color:#ffd27f;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Training model...")
def get_model():
    return cm.train_model()


@st.cache_data
def get_reference():
    return cm.reference_values()


def bar_chart(labels, reference, user, title):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(labels))
    w = 0.38
    ax.bar(x - w / 2, reference, w, color="g", edgecolor="grey",
           label="Typical low-risk value")
    ax.bar(x + w / 2, user, w, color="r", edgecolor="grey", label="Your value")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Respective values", fontweight="bold")
    ax.set_title(title, fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return fig


def footer():
    st.markdown(
        """
        <div class="footer">
        Streamlit edition by Iyinoluwa Don-Taiwo
        &nbsp;|&nbsp;
        <a href="https://github.com/IyinoluwaDon/Cardio-Monitor" target="_blank">GitHub</a><br>
        <span style="font-weight:400;font-size:0.85rem;">
        Based on the original Flask project by Sarvesh Kumar Sharma
        </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def predict_page():
    left, right = st.columns([1, 8])
    left.image(str(STATIC / "heartlogo.png"), width=80)
    right.title("Cardio Monitor")
    st.write(
        "Find out whether you are at risk of developing heart disease. "
        "Fill in the details below and press **Predict**."
    )

    with st.form("patient_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Your name", placeholder="e.g. Ada")
        age = c2.number_input("Age", min_value=1, max_value=120, value=34, step=1)
        trestbps = c1.number_input(
            "Resting blood pressure in mm Hg (trestbps)",
            min_value=50, max_value=250, value=130, step=1)
        chol = c2.number_input(
            "Serum cholesterol in mg/dl (chol)",
            min_value=80, max_value=600, value=250, step=1)
        thalach = c1.number_input(
            "Maximum heart rate achieved (thalach)",
            min_value=60, max_value=250, value=150, step=1)
        oldpeak = c2.number_input(
            "ST depression induced by exercise (oldpeak)",
            min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        ca = c1.number_input(
            "Major vessels (0-3) colored by fluoroscopy (ca)",
            min_value=0, max_value=3, value=0, step=1)
        sex = c2.selectbox("Sex", list(cm.SEX))
        cp = c1.selectbox("Chest pain type (cp)", list(cm.CHEST_PAIN))
        exang = c2.selectbox("Exercise induced angina (exang)", list(cm.YES_NO), index=1)
        fbs = c1.selectbox("Fasting blood sugar > 120 mg/dl (fbs)", list(cm.YES_NO), index=1)
        slope = c2.selectbox("Slope of the peak exercise ST segment (slope)", list(cm.SLOPE), index=1)
        thal = c1.selectbox("Thalassemia result (thal)", list(cm.THAL))
        restecg = c2.selectbox("Resting ECG results (restecg)", list(cm.REST_ECG))
        submitted = st.form_submit_button("Predict", type="primary", width="stretch")

    st.caption("Your inputs are used only for this prediction and are not stored.")

    if submitted:
        record = {
            "age": age,
            "sex": cm.SEX[sex],
            "cp": cm.CHEST_PAIN[cp],
            "trestbps": trestbps,
            "chol": chol,
            "fbs": cm.YES_NO[fbs],
            "restecg": cm.REST_ECG[restecg],
            "thalach": thalach,
            "exang": cm.YES_NO[exang],
            "oldpeak": oldpeak,
            "slope": cm.SLOPE[slope],
            "ca": ca,
            "thal": cm.THAL[thal],
        }
        model, _ = get_model()
        label, low_risk_prob = cm.predict(model, record)
        who = name.strip() or "there"

        st.divider()
        st.header("Prediction")
        st.subheader(f"Hello {who}")
        if label == 1:
            st.success(
                "Good news. You have **very low chances of getting heart disease**. "
                "Open **About heart disease** in the sidebar to learn more."
            )
        else:
            st.error(
                "You have a **high risk of getting heart disease**. "
                "Please contact your doctor. Open **About heart disease** "
                "in the sidebar to learn more."
            )
        st.metric("Model estimate of low risk", f"{low_risk_prob * 100:.0f}%")

        ref = get_reference()
        st.subheader("Your data statistics")
        g1, g2 = st.columns(2)
        keys1 = ["cp", "fbs", "restecg", "exang", "oldpeak", "slope", "ca", "thal"]
        keys2 = ["trestbps", "chol", "thalach"]
        g1.pyplot(bar_chart(keys1, [ref[k] for k in keys1],
                            [float(record[k]) for k in keys1],
                            "Coded and clinical attributes"))
        g2.pyplot(bar_chart(keys2, [ref[k] for k in keys2],
                            [float(record[k]) for k in keys2],
                            "Blood pressure, cholesterol, heart rate"))
        st.warning(
            "This is only a prediction and not medical advice. "
            "See a doctor if symptoms persist."
        )


def about_page():
    st.title("About heart disease")
    tabs = st.tabs([f"Slide {i}" for i in range(2, 7)])
    for tab, i in zip(tabs, range(2, 7)):
        tab.image(str(STATIC / "corousal" / f"img{i}.png"), width="stretch")

    st.header("Overview")
    st.write(
        "Heart disease refers to any condition affecting the heart. There are "
        "many types, some of which are preventable. Unlike cardiovascular "
        "disease, which covers the entire circulatory system, heart disease "
        "affects only the heart. It is the leading cause of death in the "
        "United States according to the CDC, and it affects all genders and "
        "all racial and ethnic groups."
    )

    st.header("Types")
    types = {
        "Coronary artery disease": "The most common type. Arteries that supply the heart become clogged with plaque, which hardens and narrows them. The heart gets less oxygen and fewer nutrients, and over time the muscle weakens, raising the risk of heart failure and arrhythmias.",
        "Congenital heart defects": "Heart problems present from birth, such as abnormal valves, holes in the walls between heart chambers, or a missing valve. Many cause no symptoms and are found on routine checks.",
        "Arrhythmia": "An irregular heartbeat caused by faulty electrical impulses. The heart may beat too fast (tachycardia), too slow (bradycardia), or erratically. Persistent arrhythmias need treatment.",
        "Dilated cardiomyopathy": "The heart chambers stretch and the muscle thins, so the heart cannot pump well. Common causes are prior heart attacks, arrhythmias, and toxins. It usually affects people aged 20 to 60.",
        "Myocardial infarction (heart attack)": "Blood flow to the heart is interrupted, damaging or destroying part of the muscle. The usual cause is plaque, a blood clot, or both in a coronary artery.",
        "Heart failure": "The heart still works but not as well as it should. It can result from untreated coronary artery disease, high blood pressure, or arrhythmias. Early treatment helps prevent complications.",
        "Hypertrophic cardiomyopathy": "Usually inherited. The heart muscle thickens and contractions become harder. There may be no symptoms. People with a family history should ask about screening.",
        "Mitral valve regurgitation": "The mitral valve does not close tightly, so blood flows backward. Over time the heart can enlarge and heart failure can follow.",
        "Mitral valve prolapse": "The valve flaps bulge into the left atrium and may cause a murmur. It is usually not life threatening, though some people need treatment.",
        "Aortic stenosis": "The aortic valve opening is too narrow, restricting blood flow from the left ventricle to the aorta. It can be present from birth or develop through calcium deposits or scarring.",
    }
    for title, text in types.items():
        with st.expander(title):
            st.write(text)

    st.header("Symptoms")
    st.write("Symptoms depend on the type of heart disease.")
    st.markdown(
        """
        - **Blood vessels (atherosclerosis):** chest pain or pressure, shortness of breath, pain or numbness in the legs or arms, pain in the neck, jaw, upper abdomen or back. Women may also have nausea and extreme fatigue.
        - **Abnormal heartbeat:** fluttering in the chest, racing or slow heartbeat, lightheadedness, dizziness, fainting.
        - **Weak heart muscle (cardiomyopathy):** breathlessness, swollen legs, ankles and feet, fatigue, irregular heartbeats.
        - **Heart infection (endocarditis):** fever, shortness of breath, weakness, swelling, dry cough, skin rashes.
        - **Valve problems:** fatigue, shortness of breath, irregular heartbeat, swollen feet or ankles, chest pain, fainting.
        """
    )
    st.error(
        "Seek emergency medical care for chest pain, shortness of breath, or fainting."
    )

    st.header("Risk factors")
    st.markdown(
        """
        - **Age and sex:** risk grows with age. Men are generally at higher risk, and risk for women rises after menopause.
        - **Family history:** especially a parent with early heart disease.
        - **Smoking, poor diet, physical inactivity, stress.**
        - **High blood pressure, high cholesterol, diabetes, obesity.**
        - **Poor dental health:** germs can reach the heart and cause endocarditis.
        """
    )

    st.header("Prevention")
    st.markdown(
        """
        - Do not smoke.
        - Control blood pressure, cholesterol, and diabetes.
        - Exercise at least 30 minutes on most days.
        - Eat a diet low in salt and saturated fat.
        - Maintain a healthy weight.
        - Manage stress and practice good hygiene.
        """
    )


def main():
    st.sidebar.image(str(STATIC / "heartlogo.png"), width=90)
    st.sidebar.title("Cardio Monitor")
    page = st.sidebar.radio("Go to", ["Predict", "About heart disease"])
    _, accuracy = get_model()
    st.sidebar.caption(f"Model: KNN (k=7). Test accuracy: {accuracy * 100:.1f}%")

    if page == "Predict":
        predict_page()
    else:
        about_page()
    footer()


main()
