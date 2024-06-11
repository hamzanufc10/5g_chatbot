from flask import Flask,render_template,url_for,request,redirect
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAI



app=Flask(__name__)



api_key="AIzaSyDg9wGOexphTK8JbhbufWZ6idMuZdkZi8M"
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)


from langchain.document_loaders.csv_loader import CSVLoader
loader = CSVLoader(file_path='5g_faq.csv', source_column="prompt")
# Store the loaded data in the 'data' variable
data = loader.load()

instructor_embeddings =  SentenceTransformerEmbeddings(model_name="paraphrase-MiniLM-L6-v2")


from langchain.vectorstores import FAISS

# Create a FAISS instance for vector database from 'data'
vectordb = FAISS.from_documents(documents=data,
                                 embedding=instructor_embeddings)

# Create a retriever for querying the vector database
retriever = vectordb.as_retriever(score_threshold = 0.7)

from langchain.prompts import PromptTemplate

prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""


PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}


from langchain.chains import RetrievalQA

chain = RetrievalQA.from_chain_type(llm=llm,
                            chain_type="stuff",
                            retriever=retriever,
                            input_key="query",
                            return_source_documents=True,
                            chain_type_kwargs=chain_type_kwargs)








@app.route('/',methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        a=str(request.form['user_input'])
        b=chain(a)
        return render_template("home.html",ans=b['result'])

if __name__=="__main__":
    app.run(debug=True)