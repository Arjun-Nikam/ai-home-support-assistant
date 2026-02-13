import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="AI Home Support Assistant")

st.title("AI Home Maintenance Assistant ")

user_input = st.text_area("Describe your issue")

if st.button("Generate Reply"):

    if user_input.strip() == "":
        st.warning("Please enter a query.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"message": user_input}
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader(" Reply")
                st.write(result["response"])

               
            else:
                st.error("API Error: " + response.text)

        except Exception as e:
            st.error(f"Connection failed: {e}")