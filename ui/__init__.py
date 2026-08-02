"""
=============================================================================
  Pacote de Componentes Visuais e Gráficos — LogiQ
  Armazena construtores de gráficos e elementos de interface.
=============================================================================
"""
from .charts import gerar_grafico_area, gerar_grafico_ocupacao
from .wms_graphs import (
    gerar_grafico_funil_turno,
    gerar_grafico_acuracia_picking,
    gerar_grafico_ocupacao_estantes,
)

__all__ = [
    "gerar_grafico_area",
    "gerar_grafico_ocupacao",
    "gerar_grafico_funil_turno",
    "gerar_grafico_acuracia_picking",
    "gerar_grafico_ocupacao_estantes",
]
