from flask import Flask, jsonify, request,render_template
from tinydb import TinyDB
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app) 

# Instanciando o banco de dados e os logs  
db = TinyDB('db.json')
logs = TinyDB('logs.json')

# Rota da página home
@app.route('/')
def ola():
    return render_template('home.html')

# Rota que acessa a pagina de dash com os logs de acessos 
@app.route('/dash')
def retorna_acessos():
    return render_template('dash.html', itens=logs.all())

@app.route('/info')
def return_info():
    return render_template('info.html')



# Função para adicionar logs
def add_log(message):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.insert({'Data e horario': current_date, 'Tipo de requisicao': message})

# Rota ping 
@app.route('/ping', methods=['GET'])
def ping():
    add_log(message= 'GET /ping')
    return jsonify({'resposta': 'pong'})

# Rota ECHO 
@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    try:
        db.insert(data)
        data_user_sent = data.get('dados')
        add_log(message= f'POST /echo os dados enviados foram:  {data_user_sent}')
        return jsonify({'resposta': data_user_sent})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# Fetch nos logs 
@app.route('/all-logs', methods=['GET'])
def all_logs():
    return jsonify(logs.all())

# Fetch nos dados do banco de dados 
@app.route('/all-data', methods=['GET'])
def all_data():
    return jsonify(db.all())



if __name__ == "__main__":
    app.run(debug=True)

