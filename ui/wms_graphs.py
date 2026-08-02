"""
=============================================================================
  GRÁFICOS OPERACIONAIS WMS DIDÁTICO (wms_graphs.py) — LogiQ
  Geração de gráficos Plotly interativos em formato JSON para o novo
  Dashboard Operacional do Turno (/dashboard-turno).
=============================================================================
"""
import json
from typing import Dict, Any, List
from functools import lru_cache
import plotly.graph_objects as go
import plotly.utils


@lru_cache(maxsize=1)
def _base_layout() -> Dict[str, Any]:
    """
    Layout base unificado para gráficos interativos do Dashboard de Turno.

    Returns:
        Dict[str, Any]: Dicionário de propriedades do layout Plotly.
    """
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a", family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=30, b=40),
    )


def _fig_to_json(fig: go.Figure) -> str:
    """
    Serializa o gráfico Plotly em string JSON compatível com frontend.

    Args:
        fig (go.Figure): Gráfico gerado.

    Returns:
        str: JSON contendo data e layout do gráfico.
    """
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def gerar_grafico_funil_turno(itens: List[Dict[str, Any]]) -> str:
    """
    Gera um gráfico de barras comparando a contagem de caixinhas em cada
    uma das 4 etapas do turno operacional (Recebimento, Estoque, Picking, Expedição).

    Args:
        itens: Lista dos itens no turno do aluno.

    Returns:
        str: JSON serializado do gráfico.
    """
    contagem = {
        "Recebimento": 0,
        "Estoque": 0,
        "Picking": 0,
        "Expedição": 0,
    }

    for it in itens:
        etapa = it.get("etapa", "recebimento").lower()
        if etapa == "recebimento":
            contagem["Recebimento"] += 1
        elif etapa == "estoque":
            contagem["Estoque"] += 1
        elif etapa == "picking":
            contagem["Picking"] += 1
        elif etapa == "expedicao":
            contagem["Expedição"] += 1

    etapas = list(contagem.keys())
    quantidades = list(contagem.values())
    cores = ["#2563eb", "#1e3a8a", "#f59e0b", "#10b981"]

    fig = go.Figure(
        go.Bar(
            x=etapas,
            y=quantidades,
            marker_color=cores,
            text=[str(q) for q in quantidades],
            textposition="auto",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Itens por Etapa do Turno", font=dict(size=14)),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", rangemode="tozero"),
        xaxis=dict(showgrid=False),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_acuracia_picking(acertos: int, erros: int) -> str:
    """
    Gera um gráfico de rosca (donut) mostrando a precisão das bipagens do aluno
    na etapa de separação de pedidos.

    Args:
        acertos: Quantidade de bipagens corretas.
        erros: Quantidade de bipagens incorretas (item trocado).

    Returns:
        str: JSON serializado do gráfico.
    """
    total = acertos + erros
    if total == 0:
        labels = ["Sem Bipagem Registrada"]
        values = [1]
        cores = ["#cbd5e1"]
    else:
        labels = ["Bipagem Correta", "Erro / Troca"]
        values = [acertos, max(0, erros)]
        cores = ["#10b981", "#ef4444"]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=cores),
            textinfo="label+percent",
            hoverinfo="label+value",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Acurácia na Separação (Picking)", font=dict(size=14)),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0.1),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_ocupacao_estantes(itens: List[Dict[str, Any]]) -> str:
    """
    Gera um gráfico de colunas quantificando quantas caixinhas estão alocadas
    em cada Rua de porta-paletes da sala.

    Args:
        itens: Lista de itens presentes no turno.

    Returns:
        str: JSON do gráfico Plotly.
    """
    contagem_ruas: Dict[str, int] = {}
    for it in itens:
        rua = str(it.get("rua", "---")).strip()
        if rua != "---":
            label = f"Rua {rua}"
            contagem_ruas[label] = contagem_ruas.get(label, 0) + 1

    if not contagem_ruas:
        ruas = ["Rua 01", "Rua 02", "Rua 03", "Rua 04"]
        quantidades = [0, 0, 0, 0]
    else:
        ruas = list(contagem_ruas.keys())
        quantidades = list(contagem_ruas.values())

    fig = go.Figure(
        go.Bar(
            x=ruas,
            y=quantidades,
            marker_color="#1e3a8a",
            text=[str(q) for q in quantidades],
            textposition="auto",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Itens por Rua (Endereçamento)", font=dict(size=14)),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", rangemode="tozero"),
        xaxis=dict(showgrid=False),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)
