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
        Dict[str, Any]: Dicionário de propriedades do layout Plotly com
        estilização de tooltips, transparência e tipografia harmoniosa.
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
    Serializa o gráfico Plotly em string JSON compatível com frontend.

    Args:
        fig (go.Figure): Gráfico gerado.

    Returns:
        str: JSON contendo data e layout do gráfico.
    """
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def gerar_grafico_funil_turno(itens: List[Dict[str, Any]]) -> str:
    """
    Gera um gráfico de Funil Logístico (Plotly Funnel) demonstrando a passagem
    e retenção de itens entre as 4 etapas operacionais do turno.

    Args:
        itens: Lista dos itens no turno do aluno.

    Returns:
        str: JSON serializado do gráfico interativo.
    """
    contagem: Dict[str, int] = {
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
    cores = ["#2563eb", "#3b82f6", "#0d9488", "#10b981"]

    fig = go.Figure(
        go.Funnel(
            y=etapas,
            x=quantidades,
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=cores,
                line=dict(width=1, color="rgba(255,255,255,0.8)"),
            ),
            connector=dict(
                line=dict(color="rgba(148,163,184,0.45)", width=2, dash="dot")
            ),
            hovertemplate="<b>%{y}</b><br>Itens Bipados: <b>%{value} un</b><br>Fluxo Injetado: <b>%{percentInitial}</b><extra></extra>",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Progresso do Fluxo no Galpão", font=dict(size=14, color="#1e293b", weight="bold")),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_acuracia_picking(acertos: int, erros: int) -> str:
    """
    Gera um gráfico de rosca interativo (Donut KPI) com indicador percentual
    centralizado para exibir a precisão das bipagens em Picking.

    Args:
        acertos: Quantidade de bipagens corretas.
        erros: Quantidade de bipagens incorretas (item trocado).

    Returns:
        str: JSON serializado do gráfico.
    """
    total = acertos + erros
    if total == 0:
        labels = ["Aguardando Bipagem"]
        values = [1]
        cores = ["#e2e8f0"]
        texto_central = "<b>--</b><br><span style='font-size:11px;color:#64748b'>Sem Bipagem</span>"
    else:
        percentual = round((acertos / total) * 100)
        labels = ["Bipagem Correta", "Erro / Troca de Código"]
        values = [acertos, max(0, erros)]
        cores = ["#10b981", "#f43f5e"]
        texto_central = f"<b>{percentual}%</b><br><span style='font-size:11px;color:#64748b'>Acurácia</span>"

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.72,
            marker=dict(
                colors=cores,
                line=dict(color="#ffffff", width=2),
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>Qtd: %{value} (%{percent})<extra></extra>",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Índice de Qualidade na Separação", font=dict(size=14, color="#1e293b", weight="bold")),
        showlegend=True,
        legend=dict(orientation="h", y=-0.12, x=0.08, font=dict(size=11)),
        height=300,
        annotations=[
            dict(
                text=texto_central,
                x=0.5,
                y=0.5,
                font=dict(size=22, color="#0f172a", family="Inter, sans-serif"),
                showarrow=False,
            )
        ],
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)


def gerar_grafico_ocupacao_estantes(itens: List[Dict[str, Any]]) -> str:
    """
    Gera um gráfico horizontal de ocupação por Rua para facilitar a
    leitura da distribuição física dos itens no porta-paletes do CD.

    Args:
        itens: Lista de itens presentes no turno.

    Returns:
        str: JSON do gráfico Plotly.
    """
    contagem_ruas: Dict[str, int] = {"01": 0, "02": 0, "03": 0, "04": 0}
    for it in itens:
        rua_raw = str(it.get("rua", "---")).strip()
        if rua_raw != "---":
            rua_num = rua_raw.zfill(2) if rua_raw.isdigit() else rua_raw
            contagem_ruas[rua_num] = contagem_ruas.get(rua_num, 0) + 1

    ruas_ordenadas = sorted(contagem_ruas.keys())
    rotulos = [f"Rua {r}" for r in ruas_ordenadas]
    quantidades = [contagem_ruas[r] for r in ruas_ordenadas]

    fig = go.Figure(
        go.Bar(
            y=rotulos,
            x=quantidades,
            orientation="h",
            marker=dict(
                color=["#3b82f6", "#2563eb", "#1d4ed8", "#1e40af"][: len(rotulos)],
                line=dict(color="rgba(255,255,255,0.7)", width=1),
            ),
            text=[f"{q} un" if q > 0 else "" for q in quantidades],
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Alocados: <b>%{x} item(ns)</b><extra></extra>",
        )
    )

    layout = _base_layout().copy()
    layout.update(
        title=dict(text="Distribuição por Rua (Endereçamento)", font=dict(size=14, color="#1e293b", weight="bold")),
        yaxis=dict(showgrid=False, autorange="reversed"),
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", rangemode="tozero", title=dict(text="Caixas", font=dict(size=11))),
        height=300,
    )
    fig.update_layout(**layout)
    return _fig_to_json(fig)

