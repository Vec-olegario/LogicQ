"""
=============================================================================
  MÓDULO DE UTILITÁRIOS (helpers.py) — LogiQ
  Funções de data, hora e formatações gerais com tratamento de erros.
=============================================================================
"""
from datetime import datetime
from typing import Tuple, Optional


def hora_atual() -> str:
    """
    Retorna a hora atual formatada como 'HH:MM:SS'.

    Returns:
        str: Hora no formato de relógio de 24 horas (ex: '14:35:10').
    """
    return datetime.now().strftime("%H:%M:%S")


def data_atual() -> str:
    """
    Retorna a data atual formatada como 'DD/MM/AAAA'.

    Returns:
        str: Data do dia no formato brasileiro (ex: '02/08/2026').
    """
    return datetime.now().strftime("%d/%m/%Y")


def calcular_estatisticas_tempo(
    inicio_iso: Optional[str],
    fim_iso: Optional[str],
    total_perguntas: int
) -> Tuple[str, str]:
    """
    Calcula a duração total e a média de tempo por pergunta em um quiz.

    Args:
        inicio_iso (Optional[str]): Carimbo de data/hora ISO 8601 de início.
        fim_iso (Optional[str]): Carimbo de data/hora ISO 8601 de término.
        total_perguntas (int): Quantidade total de perguntas respondidas.

    Returns:
        Tuple[str, str]:
            - tempo_str: Tempo total formatado em 'MM:SS' (ex: '01:45').
            - media_str: Média de tempo por pergunta (ex: '7.5s').
    """
    if not inicio_iso or not fim_iso or total_perguntas <= 0:
        return "--:--", "--"

    try:
        dt_inicio = datetime.fromisoformat(inicio_iso)
        dt_fim = datetime.fromisoformat(fim_iso)
        segundos = int((dt_fim - dt_inicio).total_seconds())

        if segundos < 0:
            return "--:--", "--"

        minutos, segs = divmod(segundos, 60)
        tempo_str = f"{minutos:02d}:{segs:02d}"
        media_str = f"{segundos / total_perguntas:.1f}s"
        return tempo_str, media_str

    except (ValueError, TypeError, OverflowError):
        # Proteção robusta caso as datas ISO estejam corrompidas na sessão
        return "--:--", "--"
