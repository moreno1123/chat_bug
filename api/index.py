from fastapi import FastAPI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.chat_models import ChatOpenAI
from langchain.chains import VectorDBQA
from langchain.retrievers.self_query.base import SelfQueryRetriever
import chromadb
import os
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import OpenAIEmbedding
from llama_index import ServiceContext, VectorStoreIndex, set_global_service_context
from langchain.chat_models import ChatOpenAI
from llama_index.llms import OpenAI
import openai
from llama_index.llms import ChatMessage, MessageRole
from llama_index.prompts import ChatPromptTemplate
from llama_index.memory import ChatMemoryBuffer
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
sys.stdout.reconfigure(encoding="utf-8")
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(docs_url="/apii/docs", openapi_url="/apii/openapi.json")

openai_key = os.getenv("OPENAI_API_KEY")
chroma_server = os.getenv("CHROMA_DB_SERVER")
openai.api_key = openai_key
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    streaming=True,
    verbose=True,
    openai_api_key=openai_key,
)

# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=("Always answer the question, even if the context isn't helpful."),
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the question: {query_str}\n"
        ),
    ),
]
text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

system_prompt = """
- You are an Croatian AI assistant that answers questions in a friendly manner.
- Provide always a detailed information about the question, which was asked.
- It is very important that if the question is not related to the source documents, always answer that "you cannot provide the answer"
- Always resond in Croatian language
"""

# system_prompt = """
# - You are an Croatian AI assistant that answers questions in a friendly manner.
# - Provide always a detailed information about the question, which was asked.
# - Always resond even if the context is not helpful
# - Always resond in Croatian language
# """


def process_llm_response(llm_response):
    print(llm_response["result"])
    print("\n\nSources:")
    for source in llm_response["source_documents"]:
        print(source)


@app.get("/apii/python")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}


@app.get("/apii/query")
def query():
    embeddings = OpenAIEmbeddings()
    embed_model = OpenAIEmbedding()
    chroma_client = chromadb.HttpClient(host=chroma_server, port=8000)
    chroma_collection = chroma_client.get_collection(
        "b5877065-aa52-4641-93ef-98966b3deb11"
    )
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        service_context=service_context,
    )
    query_engine = index.as_query_engine()
    response = query_engine.query("What types of personal information is collected?")
    # vectore_store = Chroma(
    #     client=chroma_client,
    #     collection_name="b5877065-aa52-4641-93ef-98966b3deb11",
    #     embedding_function=embeddings,
    # )
    # qa_chain = ConversationalRetrievalChain.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectore_store.as_retriever(),
    #     return_source_documents=True,
    # )
    # query = "What is the context?"
    # llm_response = qa_chain(query)
    # process_llm_response(llm_response)
    print(response)
    # print(llm_response["result"])
    # print(llm_response["source_documents"])
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}


@app.get("/apii/chat")
def chat():
    # set embbeding model
    embed_model = OpenAIEmbedding()

    # get chromadb vector store collection
    chroma_client = chromadb.HttpClient(host=chroma_server, port=8000)
    chroma_collection = chroma_client.get_collection(
        "b5877065-aa52-4641-93ef-98966b3deb11"
    )
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # set service context
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0),
        embed_model=embed_model,
        system_prompt="You are a helpfull assistant and you job is to help the user get his information in a helpful way. It is very important that you only answer question which are related to the context and if the are not answer that you cannot provide the answer",
    )

    # set vector store index
    index = VectorStoreIndex.from_vector_store(
        vector_store, service_context=service_context
    )

    # query_engine = index.as_query_engine()
    # response = query_engine.query("Who is Joe Biden? respond in croatian")

    # print(response)

    memory = ChatMemoryBuffer.from_defaults()

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=system_prompt,
        memory=memory,
    )
    response = chat_engine.stream_chat("o cemu se radi u kontekstu?")
    for token in response.response_gen:
        print("bok")
        print(token)

    for key, value in response.response_gen.items():
        print(f"{key}: {value}")

    # response = chat_engine.chat("Koji je glavni grad Hrvatske?")
    # print(response.response_gen)

    # response = chat_engine.chat("Što mogu posjetiti tamo?")
    # print(response)

    # response = chat_engine.chat("Reci mi više o tome")
    # print(response)

    # response = chat_engine.chat("Koji email?")
    # print(response)

    # response = chat_engine.chat("What is this context about?")
    # print(response)

    # set chat engine
    # chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    # stream the response
    # streaming_response = chat_engine.chat("Can you please tell me about the context?")
    # print(streaming_response)
    # for token in streaming_response.response_gen:
    #     print(token, end="")

    # vectore_store = Chroma(
    #     client=chroma_client,
    #     collection_name="b5877065-aa52-4641-93ef-98966b3deb11",
    #     embedding_function=embeddings,
    # )
    # qa_chain = ConversationalRetrievalChain.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectore_store.as_retriever(),
    #     return_source_documents=True,
    # )
    # query = "What is the context?"
    # llm_response = qa_chain(query)
    # process_llm_response(llm_response)
    # print(response)
    # print(llm_response["result"])
    # print(llm_response["source_documents"])
    # return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}
