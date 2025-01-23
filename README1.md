# **LuminoDB 🚀**

**LuminoDB** is an intelligent solution for simplifying SQL queries using few-shot learning and language models (LLMs) to process natural language questions and convert them into SQL queries for efficient database interaction. The project integrates with a SQL Server database to answer user questions based on the content of the database.

## **Features**

- **Natural Language to SQL**: Automatically converts natural language questions into SQL queries.
- **Few-Shot Learning**: Uses a small number of examples to improve SQL query generation and learning.
- **SQL Server Integration**: Connects to an SQL Server database for real-time data retrieval.
- **Streamlit Interface**: Provides an interactive web interface where users can ask questions and receive answers from the database.

## **Installation**

Follow these steps to set up the project on your local machine:

### **Prerequisites**

Ensure you have the following installed:

- Python 3.8 or higher
- SQL Server (or an accessible instance of SQL Server)

### **Step 1: Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/luminodb.git
cd luminodb
```
### **Step 2: Install Required Packages**

Use `pip` to install the necessary dependencies:

```bash
pip install -r requirements.txt
```
### **Step 3: Set Up the Database Connection**

1. **Install the necessary SQL Server driver**  
   You need to install the **ODBC Driver 17 for SQL Server** to connect to your database. You can download it from the official Microsoft website or use the following command to install it:

   ```bash
   # For Linux
   sudo apt-get install unixodbc-dev
   sudo apt-get install msodbcsql17

   # For Windows
   # Download the driver from https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   ```
**Run the Streamlit app**  
   - [ ] Launch the Streamlit app with the following command:
     ```bash
     streamlit run app.py
     ```
  

