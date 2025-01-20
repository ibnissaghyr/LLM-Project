import os
import streamlit as st
from few_shots import few_shots
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
import chromadb
# Clear ChromaDB cache to avoid tenant connection issues
chromadb.api.client.SharedSystemClient.clear_system_cache()
os.environ["OPENAI_API_KEY"] = "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"


def get_few_shot_db_chain():
    DRIVER_NAME = 'ODBC Driver 17 for SQL Server'  # Adjust this to your specific driver
    SERVER_NAME = 'DESKTOP-SLHTD61\SQLEXPRESS'
    DATABASE_NAME = 'electronics_store'

    # Connection string adjusted for trusted connection (no need for uid if using Windows authentication)
    connection_string = (
        f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}?driver={DRIVER_NAME}&trusted_connection=yes"
    )

    # Create an instance of SQLDatabase
    db = SQLDatabase.from_uri(connection_string, sample_rows_in_table_info=3)

    # Display table information
    print(db.table_info)

    llm = OpenAI(temperature=0.9, max_tokens=500)
    embeddings = OpenAIEmbeddings()

    # Prepare few-shot examples
    to_vectorize = [" ".join(example.values()) for example in few_shots]

    from chromadb.config import Settings
    client_settings = Settings(
        chroma_api_impl="local",  # Use "rest" for server setup
        persist_directory="./chroma_db"  # Specify a local directory for storage
    )


    vectorstore = Chroma.from_texts(to_vectorize, embeddings,metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

    # Define MySQL-style prompt template
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    No pre-amble.
    """

    # Define the example prompt
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    # Define the few-shot prompt template
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],  # These variables are used in the prefix and suffix
    )

    # Initialize SQLDatabaseChain with LLM and database
    chain = SQLDatabaseChain.from_llm(llm,db, verbose=True, prompt=few_shot_prompt)

    return chain

if __name__=="__main__":
    chain=get_few_shot_db_chain()
    print(chain.run("If all Sony Tablets are sold today at their listed prices, what would be the total revenue?"))