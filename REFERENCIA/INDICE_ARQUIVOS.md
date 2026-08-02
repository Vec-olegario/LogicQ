# 📑 ÍNDICE DE ARQUIVOS — PROJETO LOGIQ

> **Versão 2.0 (Modular)** · Agosto 2026  
> Referência de arquivos da plataforma LogiQ — Centro de Treinamento e Simulação Logística

---

## 📂 Estrutura de Pastas e Componentes

```
LOGIQ/
│
├── README.md                           ← Documentação principal do projeto
├── requirements.txt                    ← Dependências mínimas do projeto (flask, plotly)
├── app.py                              ← Roteador Flask principal e Handlers de Erro
│
├── config/                             ← Configurações e Diretrizes Globais
│   ├── __init__.py
│   └── settings.py                     ← Chaves secretas, tópicos, títulos e modos do Quiz
│
├── logic/                              ← Camada de Regras de Negócio e Domínio Logístico
│   ├── __init__.py
│   ├── perguntas.py                    ← Banco de 32 questões pedagógicas sobre o CD
│   ├── quiz_service.py                 # Lógica do Quiz (permutações leves para sessão e score)
│   └── simuladores.py                  # Simulação de KPIs, docas e ranking operacional
│
├── ui/                                 ← Geração Visual e Componentes Gráficos
│   ├── __init__.py
│   └── charts.py                       ← Gráficos Plotly em JSON com cache (área e ocupação)
│
├── utils/                              ← Utilitários Gerais e Formatação
│   ├── __init__.py
│   └── helpers.py                      # Funções de data, relógio e cálculo de tempo decorrido
│
├── templates/                          ← Templates HTML5 Responsivos (Jinja2)
│   ├── base.html                       ← Estrutura principal, navbar e rodapé
│   ├── inicio.html                     ← Página inicial de apresentação do galpão
│   ├── recebimento.html                ← Setor de Recebimento
│   ├── estoque.html                    ← Setor de Estoque (com gráfico de ruas)
│   ├── picking.html                    ← Setor de Picking (com ranking de operadores)
│   ├── expedicao.html                  ← Setor de Expedição (com status das 6 docas)
│   ├── situacao.html                   ← Check-in operacional do turno e barra de progresso
│   └── quiz.html                       ← Interface do Quiz (Modos, Jogo e Relatório Final)
│
├── static/                             ← Recursos Estáticos
│   └── style.css                       ← Design moderno em cartões com variáveis CSS
│
├── GUIAS_E_TEMPLATES/                  ← Guias Didáticos para o Desenvolvedor
│   ├── GUIA_ADICIONAR_PERGUNTAS_QUIZ.md    ← Guia completo para expandir perguntas do Quiz
│   ├── IDEIAS_FUNCIONALIDADES_EXTRAS.md    ← Roadmap de ideias de melhorias futuras
│   └── RESUMO_EXECUTIVO_GALPAO_X.txt       ← Resumo conceitual dos setores
│
└── REFERENCIA/                         ← Documentação de Referência
    └── INDICE_ARQUIVOS.md              ← Este índice organizado
```

---

## 📋 Resumo de Cada Camada

| Pacote / Módulo | Responsabilidade |
|---|---|
| **`app.py`** | Ponto de entrada leve da aplicação Flask; define as rotas HTTP e captura erros `404` e `500`. |
| **`config/settings.py`** | Armazena configurações globais como `SECRET_KEY`, lista de `TOPICOS` e parâmetros dos modos de jogo. |
| **`logic/perguntas.py`** | Contém a estrutura `BANCO_PERGUNTAS` (32 perguntas comentadas) e funções tipadas de busca por índice e tópico. |
| **`logic/quiz_service.py`** | Resolve o gerenciamento de rodadas de Quiz, evitando estouros de cookie de 4 KB através do armazenamento de ordens e permutações. |
| **`logic/simuladores.py`** | Cria em tempo real os relatórios simulados para o ranking de picking, status das docas e KPIs por setor. |
| **`ui/charts.py`** | Constrói gráficos dinâmicos de área e barras em Plotly JSON utilizando cache de memória para o layout. |
| **`utils/helpers.py`** | Fornece horários, datas e cálculo de média de tempo por pergunta com tratamento defensivo de erros. |
