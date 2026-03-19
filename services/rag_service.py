import os
import faiss
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from congif import OPENROUTER_API_KEY, BASE_URL, MODEL
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI

#Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

INDEX_PATH = "vectorstore"

#process the pdf file
def process_pdf(file_path:str):

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        add_start_index = True
    )
    
    chunks = splitter.split_documents(docs)

    embedding_dim = len(embeddings.embed_query("Hello world"))
    index = faiss.IndexFlatL2(embedding_dim)

    vectorstore = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore= InMemoryDocstore(),
        index_to_docstore_id={}
    )
    vectorstore.add_documents(documents=chunks)

    vectorstore.save_local(INDEX_PATH)

    return len(chunks)


#load the saved index
def _load_vectorstore():

    if not os.path.exists(INDEX_PATH):
        raise ValueError("No document indexed yet. Please upload a PDF first.")
    return FAISS.load_local(INDEX_PATH,embeddings=embeddings,allow_dangerous_deserialization=True)


#retrive relevant chunks
def retrive_context(query:str,k: int =4):
    vectorstore = _load_vectorstore()
    retriver = vectorstore.as_retriever(
       search_type = "similarity",
       search_kwargs = {"k":k} 
    )

    results: list[Document] = retriver.invoke(query)

    return "\n\n".join([doc.page_content for doc in results])

#full rag pipeline
def rag_query(question:str):

    context = retrive_context(question)

    prompt = f"""Answer the question using ONLY the context below.
    If the answer is not in the context, say "I couldn't find that in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    messages =[
        {
            "role": "system",
            "content": "You are a helpful AI tutor that answers questions based on provided document context.",
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = client.chat.completions.create(model=MODEL,messages=messages)
        if response and response.choices:
            return response.choices[0].message.content
        return "No respone from model"
    except Exception as e:
        print("Rag LLM Error:",e)
        return f"Error: {str(e)}"
