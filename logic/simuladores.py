"""
=============================================================================
  SIMULADORES DE OPERAÇÃO E KPIS (simuladores.py) — LogiQ
  Geradores de dados simulados de armazém, ranking de operadores, status de docas
  e métricas (KPIs) dinâmicas para as páginas educativas.
=============================================================================
"""
import random
from typing import List, Dict, Any


def gerar_ranking_operadores() -> List[Dict[str, Any]]:
    """
    Gera um ranking simulado de produtividade e acurácia de separadores no Picking.

    Returns:
        List[Dict[str, Any]]: Lista contendo 5 operadores ordenados por pedidos separados.
    """
    nomes = ["Ana S.", "Carlos M.", "Juliana R.", "Pedro L.", "Maria F."]
    pedidos = sorted([random.randint(20, 65) for _ in range(5)], reverse=True)
    acertos = [round(random.uniform(96.0, 100.0), 1) for _ in range(5)]

    return [
        {"picker": nome, "pedidos": pedido, "acertos": acerto}
        for nome, pedido, acerto in zip(nomes, pedidos, acertos)
    ]


def gerar_status_docas() -> List[Dict[str, str]]:
    """
    Gera o status operacional simulado para as 6 docas do Centro de Distribuição.

    Returns:
        List[Dict[str, str]]: Lista de docas com número, status em texto e cores de estilo.
    """
    docas: List[Dict[str, str]] = []
    for i in range(1, 7):
        status = random.choice(["🟢 Livre", "🟡 Carregando", "🔴 Ocupada"])
        if "Livre" in status:
            cor, bg = "#10b981", "#ecfdf5"
        elif "Carregando" in status:
            cor, bg = "#f59e0b", "#fffbeb"
        else:
            cor, bg = "#ef4444", "#fef2f2"

        docas.append({"numero": str(i), "status": status, "cor": cor, "bg": bg})
    return docas


def gerar_kpis_recebimento() -> Dict[str, Any]:
    """
    Gera KPIs dinâmicos simulados para a página do setor de Recebimento.

    Returns:
        Dict[str, Any]: Dicionário com eficiência, notas fiscais e divergências.
    """
    return {
        "ef": random.randint(85, 99),
        "ef_d": f"+{random.randint(1, 5)}%",
        "nfs": random.randint(30, 75),
        "nfs_d": f"+{random.randint(2, 10)}",
        "div": random.randint(0, 5),
        "div_d": f"-{random.randint(0, 2)}",
        "pend": random.randint(2, 12),
        "pend_d": f"-{random.randint(1, 3)}",
    }


def gerar_kpis_estoque() -> Dict[str, Any]:
    """
    Gera KPIs dinâmicos simulados para a página do setor de Estoque.

    Returns:
        Dict[str, Any]: Dicionário com acurácia, posições ocupadas e movimentações.
    """
    return {
        "ac": round(random.uniform(96.0, 99.9), 1),
        "ac_d": f"+{round(random.uniform(0.1, 1.5), 1)}%",
        "pos": random.randint(650, 820),
        "pos_d": f"+{random.randint(5, 20)}",
        "mov": random.randint(40, 130),
        "mov_d": f"+{random.randint(5, 15)}",
        "pend": random.randint(3, 15),
        "pend_d": f"-{random.randint(1, 4)}",
    }


def gerar_kpis_picking() -> Dict[str, Any]:
    """
    Gera KPIs dinâmicos simulados para a página do setor de Picking.

    Returns:
        Dict[str, Any]: Dicionário com produtividade/hora, erros de separação e fila.
    """
    return {
        "ph": random.randint(18, 42),
        "ph_d": f"+{random.randint(1, 6)}",
        "err": round(random.uniform(0.1, 2.5), 1),
        "err_d": f"-{round(random.uniform(0.1, 0.8), 1)}%",
        "fila": random.randint(5, 35),
        "fila_d": f"-{random.randint(2, 8)}",
        "ef": random.randint(88, 99),
        "ef_d": f"+{random.randint(1, 4)}%",
    }


def gerar_kpis_expedicao() -> Dict[str, Any]:
    """
    Gera KPIs dinâmicos simulados para a página do setor de Expedição.

    Returns:
        Dict[str, Any]: Dicionário com volumes expedidos, tempo médio e veículos.
    """
    return {
        "exp": random.randint(80, 220),
        "exp_d": f"+{random.randint(5, 25)}",
        "tempo": random.randint(4, 12),
        "tempo_d": f"-{random.randint(1, 3)} min",
        "veic": random.randint(3, 8),
        "veic_d": f"+{random.randint(1, 2)}",
        "pend": random.randint(4, 18),
        "pend_d": f"-{random.randint(1, 5)}",
    }
