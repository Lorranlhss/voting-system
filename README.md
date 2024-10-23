# Sistema de Votação

Este é um sistema de votação desenvolvido em Python com Flask, que permite aos usuários se registrarem, fazerem login, votarem em um dos 39 candidatos e verem os resultados da votação em tempo real. O sistema garante que cada usuário só possa votar uma vez.

## Funcionalidades

- **Registro de Usuário**: Os usuários podem se registrar com um nome de usuário e senha.
- **Login**: Sistema de login para que apenas usuários registrados possam votar.
- **Votação**: Permite que os usuários escolham um candidato entre 39 opções organizadas em uma tabela.
- **Restrição de Voto**: Cada usuário pode votar apenas uma vez.
- **Resultados em Tempo Real**: A tela de resultados é atualizada automaticamente a cada 5 segundos, mostrando os 5 candidatos mais votados.

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS, JavaScript (AJAX)
- **Banco de Dados**: SQLite
- **Estilo**: CSS para estilização da interface
- **Atualização em Tempo Real**: AJAX para atualizar os resultados automaticamente

## Como Rodar o Projeto Localmente

### Pré-requisitos

- **Python 3.x**
- **Flask**
- **SQLite3** (embutido no Python)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```

Acesse o diretório do projeto:

  ```bash Copiar código
  cd seu-repositorio
  ```
Crie e ative um ambiente virtual (opcional, mas recomendado):

  ```bash Copiar código
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate  # Windows
  ```
Instale as dependências necessárias:

```bash Copiar código
pip install -r requirements.txt
```
Configure o ambiente Flask criando um arquivo .flaskenv:

```makefile Copiar código
FLASK_APP=app.py
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
```
Crie o banco de dados:

O banco de dados SQLite será criado automaticamente ao rodar o projeto pela primeira vez, mas se desejar, pode executar manualmente os scripts SQL para criar as tabelas necessárias.
Execute o projeto:

```bash Copiar código
flask run
```
Abra seu navegador e acesse http://127.0.0.1:5000.

Estrutura do Projeto
```bash
Copiar código
├── app.py              # Código principal da aplicação Flask
├── database.db         # Banco de dados SQLite
├── templates/          # Arquivos HTML
│   ├── base.html       # Template base
│   ├── login.html      # Página de login
│   ├── register.html   # Página de registro
│   ├── votacao.html    # Página de votação
│   ├── resultado.html  # Página de resultados
├── static/             # Arquivos estáticos (CSS, JS)
│   ├── styles.css      # Arquivo de estilo CSS
│   ├── script.js       # Lógica de atualização em tempo real (AJAX)
└── README.md           # Este arquivo
```
# Contribuindo

- Faça um fork do projeto.
- Crie uma branch para sua feature (git checkout -b feature/nova-feature).
- Commit suas mudanças (git commit -am 'Adiciona nova feature').
- Envie para a branch principal (git push origin feature/nova-feature).
- Crie um novo Pull Request.

Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.




