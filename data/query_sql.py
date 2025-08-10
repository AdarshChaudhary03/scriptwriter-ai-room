from langchain_community.utilities import SQLDatabase
from langchain.chains import SQLDatabaseChain
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini wrapper for LangChain
import os

# 2️⃣ Connect to SQLite database
db = SQLDatabase.from_uri("sqlite:///scripts.db")

# 3️⃣ Use Gemini model (free tier supports gemini-pro)
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# 4️⃣ Create SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# 5️⃣ Example query
response = db_chain.run("List all sections and their contents from the script.")
print("\n💬 Query Response:\n", response)
