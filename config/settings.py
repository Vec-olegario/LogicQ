"""
=============================================================================
  CONFIGURAÇÕES DO SISTEMA (settings.py) — LogiQ
  Definição de constantes, chaves secretas e parâmetros da aplicação.
=============================================================================
"""
from typing import List, Dict

# Chave secreta para criptografia de sessão no Flask
SECRET_KEY: str = "galpao-logistico-2026-secreto"

# Título global do projeto
APP_TITLE: str = "LogiQ — Centro de Treinamento e Simulação Logística"

# Tópicos dos setores do Centro de Distribuição (CD)
TOPICOS: List[str] = [
    "Recebimento",
    "Estoque",
    "Picking",
    "Expedição",
]

# Quantidades de perguntas por modo de quiz
MODOS_QUIZ: Dict[str, int] = {
    "rapido": 5,
    "padrao": 15,
    "completo": 32,
    "topico": 8,
}
