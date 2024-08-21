import streamlit as st
from GenAi import analyze
# Initialize session state
def initialize_session_state():
    if 'answers' not in st.session_state:
        st.session_state.answers = {
            'q1': "",
            'q2': "",
            'q3': "",
            'q4': "",
            'q5': "",
            'q6': ""
        }

def main():
    # Define questions
    questions = [
        "What are the skills or talents you possess that you are most proud of? Which of these skills do you feel come naturally to you?",
        "Reflecting on your past experiences, which moments or achievements stand out as the most fulfilling or impactful for you? Why do they stand out?",
        "What activities or hobbies do you engage in that make you lose track of time because you enjoy them so much? What is it about these activities that you find so engaging?",
        "What do others frequently compliment you on? Are there any particular strengths or attributes that people often acknowledge about you?",
        "Can you describe a situation or task where you became so absorbed that you didn’t notice the passage of time? What were you doing, and why do you think it had that effect on you?",
        "Are there specific topics or areas that, when you talk or think about them, you feel a surge of enthusiasm or excitement? What subjects or fields ignite your curiosity and passion the most?"
    ]
    
    # Initialize session state
    initialize_session_state()
    
    st.title("Discover Your Uniqueness and Identify Ideal Roles")
    st.write('''Uncovering what makes you unique is a journey of self-discovery that can guide you toward roles and activities that 
             resonate deeply with your strengths and passions.Let's embark on this journey together. Take your time to reflect on each question, 
             and provide your answers below.''')

    # Display questions and text areas
    for i, question in enumerate(questions):
        st.write(f"**Question {i + 1}:** {question}")
        answer_key = f'q{i + 1}'
        st.session_state.answers[answer_key] = st.text_area(f"Your Answer {i + 1}:", value=st.session_state.answers[answer_key], key=answer_key)
    
    # Submit button
    if st.button("Submit"):
        st.write("Thank you for your responses!")
        st.write("Analyzing and genrating your report")

        # Initialize progress bar
        with st.spinner('Generating white paper summary...'):
            progress_bar = st.progress(0)
            # Generate the docx binary stream
            doc_stream = analyze(st.session_state.answers)
            
            # Update progress bar
            progress_bar.progress(100)
            
            # Provide download link for the .docx file
            st.download_button(
                label="Download Report",
                data=doc_stream,
                file_name="Uniqueness_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        # Optionally, reset answers after submission
        # initialize_session_state() 

if __name__ == '__main__':
    main()
