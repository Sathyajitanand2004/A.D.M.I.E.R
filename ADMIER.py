from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage,AIMessage,HumanMessage
import streamlit as st
import datetime
import psycopg2
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
import os
import csv
import pandas as pd

host="localhost"
user="postgres"
database="medical_data"
password="sjvisami"
port="5432"

connection=psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

cursor=connection.cursor()

if 'page' not in st.session_state: st.session_state.page = 0
def login(): st.session_state.page = 0
def signup(): st.session_state.page = 1
def mode():st.session_state.page=2
def register():st.session_state.page=3
def insert():st.session_state.page=4
def retreival():st.session_state.page=5
ph = st.empty()

count1=0

if st.session_state.page == 0:
    with ph.container():
        st.sidebar.markdown("## Feedback & Support")
        if st.sidebar.button("Provide Feedback"):
            feedback_text = st.text_area("Your Feedback", "")
            if feedback_text:
                st.write(f"Thank you for your feedback: {feedback_text}")

        if st.sidebar.button("Report an Issue"):
            st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")

    
        st.markdown("<h1 style='text-align: center; color: red;'>A.D.M.I.E.R</h1>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center; color: red;'>AI-Driven Medical History Insertion and Expert Retreival</h6>", unsafe_allow_html=True)
        tab1,tab2,tab3,tab4= st.tabs(["login","About","Help","Terms & Conditions"])

        with tab2:
            st.write("A.D.M.I.E.R is a web-application that doctors use to insert and retrieve patient data quickly.")
            

        with tab1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if username and password:
                    try:
                        query="SELECT COUNT(*) from healthcare_expert where license_no=%s and password=%s ;"
                        data=(username,password)
                        cursor.execute(query,data)
                        count=cursor.fetchone()[0]
                        if(count==0):
                            st.write("LOGIN FAILED PLEASE SIGNUP")
                            st.session_state.page=0
                        else:
                            st.success("LOGIN SUCCESSFULLY")
                            st.session_state.page=2
                    except psycopg2.IntegrityError as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()

            if st.button("Sign Up"):
                st.session_state.page=1

        with tab3:
            st.write("Contact fffd@gmail.com for more details")
            st.markdown("""
<style>
    div.stButton > button:first-child {
        border: 2px solid #35629e;
        border-radius: 5px;
        background-color: #35629e;
        color: white;
    }
    h2 {
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

        
elif st.session_state.page == 1:
    with ph.container():
    
        st.markdown("<h1 style='text-align: center; color: red;'>REGISTRATION FOR DOCTOR</h1>", unsafe_allow_html=True)
 

        st.sidebar.markdown("## Feedback & Support")
        if st.sidebar.button("Provide Feedback"):
            feedback_text = st.text_area("Your Feedback", "")
            if feedback_text:
                st.write(f"Thank you for your feedback: {feedback_text}")

            if st.sidebar.button("Report an Issue"):
                st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")
        tab1,tab2,tab3,tab4= st.tabs(["Sign Up","About","Help","Terms & Conditions"])
        with tab2:
            st.write("This is the sign-up page for medical professionals.")
            st.write("Use this page to sign up and access our web app!")

        with tab3:
            st.write("Contact dfw@gmail.com!")

        with tab4:
            st.write("Check our terms and conditions")
            st.markdown("[T&C](https://policies.google.com/terms?hl=en-US)")

        with tab1:
            words = st.text_input("Enter your name:")
            st.write("You entered:", words)

            phone = st.text_input("Enter your phone number:", max_chars=10)

            username = st.text_input("Enter your LICENSE NUMBER :", max_chars=20)
            st.caption("Username must be the same as your doctor ID")
            password = st.text_input("Create a password", max_chars=20, type="password")
            st.caption("At least 8 characters")

            if st.button("SIGN UP"):
                if words and phone and username and password:
                    try:
                        query="INSERT INTO healthcare_expert(license_no,name,phone_no,password) Values('{id}','{name}',{ph},'{passw}');".format(id=username,name=words,ph=phone,passw=password)
                        cursor.execute(query)
                        connection.commit()
                    except psycopg2.IntegrityError as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()
                st.session_state.page=0
        st.markdown("""
<style>
    div.stButton > button:first-child {
        border: 2px solid #35629e;
        border-radius: 5px;
        background-color: #35629e;
        color: white;
    }
    h2 {
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)


elif st.session_state.page == 2:
    with ph.container():
        st.markdown("<h1 style='text-align: center; color: red;'>HEY DOC 🩺!</h1>", unsafe_allow_html=True)
        
        tab1,tab2,tab3,tab4= st.tabs(["----->","Insert mode","Retrieval mode","Terms & Conditions"])
        with tab2:
            st.header("What is INSERT MODE?")
            st.write("With th help of insert mode you can input patient details into the database")
        with tab3:
            st.header("What is RETRIEVAL MODE?")
            st.write("With th help of retrieval mode you can fetch patient details with the help of an AI integrated chat-bot")
        with tab4:   
            st.write("check our terms and conditions")
            st.markdown("[T&C](https://policies.google.com/terms?hl=en-US)")

        patient_id = st.text_input("Enter the patient ID:", max_chars=12)
        id1=patient_id
        if id1:
            try:
                query1="SELECT COUNT(*) FROM patient_details WHERE patient_id={id}".format(id=id1)
                cursor.execute(query1)
                count1 = cursor.fetchone()[0]
                if count1 == 0:
                    st.write("Patient id is not present please click on New patient? REGISTER")
                else:
                    st.write("Patient id is present. Now select any mode")
                    pt_id=patient_id
            except Exception as e:
                connection.rollback()
                st.error(f"Error inserting patient ID: {str(e)}")
            finally:
                cursor.close()
        if st.sidebar.button("About"):
            st.sidebar.markdown("## ABOUT")
            st.sidebar.write("This is the page for inserting patient details.")
            st.sidebar.write("You can insert patient data, which will be stored in the database.")

        if st.sidebar.button("Help"):
            st.sidebar.markdown("## HELP")
            st.sidebar.write("This is the help page with information about the app's objectives.")

        if st.sidebar.button("CONTACT"):
            st.sidebar.markdown("## CONTACT")
            st.sidebar.write("This innovation is done by the students of SMARKLINKERS.")
            st.sidebar.write("If you have any queries, please contact them.")
        st.sidebar.markdown("## Feedback & Support")
        if st.sidebar.button("Provide Feedback"):
            feedback_text = st.text_area("Your Feedback", "")
            if feedback_text:
                wonder =st.write(f"Thank you for your feedback: {feedback_text}")
        if st.sidebar.button("Report an Issue"):
            st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")
        selected_var= st.selectbox("select an option :",["REGISTER","INSERT","RETREIVAL"])
        if selected_var=="INSERT" and count1>=1:
            if st.button("INSERT"):
               st.session_state.page=4

        elif selected_var=="RETREIVAL" and count1>=1:
            if st.button("RETREIVAL"):
                st.session_state.page=5

        elif selected_var=="REGISTER" and count1==0:
            if st.button("REGISTER"):
                st.session_state.page=3
        st.markdown("""
<style>
    div.stButton > button:first-child {
        border: 2px solid #35629e;
        border-radius: 5px;
        background-color: #35629e;
        color: white;
    }
    h2 {
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

elif st.session_state.page==3:
    st.markdown("<h1 style='text-align: center; color: red;'>REGISTER THE PATIENT DETAILS</h1>", unsafe_allow_html=True)

    st.sidebar.markdown("## Feedback & Support")
    if st.sidebar.button("Provide Feedback"):
        feedback_text = st.text_area("Your Feedback", "")
        if feedback_text:
          st.write(f"Thank you for your feedback: {feedback_text}")
    if st.sidebar.button("Report an Issue"):
        st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")

    tab1, tab2, tab3, tab4 = st.tabs(["------>", "About", "Help", "Terms & Conditions"])

    with tab2:
        st.write("This is the page where you can register the patient")

    with tab3:
        st.write("Queries? Write to saddkw@gmail.com")

    with tab4:
        st.write("Check our terms and conditions")
        st.markdown("[T&C](https://policies.google.com/terms?hl=en-US)")

    words = st.text_input("Enter your name:")
    dob = st.date_input("Select your Date Of Birth", datetime.date(2019, 7, 6), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    st.write('Your birthday is:', dob)
    gen = st.selectbox("Select an option:", ["Male", "Female"])
    patient_id = st.text_input("Enter the Patient Id :", max_chars=12)
    license=st.text_input("Enter the License No : ")

    if st.button("SUBMIT"):
        if words and dob and gen and patient_id and license:
            try:
                query = "INSERT INTO patient_details(patient_id, patient_name, patient_gender, patient_dob, license_no) VALUES(%s, %s, %s, %s, %s)"
                data = (patient_id, words, gen, dob,license)
                cursor.execute(query, data)
                connection.commit()
                st.success("REGISTERED SUCCESSFULLY")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                connection.close()
        st.session_state.page=2
        st.markdown("""
<style>
    div.stButton > button:first-child {
        border: 2px solid #35629e;
        border-radius: 5px;
        background-color: #35629e;
        color: white;
    }
    h2 {
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)


elif st.session_state.page==4:
    
    st.markdown("<h2 style='text-align: center; color: red;'>INSERT THE PATIENT MEDICAL RECORDS</h2>", unsafe_allow_html=True)

    if st.sidebar.button("Provide Feedback"):
        feedback_text = st.text_area("Your Feedback", "")
        if feedback_text:
           wonder =st.write(f"Thank you for your feedback: {feedback_text}")
    if st.sidebar.button("Report an Issue"):
        st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")
    tab1,tab2,tab3,tab4= st.tabs(["----->","About","Help","Terms & Conditions"])
    with tab2:
        st.write("you can insert patient details into the databse")
    with tab3:
        st.write("queries?....write to saddkw@gmail.com")
    with tab4:   
        st.write("check our terms and conditions")
        st.markdown("[T&C](https://policies.google.com/terms?hl=en-US)")
    d = st.date_input("Date of visit to the hospital ", datetime.date(2019, 7, 6), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2050, 12, 31))
    hosp=st.text_input("Enter the HOSPITAL name:")
    val=st.text_area("Enter the patient Illness statement :")
    code=st.text_input("Enter the diagonistic code ")
    st.caption(" Diagnostic code is the translation of written descriptions of diseases, illnesses and injuries")
    lab_values=st.text_area("Enter the Lab values for the Patient : ")
    patient_id=st.text_input("Enter the Patient Id : ",max_chars=12)

    if st.button("Submit"):
        if d and hosp and val and code and patient_id and lab_values :
            try:
                cursor=connection.cursor()
                query="INSERT INTO patient_illness(patient_date_of_checkup,hospital_name,patient_illness_statement,patient_diagnosis_code,patient_id) Values(%s,%s,%s,%s,%s,%s);"
                data=(d,hosp,val,code,patient_id,lab_values)
                cursor.execute(query,data)
                connection.commit()
                st.write("INSERTED SUCCESSFULLY")
            except psycopg2.IntegrityError as e:
                print(f"Error:{e}")
            finally:
                connection.commit()
                connection.close()
        st.session_state.page=2
        st.markdown("""
<style>
    div.stButton > button:first-child {
        border: 2px solid #35629e;
        border-radius: 5px;
        background-color: #35629e;
        color: white;
    }
    h2 {
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)


elif st.session_state.page==5:
    if st.sidebar.button("About"):
        st.sidebar.markdown("## ABOUT")
        st.sidebar.write("This is the page for inserting patient details.")
        st.sidebar.write("You can insert patient data, which will be stored in the database.")

    if st.sidebar.button("Help"):
        st.sidebar.markdown("## HELP")
        st.sidebar.write("This is the help page with information about the app's objectives.")

    if st.sidebar.button("CONTACT"):
        st.sidebar.markdown("## CONTACT")
        st.sidebar.write("This innovation is done by the students of SMARKLINKERS.")
        st.sidebar.write("If you have any queries, please contact them.")

    st.sidebar.markdown("## Feedback & Support")
    if st.sidebar.button("Provide Feedback"):
        feedback_text = st.text_area("Your Feedback", "")
        if feedback_text:
            st.write(f"Thank you for your feedback: {feedback_text}")

    if st.sidebar.button("Report an Issue"):
        st.sidebar.write("https://www.mediacollege.com/internet/troubleshooter/report-website-problem.html")
    cursor=connection.cursor()
    count=0

    pt_id=st.text_input("Enter the Patient ID : ",max_chars=12)
    if pt_id:
        query="SELECT COUNT(*) FROM patient_details where patient_id=%s;"
        data=(pt_id,)
        cursor.execute(query,data)
        count=cursor.fetchone()[0]
        if(count==0):
            st.write("The patient id is not avaible in the database")

        else:
            st.write("The patient id is present.Now you can ask the message")
            sql_query = """SELECT patient_details.patient_id, patient_name,patient_date_of_checkup,patient_diagnosis_code, patient_illness_statement
        FROM healthcare_expert
        INNER JOIN patient_details ON healthcare_expert.license_no = patient_details.license_no
        INNER JOIN patient_illness ON patient_details.patient_id = patient_illness.patient_id
        WHERE patient_details.patient_id={pt_id}
        """.format(pt_id=pt_id)

        df = pd.read_sql_query(sql_query, connection)

        connection.close()

        csv_file_path = 'patient_record.csv'

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)

        print(f'Data has been exported to {csv_file_path}')
        os.environ['OPENAI_API_KEY']="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"

        loader = TextLoader("patient_record.csv")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)
        qa = RetrievalQA.from_chain_type(llm=OpenAI(model='gpt-4'), chain_type="stuff", retriever=docsearch.as_retriever())
        
        # Shortened prompt
        prompt = "Role: Doctor. Analyze the question , answer related to patient: [question]:"
        
        st.session_state.chat_history = []
        st.markdown("<h1 style='text-align: center; color: red;'>MED BOT</h1>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center; color: red;'>Hello! I'm your retrieval bot. You can ask anything you want.</h6>", unsafe_allow_html=True)
        
        user_input = st.chat_input("Enter your message:")
        if user_input:
            st.markdown(f"<p style='text-align: right; color: dark blue;'>🧑‍⚕ You: {user_input}</p>", unsafe_allow_html=True)
            if len(prompt + user_input) < 2000:  # Ensuring the token limit isn't exceeded
                output = qa.run(prompt + user_input)
                bot_response = f"You said: {output}"
                st.text_area("🤖", f" {bot_response}")
            else:
                st.write("Your query is too long. Please make it more concise.")
    else:
        st.write("Enter the Patient Id first. So you can retrieve the data")