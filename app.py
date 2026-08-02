"""
=============================================================================
  GALPÃO LOGÍSTICO DIDÁTICO (LogiQ) — Flask v2.0 Modular
  Execute : python app.py
  Acesse  : http://localhost:5000
=============================================================================
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response,
)

from config import SECRET_KEY, TOPICOS
from utils import hora_atual, data_atual, calcular_estatisticas_tempo
from ui import gerar_grafico_ocupacao
from logic import (
    BANCO_PERGUNTAS,
    get_pergunta_by_index,
    gerar_ordens_opcoes,
    obter_pergunta_com_ordem,
    calcular_analise_desempenho,
    inicializar_sessao_quiz,
    gerar_ranking_operadores,
    gerar_status_docas,
    gerar_kpis_recebimento,
    gerar_kpis_estoque,
    gerar_kpis_picking,
    gerar_kpis_expedicao,
)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.jinja_env.filters["enumerate"] = enumerate


# ─────────────────────────────────────────────
# HANDLERS DE ERRO GERAIS
# ─────────────────────────────────────────────
@app.errorhandler(404)
def pagina_nao_encontrada(e: Any) -> Response:
    """
    Handler para rotas inexistentes (404).
    Redireciona para a página inicial com mensagem informativa.
    """
    flash("⚠️ A página acessada não foi encontrada. Retornando ao início.", "warning")
    return redirect(url_for("inicio"))


@app.errorhandler(500)
def erro_interno_servidor(e: Any) -> Response:
    """
    Handler para erros internos do servidor (500).
    Evita exibição de stack trace pura para o usuário final.
    """
    flash("❌ Ocorreu um erro interno no servidor. Tentando restaurar a sessão.", "danger")
    return redirect(url_for("inicio"))


# ─────────────────────────────────────────────
# ROTAS — PÁGINAS EDUCATIVAS
# ─────────────────────────────────────────────
@app.route("/")
def inicio() -> str:
    """Renderiza a página inicial do CD didático."""
    return render_template("inicio.html")


@app.route("/recebimento")
def recebimento() -> str:
    """Renderiza a página do setor de Recebimento com KPIs simulados."""
    return render_template(
        "recebimento.html",
        hora=hora_atual(),
        data=data_atual(),
        k=gerar_kpis_recebimento(),
    )


@app.route("/estoque")
def estoque() -> str:
    """Renderiza a página do setor de Estoque com KPIs e gráfico de ocupação."""
    return render_template(
        "estoque.html",
        hora=hora_atual(),
        data=data_atual(),
        k=gerar_kpis_estoque(),
        grafico_json=gerar_grafico_ocupacao(),
    )


@app.route("/picking")
def picking() -> str:
    """Renderiza a página do setor de Picking com ranking de separadores."""
    return render_template(
        "picking.html",
        hora=hora_atual(),
        data=data_atual(),
        k=gerar_kpis_picking(),
        ranking=gerar_ranking_operadores(),
    )


@app.route("/expedicao")
def expedicao() -> str:
    """Renderiza a página do setor de Expedição com status das docas."""
    return render_template(
        "expedicao.html",
        hora=hora_atual(),
        data=data_atual(),
        k=gerar_kpis_expedicao(),
        docas=gerar_status_docas(),
    )


# ─────────────────────────────────────────────
# ROTAS — SITUAÇÃO E CONFERÊNCIA OPERACIONAL
# ─────────────────────────────────────────────
@app.route("/situacao/reiniciar")
def situacao_reiniciar() -> Response:
    """Reinicia o turno operacional limpanho as etapas do progresso na sessão."""
    session.pop("situacao_etapas", None)
    session.pop("situacao_dados", None)
    flash("🔄 Turno operacional reiniciado com sucesso!", "info")
    return redirect(url_for("situacao"))


@app.route("/situacao/registrar/<etapa>", methods=["POST"])
def situacao_registrar_etapa(etapa: str) -> Response:
    """
    Registra uma etapa operacional via requisição POST direcionada,
    evitando a perda do formulário e mantendo o progresso das etapas.
    """
    etapas: List[str] = session.get("situacao_etapas", [])
    if etapa in ("recebimento", "estoque", "picking", "expedicao"):
        if etapa not in etapas:
            etapas.append(etapa)
        session["situacao_etapas"] = etapas

        dados: Dict[str, Any] = session.get("situacao_dados", {})
        dados[etapa] = request.form.to_dict()
        session["situacao_dados"] = dados

        flash(f"✅ Registro da etapa de {etapa.capitalize()} concluído com sucesso!", "success")

    return redirect(url_for("situacao"))


@app.route("/situacao", methods=["GET", "POST"])
def situacao() -> str:
    """
    Gerencia a página integradora de Situação do Turno Operacional.
    Processa submissões dos formulários por setor e calcula se o ciclo foi completo.
    """
    if "situacao_etapas" not in session:
        session["situacao_etapas"] = []

    if request.method == "POST":
        etapa = request.form.get("etapa", "")

        if etapa == "recebimento":
            nf = request.form.get("nf", "---")
            sku = request.form.get("sku", "---")
            qtd = request.form.get("quantidade", "1")
            forn = request.form.get("fornecedor", "---")
            cond = request.form.get("condicao", "---")
            flash(
                f"✅ Recebimento registrado! NF: {nf} | SKU: {sku} | Qtd: {qtd} | "
                f"Fornecedor: {forn} | Condição: {cond}",
                "rec",
            )

        elif etapa == "estoque":
            sku = request.form.get("sku", "---")
            tipo = request.form.get("tipo_mov", "---")
            qtd = request.form.get("quantidade", "1")
            rua = request.form.get("rua", "---")
            prat = request.form.get("prateleira", "---")
            niv = request.form.get("nivel", "---")
            flash(
                f"✅ Movimentação registrada! SKU: {sku} | {tipo} | Qtd: {qtd} | "
                f"Posição: {rua} → {prat} → {niv}",
                "est",
            )

        elif etapa == "picking":
            pedido = request.form.get("pedido", "---")
            sku = request.form.get("sku", "---")
            qtd = request.form.get("quantidade", "1")
            orig = request.form.get("origem", "---")
            metodo = request.form.get("metodo", "---")
            conf = request.form.get("conferencia", "---")
            flash(
                f"✅ Separação confirmada! Pedido: {pedido} | SKU: {sku} | Qtd: {qtd} | "
                f"Origem: {orig} | Método: {metodo} | Conferência: {conf}",
                "pick",
            )

        elif etapa == "expedicao":
            pedido = request.form.get("pedido", "---")
            vols = request.form.get("volumes", "1")
            peso = request.form.get("peso", "---")
            transp = request.form.get("transportadora", "---")
            doca = request.form.get("doca", "---")
            prior = request.form.get("prioridade", "Normal")
            flash(
                f"✅ Despacho confirmado! Pedido: {pedido} | Volumes: {vols} | Peso: {peso} kg | "
                f"Transportadora: {transp} | Doca: {doca} | Prioridade: {prior}",
                "exp",
            )

        if etapa in ("recebimento", "estoque", "picking", "expedicao"):
            etapas: List[str] = session.get("situacao_etapas", [])
            if etapa not in etapas:
                etapas.append(etapa)
            session["situacao_etapas"] = etapas

        return redirect(url_for("situacao"))

    etapas_concluidas: List[str] = session.get("situacao_etapas", [])
    todas_concluidas = all(
        e in etapas_concluidas
        for e in ("recebimento", "estoque", "picking", "expedicao")
    )

    return render_template(
        "situacao.html",
        hora=hora_atual(),
        data=data_atual(),
        etapas_concluidas=etapas_concluidas,
        todas_concluidas=todas_concluidas,
    )


# ─────────────────────────────────────────────
# ROTAS — QUIZ LOGÍSTICO (COM SESSÃO LEVE)
# ─────────────────────────────────────────────
@app.route("/quiz")
def quiz() -> str:
    """
    Gerencia a interface de Quiz Logístico em seus 3 estados:
    - SETUP   : Seleção de modo de jogo e tópicos
    - PLAYING : Renderização da pergunta da rodada atual
    - RESULT  : Exibição do relatório analítico e placar final
    """
    setor_param = request.args.get("setor") or request.args.get("topico")
    modo_param = request.args.get("modo")
    iniciar_param = request.args.get("iniciar", "").lower() == "true"

    if setor_param and setor_param in TOPICOS and iniciar_param:
        session["quiz"] = inicializar_sessao_quiz("topico", setor_param)
        return redirect(url_for("quiz"))

    q: Dict[str, Any] = session.get("quiz", {"state": "SETUP"})

    selected_topico = (
        setor_param if (setor_param and setor_param in TOPICOS) else "Recebimento"
    )
    selected_modo = (
        modo_param
        if modo_param in ["rapido", "padrao", "completo", "topico"]
        else ("topico" if setor_param else "padrao")
    )

    ctx: Dict[str, Any] = dict(
        quiz=q,
        pergunta=None,
        respondido=False,
        resposta_info=None,
        total=0,
        idx=0,
        analise={},
        percentual=0,
        pontos=0,
        tempo_str="--:--",
        media_str="--",
        topicos=TOPICOS,
        perguntas=BANCO_PERGUNTAS,
        selected_topico=selected_topico,
        selected_modo=selected_modo,
        hora=hora_atual(),
        data=data_atual(),
    )

    if q.get("state") == "PLAYING":
        idx = q.get("idx", 0)
        perguntas_ids = q.get("perguntas_ids", [])
        if 0 <= idx < len(perguntas_ids):
            p_idx = perguntas_ids[idx]
            orders = q.get("opcoes_orders", [])
            perm = orders[idx] if idx < len(orders) else [0, 1, 2, 3]
            ctx["pergunta"] = obter_pergunta_com_ordem(p_idx, perm)

            ctx["respondido"] = str(idx) in q.get("respostas", {})
            ctx["resposta_info"] = q.get("respostas", {}).get(str(idx))
            ctx["total"] = len(perguntas_ids)
            ctx["idx"] = idx

    elif q.get("state") == "RESULT":
        perguntas_ids = q.get("perguntas_ids", [])
        total = len(perguntas_ids)
        pontos = q.get("pontuacao", 0)
        ctx["total"] = total
        ctx["pontos"] = pontos
        ctx["percentual"] = round(pontos / total * 100) if total else 0

        orders = q.get("opcoes_orders", [])
        ctx["perguntas"] = {
            p_idx: obter_pergunta_com_ordem(
                p_idx, orders[i] if i < len(orders) else [0, 1, 2, 3]
            )
            for i, p_idx in enumerate(perguntas_ids)
        }

        ctx["analise"] = calcular_analise_desempenho(
            perguntas_ids, q.get("respostas", {})
        )

        tempo_str, media_str = calcular_estatisticas_tempo(
            q.get("inicio"), q.get("fim"), total
        )
        ctx["tempo_str"] = tempo_str
        ctx["media_str"] = media_str

    return render_template("quiz.html", **ctx)


@app.route("/quiz/iniciar", methods=["GET", "POST"])
def quiz_iniciar() -> Response:
    """Inicializa um novo quiz de acordo com o modo e tópico especificados."""
    if request.method == "POST":
        modo = request.form.get("modo", "rapido")
        topico = request.form.get("topico", "Recebimento")
    else:
        modo = (
            request.args.get("modo")
            or ("topico" if (request.args.get("topico") or request.args.get("setor")) else "rapido")
        )
        topico = (
            request.args.get("topico")
            or request.args.get("setor")
            or "Recebimento"
        )

    session["quiz"] = inicializar_sessao_quiz(modo, topico)
    return redirect(url_for("quiz"))


@app.route("/quiz/responder", methods=["POST"])
def quiz_responder() -> Response:
    """Processa a resposta enviada pelo usuário na rodada atual do quiz."""
    q: Optional[Dict[str, Any]] = session.get("quiz")
    if not q or q.get("state") != "PLAYING":
        return redirect(url_for("quiz"))

    idx = q.get("idx", 0)
    if str(idx) in q.get("respostas", {}):
        return redirect(url_for("quiz"))

    try:
        escolhida = int(request.form.get("resposta", -1))
    except (ValueError, TypeError):
        return redirect(url_for("quiz"))

    perguntas_ids = q.get("perguntas_ids", [])
    if not (0 <= idx < len(perguntas_ids)):
        return redirect(url_for("quiz"))

    p_idx = perguntas_ids[idx]
    orders = q.get("opcoes_orders", [])
    perm = orders[idx] if idx < len(orders) else [0, 1, 2, 3]

    q_orig = get_pergunta_by_index(p_idx)
    if not q_orig:
        return redirect(url_for("quiz"))

    correta_idx = perm.index(q_orig["correta"])
    correta = escolhida == correta_idx

    q["respostas"][str(idx)] = {"escolhida": escolhida, "correta": correta}
    if correta:
        q["pontuacao"] = q.get("pontuacao", 0) + 1

    session["quiz"] = q
    return redirect(url_for("quiz"))


@app.route("/quiz/avancar")
def quiz_avancar() -> Response:
    """Avança para a próxima pergunta ou finaliza o quiz indo para o placar."""
    q: Optional[Dict[str, Any]] = session.get("quiz")
    if not q or q.get("state") != "PLAYING":
        return redirect(url_for("quiz"))

    idx = q.get("idx", 0)
    total = len(q.get("perguntas_ids", []))

    if idx < total - 1:
        q["idx"] = idx + 1
    else:
        q["state"] = "RESULT"
        q["fim"] = datetime.now().isoformat()

    session["quiz"] = q
    return redirect(url_for("quiz"))


@app.route("/quiz/reiniciar")
def quiz_reiniciar() -> Response:
    """Encerra a sessão de quiz e retorna à tela inicial de SETUP."""
    session.pop("quiz", None)
    return redirect(url_for("quiz"))


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
