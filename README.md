# Talk To Me — Flashcards Inteligentes para Aprendizado de Inglês

Aplicação web desenvolvida em Python (Flask) e MySQL, fundamentada no padrão de arquitetura MVC (Model-View-Controller).

O sistema integra cartões interativos tridimensionais, transcrição fonética internacional (IPA), segmentação visual de cadência rítmica da fala, síntese vocal masculina automatizada e motor de validação rigorosa de pronúncia por inteligência artificial via reconhecimento de voz no navegador.

---

## Funcionalidades do Sistema

- **Cartões Interativos 3D (Flip Cards):** Interface construída com rotação tridimensional ao clique em qualquer área do cartão para alternar entre a frase em língua inglesa e a sua tradução equivalente em português.
- **Síntese Vocal Automatizada (Text-to-Speech):** Reprodução automática de voz masculina calibrada assim que o cartão é carregado ou alternado, com alternância de velocidade ajustável (0.75x, 1.0x, 1.25x).
- **Transcrição Fonética Internacional (IPA):** Mapeamento fonético completo de cada sentença para suporte à correta articulação sonora dos fonemas.
- **Análise de Cadência e Ritmo:** Diferenciação visual entre palavras de conteúdo (content words - tônicas) e palavras gramaticais (grammar words - átonas), auxiliando na compreensão da musicalidade e do ritmo do inglês falado.
- **Validador Estrito de Pronúncia:** Captura de áudio nativa via Web Speech API e algoritmo de conferência no backend, exigindo o índice mínimo de 90% de correspondência estrita e presença de todas as palavras enunciadas.
- **Traduções Idiomáticas Equivalentes:** Foco no significado semântico e cultural do quotidiano, substituindo traduções literais mecânicas por expressões reais do dia a dia.
- **Algoritmo de Repetição Espaçada (SRS):** Gestão de intervalos de retenção de memória parametrizada:
  - Muito Difícil: Retorno em 15 minutos.
  - Difícil: Retorno em 1 dia.
  - Fácil: Retorno em 4 dias.
- **Distribuição Aleatória:** Sorteio randômico dos cartões cadastrados, priorizando itens com agendamento de revisão vencido.

---

## Arquitetura de Software (MVC)

A disposição estrutural do projeto obedece à separação de responsabilidades do padrão Model-View-Controller:

```text
APP ENGLISH/
├── app/
│   ├── controllers/
│   │   └── card_controller.py     # Gestão de rotas da API, SRS e verificação fonética
│   ├── models/
│   │   └── card.py                # Entidade de dados mapeada via SQLAlchemy para o MySQL
│   ├── services/
│   │   ├── daily_fetcher.py       # Serviço de carga e gestão de frases diárias
│   │   └── phrase_service.py      # Extração de fonética IPA, cadência e tradução
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Folha de estilos e transformações 3D
│   │   └── js/
│   │       └── app.js             # Lógica de interface, Web Speech API e requisições assíncronas
│   ├── templates/
│   │   └── index.html             # Camada de apresentação (View)
│   ├── __init__.py                # Inicialização e fábrica da aplicação Flask
│   └── config.py                  # Parâmetros de infraestrutura e variáveis de ambiente
├── .env.example                   # Arquivo de referência para variáveis locais
├── .gitignore                     # Diretivas de exclusão do controle de versão
├── popular_cards.py               # Script de carga inicial e saneamento da base de dados
├── requirements.txt               # Declaração explícita de dependências do Python
└── run.py                         # Ponto de entrada do servidor de desenvolvimento
```

---

## Tecnologias e Bibliotecas

- **Linguagem:** Python 3.10+
- **Framework Web:** Flask
- **Camada de Persistência:** SQLAlchemy e PyMySQL sobre base de dados MySQL
- **Processamento de Linguagem Natural:** eng-to-ipa e requests
- **Interface e Navegador:** HTML5, CSS3 (CSS 3D Transforms) e JavaScript ECMAScript 6+ (Web Speech API)

---

## Instalação e Execução

### 1. Clonar o repositório
```bash
git clone [https://github.com/heliogiovani/talk-to-me.git](https://github.com/heliogiovani/talk-to-me.git)
cd talk-to-me
```

### 2. Configurar o ambiente virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar pacotes necessários
```bash
pip install -r requirements.txt
```

### 4. Definir variáveis de ambiente
Crie um arquivo `.env` na raiz do diretório com base em `.env.example`:
```ini
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=english_cards_db
SECRET_KEY=sua_chave_secreta
```

### 5. Executar carga inicial no banco
```bash
python popular_cards.py
```

### 6. Inicializar o servidor
```bash
python run.py
```

Acesso via navegador no endereço: `http://127.0.0.1:5000`

---

## Licença

Projeto distribuído sob a Licença MIT. Para detalhes, consulte o arquivo LICENSE.
