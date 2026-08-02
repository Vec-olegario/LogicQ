# Diretrizes de Arquitetura, Clean Code e Documentação Open Source — LogiQ

## 1. Arquitetura Modular em Aplicações Web (Flask)
- **Não criar código monolítico**: Manter o arquivo `app.py` enxuto e dedicado exclusivamente a roteamento HTTP, controllers de requisições e tratamento de erros.
- **Estruturação por pacotes com responsabilidades únicas**:
  - `config/`: Constantes globais, configurações da aplicação e chaves de segurança.
  - `logic/`: Lógica puramente funcional e regras de negócio (banco de questões, cálculo de pontuação, geradores de simulação operacional).
  - `ui/`: Construtores de componentes visuais, gráficos Plotly otimizados e utilitários visuais.
  - `utils/`: Utilitários gerais (data, hora, formatações de relógio e medições temporais).

## 2. Padrões de Tipagem e Documentação (Python 3)
- **Type Hints obrigatórios**: Todas as funções, argumentos, retornos e constantes devem conter anotações estáticas de tipo (`from typing import List, Dict, Any, Optional, Tuple`, etc.).
- **Docstrings em Português**: Cada módulo (`.py`) e função pública deve conter docstring completa no formato padrão (descrição, `Args:` e `Returns:`).

## 3. Tratamento de Erros e Segurança no Flask
- **Handlers de Erro Globais**: Manter sempre implementados `@app.errorhandler(404)` e `@app.errorhandler(500)` para emitir mensagens amigáveis em flash e redirecionar o usuário sem exibir stack trace.
- **Limite de Cookie de Sessão (4 KB)**: No Flask (onde a sessão é salva em cookies client-side), nunca armazenar textos extensos, dicionários de perguntas completos ou grandes massas de dados. Salvar na sessão apenas IDs, índices e permutações curtas (`[0..3]`).
- **Cache Visual**: Empregar `@lru_cache` para layouts base ou estilos estáticos recorrentes na geração de gráficos.

## 4. Padrões para o GitHub e Documentação Open Source (Despessoalização)
- **Zero Citações a IDE ou IA**: Nunca incluir em arquivos de documentação (`README.md`, guias, comentários no código ou docstrings) menções a modelos de IA específicos ("Antigraviti", "Gemini", "ChatGPT"), IDEs específicas ou instruções exclusivas de prompt/chat. A documentação deve ser 100% universal.
- **Estrutura Obrigatória do `README.md`**:
  - Apresentação visual clara e explicação do propósito do sistema;
  - Diagrama da árvore de pastas e explicação da arquitetura modular;
  - Guia de execução local via linha de comando (compatível com Linux, Windows e macOS);
  - **Guia do Desenvolvedor** detalhando onde e como customizar questões do Quiz, parâmetros, simulações e estilos.
- **Limpeza do Repositório**: Excluir pastas de rascunhos/briefings de IA antes da publicação e remover do arquivo `requirements.txt` qualquer dependência que não esteja em uso real na aplicação.
