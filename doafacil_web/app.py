import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from modelos import db, Usuario, Categoria, Subcategoria, Doacao, PetDetalhes, Favorito, Solicitacao
from banco import inicializar_banco

app = Flask(__name__)
app.config['SECRET_KEY'] = 'doafacil-secret-key'

# Caminhos absolutos para evitar erro de "unable to open database file"
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'doafacil.db')
upload_path = os.path.join(basedir, 'static', 'uploads')

# Criar pastas se não existirem
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
os.makedirs(upload_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['UPLOAD_FOLDER'] = upload_path
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.context_processor
def inject_categories():
    return dict(todas_categorias_global=Categoria.query.all())

# Inicializar banco e pastas
with app.app_context():
    inicializar_banco(app)

# --- ROTAS PRINCIPAIS ---

@app.route('/')
def index():
    recentes = Doacao.query.filter_by(status='Disponível').order_by(Doacao.data_criacao.desc()).limit(6).all()
    categorias = Categoria.query.all()
    return render_template('index.html', recentes=recentes, categorias=categorias)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/como-funciona')
def como_funciona():
    return render_template('como_funciona.html')

@app.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Email ou senha incorretos.')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        cidade = request.form.get('cidade')
        bairro = request.form.get('bairro')
        tipo_perfil = request.form.get('tipo_perfil')
        tipo_doador = request.form.get('tipo_doador')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado.')
            return redirect(url_for('cadastro'))
            
        novo_usuario = Usuario(
            nome=nome, email=email, senha=generate_password_hash(senha),
            telefone=telefone, cidade=cidade, bairro=bairro,
            tipo_perfil=tipo_perfil, tipo_doador=tipo_doador
        )
        db.session.add(novo_usuario)
        db.session.commit()
        login_user(novo_usuario)
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/categorias')
def categorias():
    todas_categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=todas_categorias)

@app.route('/categoria/<int:cat_id>')
def categoria_detalhe(cat_id):
    categoria = Categoria.query.get_or_404(cat_id)
    doacoes = Doacao.query.filter_by(categoria_id=cat_id, status='Disponível').all()
    return render_template('categoria.html', categoria=categoria, doacoes=doacoes)

@app.route('/doacao/<int:doacao_id>')
def detalhes_doacao(doacao_id):
    doacao = Doacao.query.get_or_404(doacao_id)
    favoritado = False
    if current_user.is_authenticated:
        favoritado = Favorito.query.filter_by(usuario_id=current_user.id, doacao_id=doacao_id).first() is not None
    return render_template('detalhes_doacao.html', doacao=doacao, favoritado=favoritado)

# --- ROTAS DE DOADOR ---

@app.route('/doar', methods=['GET', 'POST'])
@login_required
def nova_doacao():
    if current_user.tipo_perfil != 'Doador':
        flash('Apenas doadores podem criar anúncios.')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        categoria_id = request.form.get('categoria')
        subcategoria_id = request.form.get('subcategoria')
        descricao = request.form.get('descricao')
        cidade = request.form.get('cidade')
        bairro = request.form.get('bairro')
        whatsapp = request.form.get('whatsapp')
        condicao = request.form.get('condicao')
        
        imagem = request.files.get('imagem')
        filename = None
        if imagem:
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        doacao = Doacao(
            titulo=titulo, categoria_id=categoria_id, subcategoria_id=subcategoria_id,
            descricao=descricao, cidade=cidade, bairro=bairro, whatsapp=whatsapp,
            condicao=condicao, imagem=filename, doador_id=current_user.id
        )
        db.session.add(doacao)
        db.session.flush()
        
        # Se for Pet
        cat_pet = Categoria.query.filter_by(nome='Pets').first()
        if int(categoria_id) == cat_pet.id:
            pet = PetDetalhes(
                doacao_id=doacao.id,
                nome_pet=request.form.get('nome_pet'),
                especie=request.form.get('especie'),
                raca=request.form.get('raca'),
                sexo=request.form.get('sexo'),
                idade=request.form.get('idade'),
                porte=request.form.get('porte'),
                vacinado=request.form.get('vacinado'),
                castrado=request.form.get('castrado'),
                comportamento=request.form.get('comportamento'),
                requisitos_adocao=request.form.get('requisitos')
            )
            db.session.add(pet)
            
        db.session.commit()
        return redirect(url_for('painel_doador'))
        
    categorias = Categoria.query.all()
    return render_template('nova_doacao.html', categorias=categorias)

@app.route('/editar_doacao/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_doacao(id):
    doacao = Doacao.query.get_or_404(id)
    if doacao.doador_id != current_user.id:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        doacao.titulo = request.form.get('titulo')
        doacao.descricao = request.form.get('descricao')
        doacao.cidade = request.form.get('cidade')
        doacao.bairro = request.form.get('bairro')
        doacao.status = request.form.get('status')
        db.session.commit()
        return redirect(url_for('painel_doador'))
        
    return render_template('editar_doacao.html', doacao=doacao)

@app.route('/deletar_doacao/<int:id>')
@login_required
def deletar_doacao(id):
    doacao = Doacao.query.get_or_404(id)
    if doacao.doador_id == current_user.id:
        db.session.delete(doacao)
        db.session.commit()
    return redirect(url_for('painel_doador'))

@app.route('/painel_doador')
@login_required
def painel_doador():
    doacoes = Doacao.query.filter_by(doador_id=current_user.id).all()
    solicitacoes = Solicitacao.query.join(Doacao).filter(Doacao.doador_id == current_user.id).all()
    return render_template('painel_doador.html', doacoes=doacoes, solicitacoes=solicitacoes)

# --- ROTAS DE ADOTANTE / RECEPTOR ---

@app.route('/solicitar/<int:doacao_id>', methods=['GET', 'POST'])
@login_required
def solicitar_doacao(doacao_id):
    doacao = Doacao.query.get_or_404(doacao_id)
    if request.method == 'POST':
        solicitacao = Solicitacao(
            doacao_id=doacao_id,
            solicitante_id=current_user.id,
            mensagem=request.form.get('mensagem'),
            motivo=request.form.get('motivo'),
            telefone_contato=request.form.get('telefone')
        )
        db.session.add(solicitacao)
        db.session.commit()
        flash('Solicitação enviada com sucesso!')
        return redirect(url_for('minhas_solicitacoes'))
    return render_template('solicitar_doacao.html', doacao=doacao)

@app.route('/minhas_solicitacoes')
@login_required
def minhas_solicitacoes():
    solicitacoes = Solicitacao.query.filter_by(solicitante_id=current_user.id).all()
    return render_template('minhas_solicitacoes.html', solicitacoes=solicitacoes)

@app.route('/painel_adotante')
@login_required
def painel_adotante():
    favoritos = Favorito.query.filter_by(usuario_id=current_user.id).all()
    solicitacoes = Solicitacao.query.filter_by(solicitante_id=current_user.id).all()
    return render_template('painel_adotante.html', favoritos=favoritos, solicitacoes=solicitacoes)

@app.route('/painel_admin')
@login_required
def painel_admin():
    if current_user.tipo_perfil != 'Admin':
        flash('Acesso restrito a administradores.')
        return redirect(url_for('index'))
    
    total_usuarios = Usuario.query.count()
    total_doacoes = Doacao.query.count()
    usuarios = Usuario.query.all()
    doacoes = Doacao.query.all()
    
    return render_template('painel_admin.html', 
                           total_usuarios=total_usuarios, 
                           total_doacoes=total_doacoes,
                           usuarios=usuarios,
                           doacoes=doacoes)

@app.route('/favoritar/<int:doacao_id>')
@login_required
def favoritar(doacao_id):
    fav = Favorito.query.filter_by(usuario_id=current_user.id, doacao_id=doacao_id).first()
    if fav:
        db.session.delete(fav)
    else:
        novo_fav = Favorito(usuario_id=current_user.id, doacao_id=doacao_id)
        db.session.add(novo_fav)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/favoritos')
@login_required
def favoritos():
    favs = Favorito.query.filter_by(usuario_id=current_user.id).all()
    return render_template('favoritos.html', favoritos=favs)

# --- BUSCA E FILTROS ---

@app.route('/busca')
def busca():
    q = request.args.get('q', '')
    cat_id = request.args.get('categoria')
    sub_id = request.args.get('subcategoria')
    cidade = request.args.get('cidade')
    
    query = Doacao.query
    if q:
        query = query.filter(Doacao.titulo.contains(q) | Doacao.descricao.contains(q))
    if cat_id:
        query = query.filter(Doacao.categoria_id == cat_id)
    if sub_id:
        query = query.filter(Doacao.subcategoria_id == sub_id)
    if cidade:
        query = query.filter(Doacao.cidade.contains(cidade))
        
    resultados = query.all()
    categoria = Categoria.query.get(cat_id) if cat_id else None
    return render_template('categoria.html', doacoes=resultados, busca=True, q=q, categoria=categoria)

@app.route('/responder_solicitacao/<int:id>/<string:acao>')
@login_required
def responder_solicitacao(id, acao):
    sol = Solicitacao.query.get_or_404(id)
    if sol.doacao.doador_id == current_user.id:
        sol.status = 'Aceito' if acao == 'aceitar' else 'Recusado'
        db.session.commit()
    return redirect(url_for('painel_doador'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Binds to 127.0.0.1 for local access
    # Debug mode enabled to see exact error in browser
    app.run(host='127.0.0.1', port=5000, debug=True)
