"""
=============================================================================
  Pacote de Lógica de Negócio — LogiQ
  Armazena os domínios da aplicação (Quiz, Perguntas e Simulação Operacional).
=============================================================================
"""
from .perguntas import (
    BANCO_PERGUNTAS,
    get_pergunta_by_index,
    get_perguntas_by_topico,
    get_all_perguntas_indices,
)
from .quiz_service import (
    gerar_ordens_opcoes,
    obter_pergunta_com_ordem,
    calcular_analise_desempenho,
    inicializar_sessao_quiz,
)
from .simuladores import (
    gerar_ranking_operadores,
    gerar_status_docas,
    gerar_kpis_recebimento,
    gerar_kpis_estoque,
    gerar_kpis_picking,
    gerar_kpis_expedicao,
)

__all__ = [
    "BANCO_PERGUNTAS",
    "get_pergunta_by_index",
    "get_perguntas_by_topico",
    "get_all_perguntas_indices",
    "gerar_ordens_opcoes",
    "obter_pergunta_com_ordem",
    "calcular_analise_desempenho",
    "inicializar_sessao_quiz",
    "gerar_ranking_operadores",
    "gerar_status_docas",
    "gerar_kpis_recebimento",
    "gerar_kpis_estoque",
    "gerar_kpis_picking",
    "gerar_kpis_expedicao",
]
