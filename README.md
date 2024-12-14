# **ChatDB**

**ChatDB** is an innovative interactive platform designed to enhance your understanding of database querying.  
By combining the power of **natural language processing** with database management, ChatDB serves as your personal assistant for learning SQL and NoSQL query languages.  

It integrates functionality for:  
- **Database uploads**  
- **Query execution**  
- **Natural language query conversion**  
- **Sample query generation**  

---

## **Project Structure**

### **Root Directory Files**
1. **`sql_upload.py`**  
   Uploads datasets (`CSV` or `XLSX`) to an SQL server.

2. **`nosql_upload.py`**  
   Uploads datasets (`JSON` or `XML`) to a MongoDB server.

3. **`sql_execute.py`**  
   Executes SQL queries on the SQL server and returns the output.

4. **`nosql_execute.py`**  
   Executes NoSQL queries on the MongoDB server and returns the output.

5. **`sql_sample_queries.py`**  
   Generates random sample SQL queries using pattern matching.

6. **`nosql_sample_queries.py`**  
   Generates random sample NoSQL queries using pattern matching.

7. **`sql_nlp.py`**  
   Converts natural language (NL) queries into SQL queries, executes them, and returns results.

8. **`nosql_nlp.py`**  
   Converts natural language (NL) queries into NoSQL queries, executes them, and returns results.

---

### **Streamlit Directory**

The **Streamlit** directory contains the user interface components for ChatDB.

1. **`app.py`**  
   Main file to run the Streamlit application.

2. **`home.py`**  
   Home page UI for the application.

3. **`choose_db.py`**  
   UI to choose between SQL and NoSQL databases.

4. **`sql_info.py`**  
   UI to explore SQL databases.

5. **`nosql_info.py`**  
   UI to explore MongoDB databases.

6. **`execute_sql.py`**  
   Allows users to:  
   - Generate and view sample SQL queries.  
   - Query the SQL database using natural language.

7. **`execute_nosql.py`**  
   Allows users to:  
   - Generate and view sample NoSQL queries.  
   - Query the MongoDB database using natural language.

8. **`upload_db.py`**  
   Uploads datasets to SQL or NoSQL databases using the respective upload scripts.

9. **`utils.py`**  
   Contains utility functions used across the application.

10. **`requirements.txt`**  
    List of dependencies required to run the project.

---

## **Setup and Installation**

### **1. Prerequisites**

- **Python 3.8+** must be installed.  
- SQL database server (e.g., MySQL, PostgreSQL) and MongoDB setup.

### **2. Install Dependencies**

Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```
### **3. Run the Streamlit Application**

Start the Streamlit interface using:

```bash
streamlit run app.py
```
---

## **Usage**

- **Home Page**: Navigate to explore the features.  
- **Database Selection**: Choose SQL or MongoDB.  
- **Upload Databases**: Upload datasets for SQL or NoSQL using the **Upload DB** option.  
- **Query Execution**:  
  - Use **Execute SQL/NoSQL** pages to run queries.  
  - Natural language queries can be entered through the **NL SQL** and **NL NoSQL** pages.  
- **Sample Queries**: Generate and execute sample SQL/NoSQL queries.  

---

## **Dependencies**

- Python 3.x  
- Streamlit  
- Pandas  
- SQLAlchemy  
- PyMongo  
- Other dependencies as listed in `requirements.txt`  

