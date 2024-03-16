import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load the JSON config file
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Create a title for the Streamlit app
st.title("MCQs Creator Application with LangChain")

# Create a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    # Add Button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)

                # Count tokens and the cost of API call
              
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

                quiz =response.get('quiz')
                
                # Check if the response is a dictionary and extract the quiz data
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    start_idx = quiz.find('{"1":')

                    # Extract the JSON part from the string
                    json_part = quiz[start_idx:]
                    # quiz = json.loads(json_part)
                    quiz = json_part
                    if quiz is not None:
                        table_data = get_table_data(quiz)

                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            # Display the review in a text box as well
                            st.text_area("Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("No quiz data found in the response")
                else:
                    st.write(response)

            except Exception as e:
                traceback.print_exc()
                st.error("An error occurred while generating MCQs.")

# Load environment variables if needed
# load_dotenv()