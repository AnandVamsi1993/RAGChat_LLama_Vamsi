import pinecone
import os

pinecone.init(
    api_key= os.getenv('PINECONE_API_KEY'),
    environment= os.getenv('PINCECONE_ENVIRONMENT')
)