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
        Dict[str, Any]: Configuração de fundo transparente, hover e tipografia.
    """
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a", family="Inter, -apple-system, sans-serif"),
        margin=dict(l=30, r=20, t=35, b=30),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=13,
            font_family="Inter, sans-serif",
            font_color="#f8fafc",
            bordercolor="#334155",
        ),
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
        ("Recebimento", [random.randint(30, 90) for _ in range(7)], "#2563eb"),
        ("Estoque", [random.randint(40, 100) for _ in range(7)], "#3b82f6"),
        ("Picking", [random.randint(50, 120) for _ in range(7)], "#0d9488"),
        ("Expedição", [random.randint(35, 95) for _ in range(7)], "#10b981"),
    ]

    for nome, vals, cor in dados:
        fig.add_trace(
            go.Scatter(
                x=dias,
                y=vals,
                name=nome,
                fill="tozeroy",
                line=dict(color=cor, width=2.5, shape="spline"),
                hovertemplate="<b>%{x}</b><br>" + nome + ": <b>%{y} volumes</b><extra></extra>",
            )
        )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Evolução Semanal de Volumes por Etapa", font=dict(size=14, color="#1e293b", weight="bold")),
        legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11)),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", rangemode="tozero", title=dict(text="Volumes", font=dict(size=11))),
        height=320,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_ocupacao() -> str:
    """
    Constrói um gráfico de barras horizontais indicando a ocupação percentual
    das 8 ruas (Rua A a H) na área de estocagem do galpão, com cores semânticas.

    Returns:
        str: JSON serializado do gráfico para o setor de Estoque.
    """
    ruas: List[str] = [f"Rua {chr(65 + i)}" for i in range(8)]
    valores: List[int] = [random.randint(55, 96) for _ in range(8)]

    cores: List[str] = []
    for v in valores:
        if v >= 90:
            cores.append("#f43f5e")  # Vermelho coral para alerta de capacidade alta
        elif v >= 75:
            cores.append("#f59e0b")  # Amarelo/laranja para atenção
        else:
            cores.append("#10b981")  # Verde esmeralda para ocupação ideal

    fig = go.Figure(
        go.Bar(
            y=ruas,
            x=valores,
            orientation="h",
            marker=dict(
                color=cores,
                line=dict(color="rgba(255,255,255,0.8)", width=1),
            ),
            text=[f"{v}%" for v in valores],
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Ocupação: <b>%{x}% da Capacidade</b><extra></extra>",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Taxa de Ocupação por Rua do Galpão (%)", font=dict(size=14, color="#1e293b", weight="bold")),
        yaxis=dict(showgrid=False, autorange="reversed"),
        xaxis=dict(
            range=[0, 105],
            showgrid=True,
            gridcolor="#f1f5f9",
            title=dict(text="Ocupação (%)", font=dict(size=11)),
        ),
        height=320,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)

