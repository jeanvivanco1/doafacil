# DoaFácil - Marketplace de Doações Locais

O **DoaFácil** é uma plataforma web completa para conectar doadores a pessoas que precisam de itens ou desejam adotar animais de estimação. Inspirado em plataformas como OLX, o foco aqui é a solidariedade e o impacto local.

## Funcionalidades Principais

- **Sistema de Usuários:** Cadastro de Doadores (Pessoas ou Instituições) e Adotantes/Receptores.
- **Doações:** Publicação de itens com categorias, subcategorias, fotos e detalhes específicos para pets.
- **Interação:** Sistema de favoritos, solicitações de doação e contato direto via WhatsApp.
- **Painéis:** Dashboards personalizados para gerenciar doações enviadas ou recebidas.
- **Design Moderno:** Interface responsiva, amigável e com suporte a Modo Escuro (Dark Mode).

## Tecnologias Utilizadas

- **Backend:** Python + Flask
- **Banco de Dados:** SQLite (com SQLAlchemy)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Segurança:** Hashing de senhas com Werkzeug

## Como Executar

### Pré-requisitos
- Python 3.x instalado.

### Passo a Passo (Windows)
1. Clique duas vezes no arquivo `INICIAR_SITE.bat`.
2. O script criará um ambiente virtual, instalará as dependências e iniciará o servidor.
3. O site abrirá automaticamente no seu navegador em `http://127.0.0.1:5000`.

### Passo a Passo (Linux/Mac)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Contas de Demonstração
- **Doador:** `doador@doafacil.com` / Senha: `123456`
- **Adotante:** `adotante@doafacil.com` / Senha: `123456`

---
*Desenvolvido para transformar vidas através de pequenos gestos.*
