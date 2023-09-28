from torch import cuda
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from flask import redirect,flash
from pinecone_initializer import pinecone


class Embeddings_pipeline():

    def __init__(self, embed_model_id) -> None:
        self.device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
        self.embed_model_id = embed_model_id
        self.embed_model = HuggingFaceBgeEmbeddings(model_name=embed_model_id,
                                         model_kwargs={'device': self.device},
                                         encode_kwargs={'normalize_embeddings': True},
                                         query_instruction="为这个句子生成表示以用于检索相关文章：")

        

    '''
        This function pulls the necessary file from an S3 bucket and uploads 1024 dimensions embeddings vector
        to pinecone vector database.

        I am currently working on Runpod GPU clouds. So, S3 code is greyed out
    '''
    def lambda_pinecone_upsert_vectors(self,file_path,chunk_size,chunk_overlap):
        #loader = AmazonTextractPDFLoader(file_path=file_path,region_name='us-east-1')
        try:

            if not all(os.getenv(var) for var in ['PINECONE_API_KEY', 'PINCECONE_ENVIRONMENT', 'PINECONE_INDEX']):
                flash('Error adding Embeddings. Please check your file')
                return redirect('/')
        

            loader = PyPDFLoader(file_path=file_path)
            pages = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
            text_chunks = text_splitter.split_documents(pages)
            
            
            index = pinecone.Index(os.getenv('PINECONE_INDEX'))

            for i in range(0,len(text_chunks), 32):
                i_end = min(i+32,len(text_chunks))
                batch = text_chunks[i:i_end]
                texts = [x.page_content for i,x in enumerate(batch)]
                texts = [content.replace('\t', '') for content in texts]
                ids = ['{}-chunk-{}-iter-{}'.format(x.metadata['source'].split('/')[-1],i,j) for j, x in enumerate(batch)]
                embeds = self.embed_model.embed_documents(texts)
                metadata = [{'page':x.metadata['page'],
                            'source':x.metadata['source'].split('/')[-1],
                            'text': texts[i]}

                            for i,x in enumerate(batch)]
                index.upsert(vectors = zip(ids,embeds,metadata))
            print('Upserted them all')

        except pinecone.PineconeException as pc_exc:
            flash('Some error related to Pinecone upsertion! Please check your API keys')
            return redirect('/')
        except Exception as e:
            print(e)
            flash('Error adding Embeddings. Please check your file')
            return redirect('/')

        return 'Embeddings upserted succesfully'






