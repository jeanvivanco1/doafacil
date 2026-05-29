from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    tipo_perfil = db.Column(db.String(20), nullable=False) # 'Doador', 'Adotante' ou 'Admin'
    tipo_doador = db.Column(db.String(20), nullable=True) # 'Pessoa Física' ou 'Instituição'
    imagem_perfil = db.Column(db.String(200), nullable=True)
    
    doacoes = db.relationship('Doacao', backref='doador', lazy=True)
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True)
    solicitacoes = db.relationship('Solicitacao', backref='solicitante', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    subcategorias = db.relationship('Subcategoria', backref='categoria', lazy=True)

class Subcategoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

class Doacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategoria.id'), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    condicao = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='Disponível') # 'Disponível', 'Reservado', 'Doado'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    doador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Relacionamentos para acessar os objetos categoria e subcategoria
    categoria = db.relationship('Categoria', backref=db.backref('doacoes_list', lazy=True))
    subcategoria = db.relationship('Subcategoria', backref=db.backref('doacoes_list', lazy=True))
    
    pet_detalhes = db.relationship('PetDetalhes', backref='doacao', uselist=False, cascade="all, delete-orphan")
    solicitacoes = db.relationship('Solicitacao', backref='doacao', lazy=True, cascade="all, delete-orphan")
    favoritados = db.relationship('Favorito', backref='doacao', lazy=True, cascade="all, delete-orphan")

class PetDetalhes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doacao_id = db.Column(db.Integer, db.ForeignKey('doacao.id'), nullable=False)
    nome_pet = db.Column(db.String(50))
    especie = db.Column(db.String(50))
    raca = db.Column(db.String(50))
    sexo = db.Column(db.String(10))
    idade = db.Column(db.String(20))
    porte = db.Column(db.String(20))
    vacinado = db.Column(db.String(5)) # 'Sim' ou 'Não'
    castrado = db.Column(db.String(5)) # 'Sim' ou 'Não'
    comportamento = db.Column(db.Text)
    requisitos_adocao = db.Column(db.Text)

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    doacao_id = db.Column(db.Integer, db.ForeignKey('doacao.id'), nullable=False)

class Solicitacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doacao_id = db.Column(db.Integer, db.ForeignKey('doacao.id'), nullable=False)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    telefone_contato = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pendente') # 'Pendente', 'Aceito', 'Recusado'
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
