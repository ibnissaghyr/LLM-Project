import streamlit as st
from main import get_few_shot_db_chain

# Main Title
st.markdown(
    "<h1 style='text-align: center; font-size: 50px;'>LuminoDB 🚀</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; color: grey;'>Your smart solution for simplified SQL queries</h3>",
    unsafe_allow_html=True
)

# Add CSS for larger and styled input label
st.markdown("""
    <style>
        label {
            font-size: 30px !important; /* Enlarge the label */
            font-weight: bold;
            color: #4CAF50; /* Green color */
        }
        .stButton button {
            font-size: 20px;
            color: white;
            background-color: #4CAF50;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Input Field with Enlarged Label
question = st.text_input("Ask your question 📊:")

# Add a button for processing the query
if st.button('Get the answer'):
    if question:
        with st.spinner("⏳ Processing your query, please wait..."):
            try:
                # Build the few-shot learning chain
                chain = get_few_shot_db_chain()

                # Run the user's question through the chain
                response = chain.run(question)

                # Display the response
                st.success("Here is the answer to your question!")
                st.header("Answer")
                st.write(response)
            except Exception as e:
                # Display an error message in case of failure
                st.error(f"Une erreur est survenue : {str(e)}")
    else:
        # Warn if no question is provided
        st.warning("Veuillez entrer une question.")
