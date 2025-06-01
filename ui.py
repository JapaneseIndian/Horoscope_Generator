import streamlit as st
import requests
from datetime import datetime

URL = "http://127.0.0.1:5000/"
zodiac = [
    "Aries", "Taurus", "Gemini", "Cancer", "Scorpio", "Leo", 
    "Pisces", "Libra", "Virgo", "Aquarius", "Sagittarius", "Capricorn"
]
CATEGORIES = ["love", "career", "health", "social life", "mind"]
st.set_page_config(page_title="Horoscope App", page_icon="🔮")
st.title("🔮 Mystic Horoscope Reader")

def main():
    tab1, tab2 = st.tabs(["Get Prediction", "Saved Predictions"])
    
    with tab1:
        st.header("Get Your Horoscope")
        
        col1, col2 = st.columns(2)
        with col1:
            sign = st.selectbox("Your Zodiac Sign", zodiac)
        with col2:
            category = st.selectbox("Category", CATEGORIES)
        
        if st.button("Get Prediction", type="primary"):
            try:
                response = requests.get(
                    f"{URL}/horoscope",
                    params={"sign": sign, "category": category}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✨ Here's your horoscope reading:")
                    st.subheader(f"{sign} - {category.capitalize()}")
                    st.write(data["prediction"])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Lucky Number", data["lucky_number"])
                    with col2:
                        st.metric("Date", data["date"])
                    
                    st.session_state.current_prediction = {
                        "sign": sign,
                        "prediction": data["prediction"],
                        "category": category
                    }
                
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
        if 'current_prediction' in st.session_state:
            if st.button("Save This Prediction"):
                try:
                    save_response = requests.post(
                        f"{URL}/horoscope/save",
                        json=st.session_state.current_prediction
                    )
                    
                    if save_response.status_code == 201:
                        st.success("Prediction saved permanently!")
                        del st.session_state.current_prediction
                    else:
                        st.error(f"Failed to save. Status code: {save_response.status_code}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
    
    with tab2:
        st.header("Your Saved Predictions")
        
        try:
            response = requests.get(f"{URL}/horoscope/saved")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["count"] == 0:
                    st.info("No saved predictions yet. Get a prediction and save it!")
                else:
                    st.subheader(f"Total Saved Predictions: {data['count']}")
                    
                    for pred in data["horoscopes"]:
                        with st.expander(f"#{pred['id']} {pred['sign']} - {pred['category'].capitalize()}"):
                            st.write(pred["prediction"])
                            st.caption(f"Saved on: {pred['saved_at']}")
            
                            if st.button(f"Delete #{pred['id']}", key=f"delete_{pred['id']}"):
                                del_response = requests.delete(f"{URL}/horoscope/delete/{pred['id']}")
                                if del_response.status_code == 200:
                                    st.rerun()  # Refresh the list
                                else:
                                    st.error("Failed to delete prediction")
            else:
                st.error(f"Error fetching saved predictions: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")

if __name__ == "__main__":
    main()
    