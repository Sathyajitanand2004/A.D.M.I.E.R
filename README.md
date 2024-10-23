# AI-Driven Medical History Insertion and Expert Retrieval (A.D.M.I.E.R)
A.D.M.I.E.R is an AI-driven chatbot system for secure medical record storage and retrieval, enhancing healthcare decision-making efficiency

Here's a detailed project description and `README.md` file formatted for pushing to GitHub for your A.D.M.I.E.R project.

---



### **Project Description:**

**A.D.M.I.E.R** is an innovative AI-powered application designed to streamline and optimize the storage and retrieval of patient medical records. In today's fast-paced healthcare environment, timely and accurate access to patient history is crucial for providing optimal care. A.D.M.I.E.R leverages Artificial Intelligence to analyze health records and provide healthcare professionals with accurate, evidence-based answers to their queries, thereby improving diagnosis and treatment efficiency.

Key features of **A.D.M.I.E.R** include:
- **AI-driven analysis** of medical histories to offer timely and accurate insights.
- **Strong data security protocols**, including OTP verification and alert messages, ensuring patient privacy and preventing unauthorized access.
- **Easy-to-use interface** for healthcare professionals to input, update, and access medical records.
- **OpenAI integration** for understanding doctors' inquiries and providing evidence-based responses.

With the help of A.D.M.I.E.R, healthcare workers can easily store, retrieve, and analyze patients' historical medical records, improving decision-making and patient outcomes.

---

### **Installation and Setup**

To set up and run the **A.D.M.I.E.R** application locally, follow the steps below:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ADMIER.git
   cd ADMIER
   ```

2. **Set Up a Virtual Environment:**
   
   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. **Install the Required Dependencies:**

   Install all the necessary packages by running:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure you have the following packages specified in `requirements.txt`:

   ```txt
   python==3.11.9
   streamlit==1.26.0
   psycopg2==2.9.7
   langchain==0.0.271
   openai==0.27.8
   chromadb==0.3.25
   pandas==2.1.1
   ```

4. **Run the Application:**

   Once everything is set up, run the application using the following command:

   ```bash
   python -m streamlit run ADMIER.py
   ```

   This will launch the **A.D.M.I.E.R** web application in your browser.

---


### **How A.D.M.I.E.R Works:**

1. **Medical History Insertion:**  
   Healthcare professionals can input patient medical history using an intuitive user interface. The system stores this data securely in a database.

2. **Expert Retrieval and Analysis:**  
   The AI model, powered by OpenAI's machine learning capabilities, can analyze medical histories and provide accurate responses to health-related queries from medical workers.

3. **Data Security:**  
   Patient data is protected by advanced security features such as OTP verification to ensure unauthorized access is prevented.

---

### **Contributing:**

Contributions are welcome! Please fork this repository and submit a pull request for any features, improvements, or bug fixes.

---



