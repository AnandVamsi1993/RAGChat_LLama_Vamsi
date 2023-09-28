from flask import Flask,jsonify,request,redirect,flash,render_template
from boto3 import client,resource
import botocore
import os
from dotenv import load_dotenv
import requests
from embeddings import Embeddings_pipeline

load_dotenv()

def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('Please choose a file', 'error')
        return redirect('/')
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('Please choose a file', 'error')
        return redirect('/')
    
    #Check if the content type is pdf
    if file.content_type != 'application/pdf':
        flash('Please upload a pdf file', 'error')
        return redirect('/')
    
    file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), file.filename)

    if not os.path.exists(file_path):
        file.save(file_path)
        #We chunk the document and upload the embeddings to Pinecone vector database
        embedding = Embeddings_pipeline("BAAI/bge-large-en-v1.5")
        embedding.lambda_pinecone_upsert_vectors(file_path=file_path,chunk_size= 1000,chunk_overlap= 20)

    return redirect('/')


























    '''
    Below code can be used if we want to upload everything on S3. As I am not working on AWS at the moment, I will skip this

    try:
        s3_client.head_object(Bucket = bucket_name,Key = filename)
        print('Exists')
        flash('File is already uploaded', 'error')
        return redirect('/')
    except botocore.exceptions.ClientError as e:
        print('Line 34')
        s3_params = {
            'Bucket': bucket_name,
            'Key': filename,
            'ContentType': content_type
            #'ExpiresIn': url_expiration_seconds
        }



        upload_url = s3_client.generate_presigned_url('put_object', Params=s3_params)

        # Use requests to put the file to the presigned url
        response = requests.put(upload_url, data=file.read(), headers={'Content-Type': content_type})
        response = requests.put(upload_url, data=file.read(), headers={'Content-Type': content_type})

        if response.status_code == 200:
            return redirect('/')
            #return jsonify({'success': True, 'url': f"{bucket_name}/{filename}"}), 200
        else:
            flash('Server error: Cannot upload the file', 'error')
            return redirect('/')
    
    
    
    '''
    