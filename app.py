from flask import Flask, request, jsonify, redirect, flash,render_template,session,logging,send_from_directory
import os
from ChatBot import RagAgent
from flask import make_response
from pinecone_initializer import pinecone
from embeddings import Embeddings_pipeline


app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = False


#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, 'build', path)):
        print("path for ", path, " is " ,os.path.join(app.static_folder, 'build'), path)
        return send_from_directory(os.path.join(app.static_folder, 'build'), path)
    else:
        return send_from_directory(os.path.join(app.static_folder, 'build'), 'index.html')


'''
 def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

'''





@app.route('/chat_history', methods = ['GET'])
#@cross_origin(origins=["http://localhost:3000/"])
def get_chat_history():
    if not session.get('chat_history', []):
        session['chat_history'] = []
    if not session.get('chat_context', []):
        session['chat_context'] = []
    result = {'chat_history': session['chat_history'], 'chat_context': session['chat_context']}
    return jsonify(result)



@app.route('/chat', methods = ['POST'], endpoint = 'chat_endpoint')
#@cross_origin(send_wildcard=True,allow_headers=['Content-Type'])
def chat():
    data = request.get_json()
    user_input = data.get('user_input')
    agent = RagAgent('meta-llama/Llama-2-7b-chat-hf')
    Mybot = agent.create_bot()
    if not session.get('chat_history', []):
        session['chat_history'] = []
        session['chat_context'] = []
    result = Mybot({'question':user_input, 'chat_history':session['chat_history']})
    result['metadata'] = Mybot.retriever.get_relevant_documents(user_input)[-1].metadata
    session['chat_history'].append((user_input,result['answer']))
    session['chat_context'].append(result['metadata'])
    session.modified = True
    return jsonify(result)

@app.route('/upload', methods=['POST'])
#@cross_origin(send_wildcard=True)
def upload():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Please choose a file'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Please choose a file'})
    
    if file.content_type != 'application/pdf':
        return jsonify({'success': False, 'error': 'Please upload a valid file'})
    
    file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), file.filename)
    
    if not os.path.exists(file_path):
        file.save(file_path)
        embedding = Embeddings_pipeline("BAAI/bge-large-en-v1.5")
        embedding.lambda_pinecone_upsert_vectors(file_path=file_path,chunk_size= 1000,chunk_overlap= 20)
    
    return jsonify({'success': True, 'message': 'File uploaded successfully'})

'''
@app.route('/')
#@cross_origin(send_wildcard=True)
def index():
    return redirect('/chat_history')

'''

  

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug= True)
