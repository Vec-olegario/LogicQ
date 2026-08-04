"""
=============================================================================
  CONFIGURAÇÕES DO SISTEMA (settings.py) — LogiQ
  Definição de constantes, chaves secretas e parâmetros da aplicação.
=============================================================================
"""
import os
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

# Chave de API externa opcional (via variável de ambiente) para o assistente
API_KEY: str = os.getenv("LOGIQ_API_KEY", "")

# Configuração do Modelo e Limites de Desempenho
PREFERED_IA_MODEL: str = os.getenv("LOGIQ_IA_MODEL", "gemini-2.0-flash")
MAX_OUTPUT_TOKENS: int = 1500
TIMEOUT_IA_SEGUNDOS: int = 4
