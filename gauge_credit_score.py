import streamlit as st
import pandas as pd
import scorecardpy as sc
import pickle
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_score_card_dict():
    """Function for load score card dictionary"""
    score_card = pickle.load(open('data_input/score_card_dict.pkl','rb'))
    df_credit = pickle.load(open('data_input/credit_taiwan.pkl','rb'))
    list_feature = [*score_card]
    list_feature.sort()
    list_feature.remove('basepoints')

    return score_card, list_feature, df_credit

score_card, list_feature, df_credit = load_score_card_dict()

st.title('Behaviour Credit Score Dashboard')
st.caption("Credit Scorecard built from Taiwan's behavioral credit dataset [modeled using logistic regression](https://github.com/hwulanayu/scorecard_python). The dataset contains information on default payments, demographic factors, credit data, history of payments, and bill statements of credit card clients in Taiwan from April 2005 to September 2005.")

st.sidebar.title('Check your Credit Score:')

# for value in list_feature:
#     value = st.sidebar.slider(value, 0, 130, 25)

# @st.cache_data()
# def get_data():
#     return []

# Inisialisasi DataFrame di session_state
if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=[
        "limit_bal", "education", "age", "pay_1", "pay_2", "pay_3",
        "pay_4", "pay_5", "pay_6", "bill_amt1", "bill_amt2", "bill_amt3",
        "bill_amt4", "bill_amt5", "bill_amt6", "pay_amt1", "pay_amt2",
        "pay_amt3", "pay_amt4", "pay_amt5", "pay_amt6"
    ])

# slider
age = st.sidebar.slider('age', 20, 80, step=1)
limit_bal = st.sidebar.slider('Limit Balance', 10000, 800000, step=1)
education = option = st.sidebar.selectbox("Education",
   options=df_credit['education'].unique(),
   index=None,
   placeholder="Select education...",
)

pay_1 = st.sidebar.slider('Payment Status on April', 0, 8, step=1)
pay_2 = st.sidebar.slider('Payment Status on May', 0, 8, step=1)
pay_3 = st.sidebar.slider('Payment Status on June', 0, 8, step=1)
pay_4 = st.sidebar.slider('Payment Status on July', 0, 8, step=1)
pay_5 = st.sidebar.slider('Payment Status on August', 0, 8, step=1)
pay_6 = st.sidebar.slider('Payment Status on September', 0, 8, step=1)

bill_amt1 = st.sidebar.slider('Billing Statement on April', 0, 100000, step=1)
bill_amt2 = st.sidebar.slider('Billing Statement on May', 0, 100000, step=1)
bill_amt3 = st.sidebar.slider('Billing Statement on June', 0, 100000, step=1)
bill_amt4 = st.sidebar.slider('Billing Statement on July', 0, 100000, step=1)
bill_amt5 = st.sidebar.slider('Billing Statement on August', 0, 100000, step=1)
bill_amt6 = st.sidebar.slider('Billing Statement on September', 0, 100000, step=1)

pay_amt1 = st.sidebar.slider('Payment Amount on April', 0, 8, step=1)
pay_amt2 = st.sidebar.slider('Payment Amount on May', 0, 8, step=1)
pay_amt3 = st.sidebar.slider('Payment Amount on June', 0, 8, step=1)
pay_amt4 = st.sidebar.slider('Payment Amount on July', 0, 8, step=1)
pay_amt5 = st.sidebar.slider('Payment Amount on August', 0, 8, step=1)
pay_amt6 = st.sidebar.slider('Payment Amount on September', 0, 8, step=1)

# Tombol untuk menyimpan input ke DataFrame
if st.sidebar.button('Submit Data'):
    new_row = pd.DataFrame({
        "limit_bal": [limit_bal],
        "education": [education],
        "age": [age],
        "pay_1": [pay_1], 
        "pay_2": [pay_2], 
        "pay_3": [pay_3],
        "pay_4": [pay_4],
        "pay_5": [pay_5],
        "pay_6": [pay_6],
        "bill_amt1": [bill_amt1],
        "bill_amt2": [bill_amt2],
        "bill_amt3": [bill_amt3],
        "bill_amt4": [bill_amt4],
        "bill_amt5": [bill_amt5],
        "bill_amt6": [bill_amt6],
        "pay_amt1": [pay_amt1], 
        "pay_amt2": [pay_amt2], 
        "pay_amt3": [pay_amt3],
        "pay_amt4": [pay_amt4],
        "pay_amt5": [pay_amt5],
        "pay_amt6": [pay_amt6]
    })
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    st.success('Submitted!')

# # Tampilkan DataFrame
# st.write('DataFrame:')
# st.dataframe(st.session_state.df)

def predict_score(df_input, score_card, cutoff):
    # Transform raw input values into score points
    recommendation = ''
    df_points = sc.scorecard_ply(dt=df_input, 
                                 card=score_card, 
                                 print_step=0, 
                                 only_total_score=False)
    
    score = df_points['score'].values[0]
    recommendation = 'APPROVE' if score > cutoff else 'REJECT'
    
    return score, recommendation

def plotly_gauge_with_threshold(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Your Credit Score"},
        gauge = {
            'axis': {'range': [300, 700]},
            'bar': {'color': "gray"},
            'steps': [
                {'range': [300, 530], 'color': 'red'},
                {'range': [531, 700], 'color': 'green'}],
            'threshold': {
                'line': {'color': "black", 'width': 6},
                'thickness': 0.75,
                'value': 530}
        }
    ))
    return fig

# Pengecekan apakah DataFrame tidak kosong
if not st.session_state.df.empty:
    score, recs = predict_score(st.session_state.df.tail(1), score_card, 530)
    gauge_score = plotly_gauge_with_threshold(score)
    st.plotly_chart(gauge_score)

    # st.write('Score:', score)
    st.markdown("<h2 style='text-align: center;'>Recommendation:</h2>", 
                unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{recs}</h2>", 
                unsafe_allow_html=True)
else:
    st.write('DataFrame is empty. Please add data using the sliders.')