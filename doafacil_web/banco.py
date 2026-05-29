from flask import Flask
from modelos import db, Usuario, Categoria, Subcategoria, Doacao, PetDetalhes
from werkzeug.security import generate_password_hash
import os

def inicializar_banco(app):
    with app.app_context():
        db.create_all()
        
        # Seed Categorias e Subcategorias
        if not Categoria.query.first():
            dados_categorias = {
                "Pets": ["Animais", "Ração", "Acessórios"],
                "Alimentos": ["Cestas Básicas", "Outros Alimentos"],
                "Vestuário": ["Roupas", "Calçados"],
                "Casa": ["Móveis", "Utensílios"],
                "Higiene": ["Pessoal", "Limpeza"],
                "Outros": ["Eletrônicos", "Material Escolar", "Diversos"]
            }
            
            for cat_nome, subcats in dados_categorias.items():
                categoria = Categoria(nome=cat_nome)
                db.session.add(categoria)
                db.session.flush()
                for sub_nome in subcats:
                    subcategoria = Subcategoria(nome=sub_nome, categoria_id=categoria.id)
                    db.session.add(subcategoria)
            
            # Contas de demonstração
            doador = Usuario(
                nome="Doador Exemplo",
                email="doador@doafacil.com",
                senha=generate_password_hash("123456"),
                telefone="11999999999",
                cidade="São Paulo",
                bairro="Centro",
                tipo_perfil="Doador",
                tipo_doador="Pessoa Física"
            )
            adotante = Usuario(
                nome="Adotante Exemplo",
                email="adotante@email.com",
                senha=generate_password_hash("123456"),
                telefone="11988888888",
                cidade="São Paulo",
                bairro="Pinheiros",
                tipo_perfil="Adotante"
            )
            admin = Usuario(
                nome="Administrador",
                email="admin@doafacil.com",
                senha=generate_password_hash("admin123"),
                telefone="11977777777",
                cidade="São Paulo",
                bairro="Centro",
                tipo_perfil="Admin"
            )
            db.session.add(doador)
            db.session.add(adotante)
            db.session.add(admin)
            db.session.flush()

            # Seed Doações (10 exemplos)
            doacoes_exemplo = [
                {"titulo": "Cesta Básica Completa", "cat": "Alimentos", "sub": "Cestas Básicas", "desc": "Cesta com arroz, feijão, óleo e macarrão.", "img": "https://images.unsplash.com/photo-1626071466175-79691666835a?w=500"},
                {"titulo": "Agasalho Masculino G", "cat": "Vestuário", "sub": "Roupas", "desc": "Blusa de lã em ótimo estado.", "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"},
                {"titulo": "Tênis Infantil Tam 28", "cat": "Vestuário", "sub": "Calçados", "desc": "Tênis azul, pouco usado.", "img": "https://images.unsplash.com/photo-1514989940723-e8e51635b782?w=500"},
                {"titulo": "Mesa de Jantar 4 Cadeiras", "cat": "Casa", "sub": "Móveis", "desc": "Mesa de madeira, marcas de uso leves.", "img": "https://images.unsplash.com/photo-1577140917170-285929fb55b7?w=500"},
                {"titulo": "Pacote de Fraldas G", "cat": "Higiene", "sub": "Pessoal", "desc": "Pacote fechado com 40 unidades.", "img": "https://images.unsplash.com/photo-1621343018855-1ccad252c735?w=500"},
                {"titulo": "Mochila Escolar", "cat": "Outros", "sub": "Material Escolar", "desc": "Mochila resistente para crianças.", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"},
                {"titulo": "Televisão 32 polegadas", "cat": "Outros", "sub": "Eletrônicos", "desc": "TV funcionando perfeitamente, sem controle.", "img": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500"},
                {"titulo": "Cadeira de Rodas", "cat": "Outros", "sub": "Diversos", "desc": "Cadeira de rodas manual, bom estado.", "img": "https://images.unsplash.com/photo-1597075095350-579e5177189d?w=500"},
                {"titulo": "Leite Integral 12L", "cat": "Alimentos", "sub": "Outros Alimentos", "desc": "Caixa fechada de leite integral.", "img": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500"},
                {"titulo": "Sofá 3 Lugares", "cat": "Casa", "sub": "Móveis", "desc": "Sofá cinza, confortável.", "img": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500"}
            ]

            for d in doacoes_exemplo:
                cat = Categoria.query.filter_by(nome=d['cat']).first()
                sub = Subcategoria.query.filter_by(nome=d['sub'], categoria_id=cat.id).first()
                nova_doacao = Doacao(
                    titulo=d['titulo'],
                    descricao=d['desc'],
                    categoria_id=cat.id,
                    subcategoria_id=sub.id,
                    cidade="São Paulo",
                    bairro="Centro",
                    whatsapp="11999999999",
                    condicao="Usado",
                    status="Disponível",
                    doador_id=doador.id,
                    imagem=d['img']
                )
                db.session.add(nova_doacao)

            # Seed Pets (4 exemplos)
            pets_exemplo = [
                {"nome": "Rex", "especie": "Cachorro", "raca": "Vira-lata", "sexo": "Macho", "idade": "2 anos", "porte": "Médio", "img": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=500"},
                {"nome": "Luna", "especie": "Gato", "raca": "Siamês", "sexo": "Fêmea", "idade": "1 ano", "porte": "Pequeno", "img": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=500"},
                {"nome": "Thor", "especie": "Cachorro", "raca": "Golden", "sexo": "Macho", "idade": "4 anos", "porte": "Grande", "img": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=500"},
                {"nome": "Mel", "especie": "Gato", "raca": "Persa", "sexo": "Fêmea", "idade": "3 anos", "porte": "Pequeno", "img": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500"}
            ]

            cat_pets = Categoria.query.filter_by(nome="Pets").first()
            sub_animais = Subcategoria.query.filter_by(nome="Animais", categoria_id=cat_pets.id).first()

            for p in pets_exemplo:
                sub = sub_animais
                doacao_pet = Doacao(
                    titulo=f"Adoção: {p['nome']}",
                    descricao=f"Lindo {p['especie']} para adoção responsável.",
                    categoria_id=cat_pets.id,
                    subcategoria_id=sub.id,
                    cidade="São Paulo",
                    bairro="Centro",
                    whatsapp="11999999999",
                    status="Disponível",
                    doador_id=doador.id,
                    imagem=p['img']
                )
                db.session.add(doacao_pet)
                db.session.flush()
                
                detalhes = PetDetalhes(
                    doacao_id=doacao_pet.id,
                    nome_pet=p['nome'],
                    especie=p['especie'],
                    raca=p['raca'],
                    sexo=p['sexo'],
                    idade=p['idade'],
                    porte=p['porte'],
                    vacinado="Sim",
                    castrado="Sim",
                    comportamento="Dócil e brincalhão.",
                    requisitos_adocao="Apartamento telado ou casa segura."
                )
                db.session.add(detalhes)

            db.session.commit()
            print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    # Script para rodar isoladamente se necessário
    from flask import Flask
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'doafacil.db')
    db.init_app(app)
    inicializar_banco(app)
