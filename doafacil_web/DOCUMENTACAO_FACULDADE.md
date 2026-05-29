# Relatório Técnico do Projeto: DoaFácil

Este documento detalha como o sistema **DoaFácil** atende aos requisitos acadêmicos solicitados.

## 1. Modelagem de Dados e Banco de Dados
O sistema utiliza um banco de dados relacional **SQLite**, garantindo a persistência das informações.
- **Tabelas:** Usuários, Categorias, Subcategorias, Doações, Detalhes de Pets, Favoritos e Solicitações.
- **Relacionamentos:** Uso de chaves estrangeiras (Foreign Keys) e relacionamentos 1:1 e 1:N.
- **Regras de Negócio:** Doações só podem ser editadas pelo dono; solicitações dependem de um perfil de Adotante.

## 2. Perfis de Usuário (Requisito: Admin e Usuário Comum)
O sistema implementa três níveis de acesso:
- **Administrador:** Acesso ao `Painel Admin`, visão geral de todos os usuários e doações. (Login: `admin@doafacil.com` / Senha: `admin123`).
- **Doador (Usuário Comum):** Pode publicar, editar e gerenciar solicitações de seus itens.
- **Adotante (Usuário Comum):** Pode buscar, favoritar e solicitar itens.

## 3. Tecnologias e Integração (Requisito: Stack Técnica)
- **Linguagem:** Python 3.
- **Framework Back-end:** Flask (Integração completa via rotas e Jinja2).
- **Front-end:** HTML5, CSS3 (com Dark Mode) e JavaScript Vanilla.
- **ORM:** SQLAlchemy para abstração do banco de dados e Orientação a Objetos.

## 4. Interface UX/UI e Validação
- **Interface:** Web responsiva, intuitiva e centrada no usuário (Design Thinking).
- **Validação:** Implementada via formulários HTML5 (required, email type) e validações no back-end (Flask-Login).
- **Usabilidade:** Menu dropdown para categorias, cards com efeito hover e feedbacks visuais (badges de status).

## 5. Engenharia de Software e POO
- **Organização:** Código dividido em `app.py` (Controller), `modelos.py` (Model) e `templates/` (View).
- **POO:** Uso intensivo de classes para representar as entidades do banco de dados, com encapsulamento de métodos e atributos.

## 6. Gestão Ágil (Simulação Trello/Jira)
O desenvolvimento seguiu o seguinte fluxo:
- **Sprint 1:** Modelagem do banco e Autenticação.
- **Sprint 2:** Fluxo de Doação e Categorias.
- **Sprint 3:** Dashboards e Sistema de Solicitação.
- **Sprint 4:** Refinamento de UI/UX e Perfil Admin.

---

