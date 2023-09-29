# RAGChat_LLama_Vamsi
Retrieval Augmented text Generation for LLms. A simple Chatbot that harnesses sentence similarity with a given document and chat history to improve performance of 
LLm's , which are prone for hallucinations.

Here a llama2 7-billion model is used as an LLM. 

Steps:

1) Upload a document and use an Embeddings pipeline object to perform text cleaning, chunking and embeddings.
2) Use the object's attributes to generate embeddings and save them in Pinecone Vector Database.
3) Initialize a RagAgent object which has a bot like attribue to save conversations and context.
4) Build a simple react app and fetch API call requests from flask. Integrate the two by building react.js modules.
5) Store chat messages from the bot and Human in session storage.Can also use Databases like Dynamo DB to save chat history.

# Model Architecture

My application mimics the following AWS architecture, except I built this whole thing in Runpod.io as it was cheaper.




![ChatBot_RAG - ChatBot_Architecture](https://github.com/AnandVamsi1993/RAGChat_LLama_Vamsi/assets/52344613/4bb04519-5d6d-49de-a8ca-4f78882782db)


So something similar in Runpod does this:
![RAG_Architecture](https://github.com/AnandVamsi1993/RAGChat_LLama_Vamsi/assets/52344613/7eb77d21-3d8f-44b7-a8d2-fb6ba4ae2aba)


##Instructions

###Prerequisites - Docker should be installed

1) Clone rhe repository to your local machine/remote server
2) docker build -t bluellama .
3) docker run --env-file .env -p 5000:5000 bluellama


Building the image takes ~300 seconds



