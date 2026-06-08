import streamlit as st
import pickle
import pandas as pd
import time
from streamlit_lottie import st_lottie
import requests

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Car Mileage Predictor",
    page_icon="🚗",
    layout="wide"
)

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.big-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#A0A0A0;
    font-size:18px;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#ff4b4b,#ff8c00);
    color:white;
    font-size:20px;
    font-weight:bold;
    border-radius:15px;
    height:60px;
}

.metric-card{
    padding:20px;
    border-radius:20px;
    background:#1f2937;
    color:white;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD MODEL
# -----------------------
with open("car_milege_pred.pkl", "rb") as file:
    model = pickle.load(file)

# -----------------------
# LOTTIE ANIMATION
# -----------------------
def load_lottie(url):
    r = requests.get(url)
    return r.json()

car_animation = load_lottie(
    "https://assets1.lottiefiles.com/packages/lf20_fcfjwiyb.json"
)

# -----------------------
# HEADER
# -----------------------
st.markdown(
    "<div class='big-title'>🚗 Car Mileage Predictor</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Predict vehicle fuel efficiency using Machine Learning</div>",
    unsafe_allow_html=True
)

st_lottie(
    car_animation,
    height=250,
    key="car"
)

# -----------------------
# USER DETAILS
# -----------------------
st.markdown("## 📋 Car Information")

col1,col2,col3 = st.columns(3)

with col1:
    car_name = st.text_input(
        "Car Name",
        placeholder="BMW"
    )

with col2:
    model_name = st.text_input(
        "Model",
        placeholder="X5"
    )

with col3:
    year = st.number_input(
        "Manufacturing Year",
        min_value=1980,
        max_value=2035,
        value=2024
    )

st.divider()

# -----------------------
# VEHICLE SPECS
# -----------------------
st.markdown("## ⚙ Vehicle Specifications")

c1,c2 = st.columns(2)

with c1:
    cyl = st.slider(
        "Number of Cylinders",
        2,12,4
    )

    disp = st.slider(
        "Displacement",
        50,500,150
    )

with c2:
    hp = st.slider(
        "Horsepower",
        40,600,100
    )

    wt = st.slider(
        "Weight (1000 lbs)",
        1.0,6.0,2.5
    )

# -----------------------
# PREDICT
# -----------------------
if st.button("🚀 Predict Mileage"):

    with st.spinner("Analyzing vehicle specifications..."):
        time.sleep(2)

    input_data = pd.DataFrame({
        "cyl":[cyl],
        "disp":[disp],
        "hp":[hp],
        "wt":[wt]
    })

    prediction = model.predict(input_data)[0]

    st.success("Prediction Completed Successfully!")

    st.balloons()

    st.markdown("## 📊 Prediction Result")

    st.metric(
        label="Estimated Mileage (MPG)",
        value=f"{prediction:.2f}"
    )

    # Fuel Efficiency Rating
    if prediction >= 28:
        rating = "🟢 Excellent"
        progress = 100

    elif prediction >= 22:
        rating = "🔵 Good"
        progress = 75

    elif prediction >= 16:
        rating = "🟡 Average"
        progress = 50

    else:
        rating = "🔴 Poor"
        progress = 25

    st.markdown(f"### Fuel Efficiency : {rating}")

    my_bar = st.progress(0)

    for percent in range(progress):
        time.sleep(0.01)
        my_bar.progress(percent + 1)

    st.markdown(
        f"""
        <div class='metric-card'>
            <h2>{car_name} {model_name}</h2>
            <h3>Year : {year}</h3>
            <h1>{prediction:.2f} MPG</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("ℹ About Project")

st.sidebar.info(
    '''
    This Machine Learning application predicts
    Car Mileage (MPG) using:

    • Cylinders

    • Displacement

    • Horsepower

    • Weight

    Built using:

    ✔ Streamlit

    ✔ Scikit-Learn

    ✔ Pandas

    ✔ Pickle
    '''
)

st.sidebar.success("Model Loaded Successfully")