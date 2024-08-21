import pathlib
import textwrap
import time
import google.generativeai as genai
from docx import Document
from doc import create_word_document
from io import BytesIO
import streamlit as st

# Access your secret API key
ak = st.secrets["genai"]["api_key"]

genai.configure(api_key=ak)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

def analyze(x):
    model=genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction='''As a Career Counselor, your job is to assess candidates' responses to questions about 
        their skills, experiences, hobbies, strengths, and passions. 
        Your goal is to identify their unique qualities and suggest career roles that align with their strengths and interests.
        output instructions:while you giving answer, don't give me again headings like summary table or challenges etc., just give me the content.''')

    chat = model.start_chat(history=[])

    print(chat)

    msg ='''Ok, now I will give the questions and answers, then I will ask you to generate the visual summary table 
    and the summary of uniqueness in two paragraphs and add a section with challenges to help the person grow professionally. I will ask you to generate 
    these one by one, while you giving answer, don't give me again headings like summary table or challenges etc., just give me the content.
    understand?'''
    r = chat.send_message(msg)
    print(r.text)

    msg=f'''
    I need you to Discover my Uniqueness and Identify Ideal Roles for me as a job to work based on the below questions and answers.

    1. Skills and Talents
    What are the skills or talents you possess that you are most proud of? Which of these skills do you feel come naturally to you?
    {x['q1']}

    2. Impactful Experiences
    Reflecting on your past experiences, which moments or achievements stand out as the most fulfilling or impactful for you? Why do they stand out?
    {x['q2']}

    3. Enjoyable Activities
    What activities or hobbies do you engage in that make you lose track of time because you enjoy them so much? What is it about these activities that you find so engaging?
    {x['q3']}


    4. Recognized Strengths
    What do others frequently compliment you on? Are there any particular strengths or attributes that people often acknowledge about you?
    {x['q4']}

    5. Flow State
    Can you describe a situation or task where you became so absorbed that you didn’t notice the passage of time? What were you doing, and why do you think it had that effect on you?
    {x['q5']}

    6. Passionate Topics
    Are there specific topics or areas that, when you talk or think about them, you feel a surge of enthusiasm or excitement? What subjects or fields ignite your curiosity and passion the most?
    {x['q6']}

    I give you the information, now I will ask you to generate the visual summary table and the summary of uniqueness in two paragraphs and add a section with challenges to help the person grow professionally one
    by one. 
    don't give the content now, i will ask you the content one by one.
    '''
    r = chat.send_message(msg)
    print(r.text)

    con = {}
    msg = 'generate a visual summary table'
    r = chat.send_message(msg)
    con['table'] = r.text
    print(r.text)

    msg = 'generate the summary of uniqueness in two paragraph'
    r = chat.send_message(msg)
    con['summary'] = r.text
    print(r.text)

    msg = 'generate a section with challenges to help the person grow professionally one'
    r = chat.send_message(msg)
    con['challenges'] = r.text
    print(r.text)

    print(con)

    d = create_word_document(con)
    doc_stream = BytesIO()
    d.save(doc_stream)
    doc_stream.seek(0)  # Rewind the buffer to the beginning
    return doc_stream.getvalue()  # Return binary data





