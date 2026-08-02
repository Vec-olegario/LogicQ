# 📦 LogiQ — Centro de Treinamento e Simulação Logística

<p align="center">
  <b>Uma plataforma interativa, didática e modular para simulação operacional de Centros de Distribuição (CD) e capacitação em logística moderna.</b>
</p>

---

## 🚀 Visão Geral

O **LogiQ** é uma aplicação web desenvolvida em **Python (Flask)** com interface moderna em **HTML5, CSS3 Responsivo e JavaScript Puro**. O sistema simula o funcionamento de um Centro de Distribuição em suas quatro grandes etapas operacionais, integra painéis de indicadores (KPIs) dinâmicos com gráficos interativos e oferece um **Quiz Logístico Interativo** com 32 questões didáticas comentadas.

### ✨ Principais Funcionalidades

- **📥 Recebimento**: Visão detalhada do processo de agendamento de docas, conferência de NF-e, Cross-Docking e gestão de divergências e avarias.
- **🏢 Estoque**: Gráfico de ocupação em tempo real por rua (Rua A a H), endereçamento WMS, controle de giro de estoque, Curva ABC e métodos FIFO/LIFO.
- **🛒 Picking (Separação)**: Tabela de ranking interativa de produtividade dos separadores, taxa de erros, Pick-to-Light, Voice Picking e Zone Picking.
- **🚚 Expedição**: Monitoramento do status operacional das docas de saída, OTIF, romaneio de carga, unitização e roteirização.
- **📋 Situação do Turno (Check-in Operacional)**: Painel interativo com cartões independentes para registro do andamento diário de cada setor, com barra de progresso visual e botão de reinicialização de turno.
- **🧠 Quiz Logístico Interativo**:
  - **32 questões didáticas** divididas igualmente entre os 4 setores logísticos.
  - Modos de jogo selecionáveis: *Rápido (5 perguntas)*, *Padrão (15 perguntas)*, *Completo (32 perguntas)* ou *Por Setor (8 perguntas)*.
  - Sistema otimizado com embaralhamento aleatório de alternativas em tempo real e relatório analítico de acertos e tempo médio de resposta.

---

## 🏗️ Arquitetura Modular (Clean Code)

O projeto foi estruturado seguindo boas práticas de **Clean Code**, **Type Hints (Python 3)** e separação de responsabilidades. Dessa forma, é extremamente simples dar manutenção, adicionar funcionalidades e realizar testes em qualquer editor ou IDE (VS Code, PyCharm, Vim, etc.).

```
logiq/
├── config/
│   ├── __init__.py
│   └── settings.py          # Constantes globais (SECRET_KEY, TOPICOS, MODOS_QUIZ, APP_TITLE)
├── logic/
│   ├── __init__.py
│   ├── perguntas.py         # Banco de 32 perguntas do Quiz e métodos tipados de busca
│   ├── quiz_service.py      # Serviços de sessão do Quiz (embaralhamento leve e relatórios)
│   └── simuladores.py       # Geradores de KPIs simulados, ranking de separadores e docas
├── ui/
│   ├── __init__.py
│   └── charts.py            # Construtores otimizados de gráficos Plotly (JSON serializado)
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Utilitários de relógio, datas e cálculos estatísticos de tempo
├── templates/
│   ├── base.html            # Template base com navegação principal e rodapé
│   ├── inicio.html          # Página inicial de apresentação do centro logístico
│   ├── recebimento.html     # Setor de Recebimento
│   ├── estoque.html         # Setor de Estoque (com gráfico Plotly)
│   ├── picking.html         # Setor de Picking (com ranking de operadores)
│   ├── expedicao.html       # Setor de Expedição (com status das docas)
│   ├── situacao.html        # Painel integrador de situação operacional do turno
│   └── quiz.html            # Interface de Quiz (Seleção, Rodada de Jogo e Placar Final)
├── static/
│   └── style.css            # Folha de estilos completa com variáveis de tema e design cards
├── requirements.txt         # Dependências mínimas do projeto (flask, plotly)
└── app.py                   # Roteador principal e Handlers de Erro (404 / 500)
```

---

## 💻 Como Executar o Projeto Localmente

O projeto não requer instalação de bancos de dados complexos ou servidores externos; ele é executado de forma leve com o servidor web nativo do Flask.

### 1. Pré-requisitos
- **Python 3.9+** instalado no computador.

### 2. Passo a Passo

1. **Clone o repositório** para sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/logiq.git
   cd logiq
   ```

2. **(Opcional) Crie e ative um ambiente virtual**:
   - No Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - No Windows (PowerShell / Prompt):
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o servidor Flask**:
   ```bash
   python app.py
   ```

5. **Acesse no navegador**:
   Abra `http://localhost:5000` para explorar a plataforma.

---

## 🛠️ Guia para Desenvolvedores — Como Modificar e Expandir

### 1. Adicionar ou Editar Perguntas do Quiz
Todas as questões estão armazenadas de forma organizada em **`logic/perguntas.py`**. Para inserir uma nova pergunta, adicione um dicionário à lista `BANCO_PERGUNTAS` respeitando a estrutura:

```python
{
    "id": "R09",                  # Identificador único (R = Recebimento, E = Estoque, etc.)
    "topico": "Recebimento",      # Tópico correspondente a um dos 4 setores
    "dificuldade": "Média",       # "Fácil", "Médio" ou "Difícil"
    "pergunta": "Qual é a principal vantagem da conferência documental eletrônica?",
    "opcoes": [                   # Lista com exatamente 4 alternativas
        "Reduzir o tempo de parada do caminhão e evitar erros manuais.",
        "Aumentar o peso máximo permitido nas estantes.",
        "Dispensar o uso de coletores de dados.",
        "Eliminar a necessidade de notas fiscais."
    ],
    "correta": 0,                 # Índice da alternativa correta (0 = Primeira, 1 = Segunda...)
    "explicacao": "A conferência eletrônica compara automaticamente a NF-e com o pedido..."
}
```

### 2. Customizar os KPIs e Dados de Simulação
Se desejar alterar os valores simulados de produtividade, eficiência, ranking dos operadores de Picking ou o status das docas, edite o módulo **`logic/simuladores.py`**. Cada função (ex: `gerar_kpis_estoque`, `gerar_ranking_operadores`) é responsável por fornecer dicionários tipados e independentes.

### 3. Personalizar Cores e Estilos Visuais
A estilização da interface está centralizada em **`static/style.css`**. O topo do arquivo contém **variáveis CSS (`:root`)** onde é possível mudar rapidamente a paleta de cores primárias, secundárias, sombras de cards e raios de borda.

### 4. Modificar Configurações e Modos do Quiz
Para alterar as quantidades de perguntas em cada modo de jogo (*Rápido, Padrão, Completo*), ou o título global da aplicação, edite o arquivo **`config/settings.py`**.

---

## 🤝 Como Contribuir

1. Faça um **Fork** do repositório.
2. Crie uma **Branch** para sua melhoria (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas alterações com mensagens claras (`git commit -m "feat: Adiciona 10 novas perguntas de Estoque"`).
4. Envie o Push para a sua Branch (`git push origin feature/nova-funcionalidade`).
5. Abra um **Pull Request** para revisão.

---

## 📄 Licença

Este projeto é disponibilizado sob a licença de código aberto para fins didáticos, acadêmicos e de treinamento profissional em logística e supply chain.
