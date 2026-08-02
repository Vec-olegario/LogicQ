"""
=============================================================================
  CONSTRUTORES DE GRÁFICOS (charts.py) — LogiQ
  Geração otimizada de gráficos Plotly em formato JSON para renderização
  responsiva no frontend (área de movimentação e ocupação de ruas).
=============================================================================
"""
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from functools import lru_cache
import plotly.graph_objects as go
import plotly.utils


@lru_cache(maxsize=1)
def _base_layout() -> Dict[str, Any]:
    """
    Retorna a estilização base compartilhada por todos os gráficos do LogiQ.
    Utiliza lru_cache para evitar re-alocação repetitiva do dicionário de estilo.

    Returns:
        Dict[str, Any]: Configuração de fundo transparente e tipografia.
    """
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif"),
        margin=dict(l=30, r=20, t=10, b=30),
    )


def _fig_to_json(fig: go.Figure) -> str:
    """
    Serializa um objeto Figure do Plotly em string JSON limpa.

    Args:
        fig (go.Figure): Instância do gráfico Plotly.

    Returns:
        str: String JSON pronta para ser interpretada pela biblioteca Plotly.js.
    """
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def gerar_grafico_area() -> str:
    """
    Constrói um gráfico de área temporal com simulação de 7 dias para as 4 etapas
    operacionais do Centro de Distribuição (Recebimento, Estoque, Picking e Expedição).

    Returns:
        str: JSON serializado do gráfico para injeção em template.
    """
    dias: List[str] = [
        (datetime.now() - timedelta(days=i)).strftime("%d/%m")
        for i in range(6, -1, -1)
    ]
    fig = go.Figure()

    dados: List[Tuple[str, List[int], str]] = [
        ("Recebimento", [random.randint(30, 90) for _ in range(7)], "#bfdbfe"),
        ("Estoque", [random.randint(40, 100) for _ in range(7)], "#93c5fd"),
        ("Picking", [random.randint(50, 120) for _ in range(7)], "#3b82f6"),
        ("Expedição", [random.randint(35, 95) for _ in range(7)], "#1e40af"),
    ]

    for nome, vals, cor in dados:
        fig.add_trace(
            go.Scatter(
                x=dias,
                y=vals,
                name=nome,
                fill="tozeroy",
                line=dict(color=cor, width=2),
            )
        )

    layout = _base_layout().copy()
    layout.update(
        legend=dict(orientation="h", y=1.12, x=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", rangemode="tozero"),
        height=320,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_ocupacao() -> str:
    """
    Constrói um gráfico de barras indicando a ocupação percentual das 8 ruas (Rua A a H)
    na área de estocagem do galpão.

    Returns:
        str: JSON serializado do gráfico de barras para o setor de Estoque.
    """
    ruas: List[str] = [f"Rua {chr(65 + i)}" for i in range(8)]
    valores: List[int] = [random.randint(55, 98) for _ in range(8)]

    fig = go.Figure(
        go.Bar(
            x=ruas,
            y=valores,
            marker_color="#1e40af",
            text=[f"{v}%" for v in valores],
            textposition="outside",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        yaxis=dict(range=[0, 110], showgrid=True, gridcolor="#e5e7eb"),
        xaxis=dict(showgrid=False),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)
