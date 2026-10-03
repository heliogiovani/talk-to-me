Talk To Me — Flashcards Inteligentes para Aprendizado de InglêsUma aplicação web moderna desenvolvida em Python (Flask) e MySQL, baseada na arquitetura MVC (Model-View-Controller). O projeto combina cartões interativos em 3D, transcrição fonética (IPA), marcação visual de cadência e ritmo de fala, sintetizador de áudio automático e um avaliador estrito de pronúncia via inteligência artificial com reconhecimento de fala. Funcionalidades Principais: Cartões Interativos 3D (Flip Cards): Interface limpa e responsiva que gira ao toque/clique em qualquer área do cartão para alternar entre a frase em inglês e a tradução natural. Áudio Automático (Text-to-Speech): Leitura de voz masculina natural acionada automaticamente assim que o cartão é carregado ou sorteado, com controle de velocidade ($0.75\times$, $1.0\times$, $1.25\times$). Fonética Internacional (IPA): Transcrição fonética completa para apoio à correta articulação sonora de cada frase. Análise de Cadência e Ritmo: Separação visual de content words (palavras fortes/enfatizadas) e grammar words (palavras fracas/conectivos), ensinando a musicalidade do idioma falado.🎙️ Avaliador Rigoroso de Pronúncia com IA: Integração direta com a API de reconhecimento de fala do navegador e algoritmo de conferência rigorosa no backend, exigindo pelo menos $90\%$ de fidelidade palavra a palavra.🇧🇷 Traduções Idiomáticas e Naturais: Expressões traduzidas pelo sentido prático e cultural do dia a dia, evitando traduções literais mecânicas. Sistema de Repetição Espaçada (SRS): Agendamento inteligente de revisões baseado na facilidade do usuário:Muito Difícil: Repete em 15 minutos.Difícil: Repete em 1 dia.Fácil: Repete em 4 dias.🎲 Seleção Aleatória Inteligente: Distribuição randômica de frases priorizando os itens pendentes de revisão. Arquitetura do Projeto (MVC)O código foi construído seguindo rigorosamente o padrão Model-View-Controller:APP ENGLISH/


├── app/
│   ├── controllers/
│   │   └── card_controller.py      # Lógica de rotas, SRS e verificação de pronúncia
│   ├── models/
│   │   └── card.py                 # Modelo SQLAlchemy mapeado para a tabela MySQL
│   ├── services/
│   │   ├── daily_fetcher.py        # Alimentador e sincronizador diário de cards
│   │   └── phrase_service.py       # Extração de fonética IPA, cadência e tradução
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Estilos visuais e animação 3D do flip card
│   │   └── js/
│   │       └── app.js              # Áudio automático, microfone e chamadas assíncronas
│   ├── templates/
│   │   └── index.html              # Interface do usuário (View)
│   ├── __init__.py                 # Fábrica da aplicação Flask e registros
│   └── config.py                   # Configurações de conexão e codificação de senha
│
├── .env.example                    # Modelo para variáveis de ambiente locais
├── .gitignore                      # Proteção de credenciais e arquivos pesados
├── requirements.txt                # Dependências do ecossistema Python
└── run.py                          # Ponto de entrada para execução do servidor


Tecnologias UtilizadasBackend: Python, Flask, Flask-SQLAlchemy, PyMySQL.Banco de Dados: MySQL.Processamento de Linguagem: eng-to-ipa, algoritmos de correspondência de sequência (difflib).Frontend: HTML5 semântico, CSS3 (3D Transforms), JavaScript Vanilla (Web Speech API).🛠️ Como Executar Localmente1. Pré-requisitosPython instalado (versão 3.10 ou superior recomendada).MySQL Server ativo e rodando.Navegador Google Chrome ou Microsoft Edge (para suporte completo à Web Speech API).2. Clonar o repositóriogit clone https://github.com/heliogiovani/talk-to-me.git
cd talk-to-me
3. Criar e ativar o ambiente virtual# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
4. Instalar as dependênciaspip install -r requirements.txt
5. Configurar o banco de dadosCrie o banco de dados no MySQL:CREATE DATABASE english_cards_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Crie o arquivo .env na raiz do projeto com suas credenciais:MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=english_cards_db
SECRET_KEY=sua_chave_secreta
6. Executar o servidorpython run.py
Acesse no navegador: http://127.0.0.1:5000
Licença: Este projeto é desenvolvido para fins educacionais e práticos no aprendizado de idiomas. Não pode ser copiado (no todo ou em partes) sem a permissão do desenvolvedor do projeto.
