from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from config import Config
from database import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg'}
@app.route('/api/dados-surpresa')
def api_dados_surpresa():
    return jsonify({
        'musicas': db.dados['musicas'],
        'mensagens': db.dados['mensagens'],
        'fotos': db.dados['fotos']
    })
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/musicas')
def musicas():
    musicas = db.dados['musicas']
    return render_template('musicas.html', musicas=musicas, config=db.dados['configuracoes'])
@app.route('/')
def index():
    config = db.dados['configuracoes']
    return render_template('index.html', config=config)

@app.route('/galeria')
def galeria():
    fotos = db.dados['fotos']
    return render_template('galeria.html', fotos=fotos)

@app.route('/cartas')
def cartas():
    cartas = db.dados['cartas']
    return render_template('cartas.html', cartas=cartas)

@app.route('/timeline')
def timeline():
    datas = db.dados['datas']
    return render_template('timeline.html', datas=datas)

@app.route('/contador')
def contador():
    dados_rel = db.obter_dados_relacionamento()
    return render_template('contador.html', dados_rel=dados_rel)

@app.route('/mensagens')
def mensagens():
    mensagens = db.dados['mensagens']
    return render_template('mensagens.html', mensagens=mensagens)

@app.route('/surpresa')
def surpresa():
    return render_template('surpresa.html', dados=db.dados)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', erro='Credenciais inválidas')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', dados=db.dados)

@app.route('/admin/adicionar_foto', methods=['POST'])
def admin_adicionar_foto():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    if 'foto' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    arquivo = request.files['foto']
    if arquivo.filename == '':
        return jsonify({'erro': 'Arquivo vazio'}), 400
    
    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename(arquivo.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        
        os.makedirs('static/uploads/fotos', exist_ok=True)
        filepath = os.path.join('static/uploads/fotos', filename)
        arquivo.save(filepath)
        
        legenda = request.form.get('legenda', '')
        db.adicionar_foto(filepath, legenda)
        
        return jsonify({'sucesso': True, 'caminho': filepath})
    
    return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400

@app.route('/admin/adicionar_musica', methods=['POST'])
def admin_adicionar_musica():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    if 'musica' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    arquivo = request.files['musica']
    if arquivo.filename == '':
        return jsonify({'erro': 'Arquivo vazio'}), 400
    
    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename(arquivo.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        
        os.makedirs('static/uploads/musicas', exist_ok=True)
        filepath = os.path.join('static/uploads/musicas', filename)
        arquivo.save(filepath)
        
        titulo = request.form.get('titulo', '')
        db.adicionar_musica(filepath, titulo)
        
        return jsonify({'sucesso': True, 'caminho': filepath})
    
    return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400

@app.route('/admin/adicionar_carta', methods=['POST'])
def admin_adicionar_carta():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    
    if not titulo or not conteudo:
        return jsonify({'erro': 'Título e conteúdo são obrigatórios'}), 400
    
    db.adicionar_carta(titulo, conteudo)
    return jsonify({'sucesso': True})

@app.route('/admin/editar_carta/<int:id_carta>', methods=['POST'])
def admin_editar_carta(id_carta):
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    
    if not titulo or not conteudo:
        return jsonify({'erro': 'Título e conteúdo são obrigatórios'}), 400
    
    db.editar_carta(id_carta, titulo, conteudo)
    return jsonify({'sucesso': True})

@app.route('/admin/remover_item/<tipo>/<int:id_item>', methods=['DELETE'])
def admin_remover_item(tipo, id_item):
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    if tipo == 'foto':
        db.remover_foto(id_item)
    elif tipo == 'musica':
        db.remover_musica(id_item)
    elif tipo == 'carta':
        db.remover_carta(id_item)
    elif tipo == 'mensagem':
        db.remover_mensagem(id_item)
    elif tipo == 'data':
        db.remover_data(id_item)
    
    return jsonify({'sucesso': True})

@app.route('/admin/adicionar_mensagem', methods=['POST'])
def admin_adicionar_mensagem():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    texto = request.form.get('texto')
    if not texto:
        return jsonify({'erro': 'Texto é obrigatório'}), 400
    
    db.adicionar_mensagem(texto)
    return jsonify({'sucesso': True})

@app.route('/admin/adicionar_data', methods=['POST'])
def admin_adicionar_data():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    titulo = request.form.get('titulo')
    data_evento = request.form.get('data_evento')
    
    if not titulo or not data_evento:
        return jsonify({'erro': 'Título e data são obrigatórios'}), 400
    
    db.adicionar_data(titulo, data_evento)
    return jsonify({'sucesso': True})

@app.route('/admin/configuracoes', methods=['POST'])
def admin_configuracoes():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
    novas_configs = {
        'titulo_site': request.form.get('titulo_site'),
        'cor_primaria': request.form.get('cor_primaria'),
        'cor_secundaria': request.form.get('cor_secundaria'),
        'fundo_particles': request.form.get('fundo_particles') == 'true'
    }
    
    db.atualizar_configuracoes(novas_configs)
    return jsonify({'sucesso': True})

if __name__ == '__main__':
    os.makedirs('static/uploads/fotos', exist_ok=True)
    os.makedirs('static/uploads/musicas', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
@app.route('/admin/salvar_config_surpresa', methods=['POST'])
def admin_salvar_config_surpresa():
    if not session.get('admin_logged'):
        return jsonify({'erro': 'Não autorizado'}), 401
    
