from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import load_tools
from langchain.vectorstores import Pinecone
from embeddings import Embeddings_pipeline
from HuggingFaceModel import MyHuggingFaceModel
import os
from pinecone_initializer import pinecone

class RagAgent():

    def __init__(self,hf_model_id):
        self.hf = MyHuggingFaceModel(hf_model_id)
        self.llm = self.hf.create_langchain_model()
        '''
        In our case, lets have FLask session state to store memory
        '''
        #self.memory = ConversationBufferMemory(memory_key='chat_history', k = 5,return_messages=True)
        self.pipeline = Embeddings_pipeline("BAAI/bge-large-en-v1.5")
        self.embed_model = self.pipeline.embed_model
        self.vectorstore = Pinecone(pinecone.Index(os.getenv('PINECONE_INDEX')), self.embed_model.embed_query, 'text')
        self.vectorstore.as_retriever(search_kwargs= {"k":2})

    def create_bot(self):
        return ConversationalRetrievalChain.from_llm(
            llm = self.llm, 
            chain_type="stuff", 
            retriever=self.vectorstore.as_retriever(search_kwargs = {"k":2}))
        
        #result = chain({"question": "what does a human energy field convery?","chat_history":chain.get_chat_history })