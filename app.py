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
    jsonify,
)

from config import SECRET_KEY, TOPICOS
from utils import hora_atual, data_atual, calcular_estatisticas_tempo, parse_int_safe
from ui import (
    gerar_grafico_ocupacao,
    gerar_grafico_funil_turno,
    gerar_grafico_acuracia_picking,
    gerar_grafico_ocupacao_estantes,
)
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
    obter_ou_criar_turno,
    registrar_bipagem_recebimento,
    registrar_enderecamento_estoque,
    validar_bipagem_picking,
    registrar_expedicao_item,
    editar_item_turno,
    gerar_csv_turno,
    atualizar_nome_operador,
    responder_duvida_logistica,
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
@app.route("/inicio")
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
    """Reinicia o turno operacional limpando as etapas do progresso e o turno ativo."""
    session.pop("situacao_etapas", None)
    session.pop("situacao_dados", None)
    session.pop("turno_id", None)
    flash("🔄 Turno operacional reiniciado com sucesso! Todos os dados de bipagem foram zerados.", "info")
    return redirect(url_for("situacao"))


@app.route("/situacao/salvar-nome", methods=["POST"])
def situacao_salvar_nome() -> Response:
    """Permite ao usuário definir ou atualizar o seu próprio nome no turno operacional."""
    turno_id, turno = _garantir_turno_sessao()
    nome = request.form.get("nome_operador", "").strip() or "Operador(a)"
    atualizar_nome_operador(turno_id, nome)
    flash(f"👤 Operador(a) identificado como: {nome}", "success")
    return redirect(request.referrer or url_for("situacao"))


def processar_registro_etapa(etapa: str, form_data: Dict[str, Any], turno_id: str) -> None:
    """Processa a bipagem/registro WMS da etapa operacional e atualiza o progresso do turno."""
    if etapa == "recebimento":
        codigo = form_data.get("codigo", "").strip() or form_data.get("nf", "---")
        sku = form_data.get("sku", "---")
        desc = form_data.get("descricao", "Caixa de Entrada Didática")
        qtd = parse_int_safe(form_data.get("quantidade", 1), default=1)
        forn = form_data.get("fornecedor", "---")
        cond = form_data.get("condicao", "Aprovado")
        registrar_bipagem_recebimento(turno_id, codigo, sku, desc, qtd, forn, cond)
        flash(f"✅ Recebimento registrado! Código: {codigo} | SKU: {sku} | Qtd: {qtd} un | Inspeção: {cond}", "success")

    elif etapa == "estoque":
        item_id = form_data.get("item_id", "")
        rua = form_data.get("rua", "01")
        prat = form_data.get("prateleira", "A")
        niv = form_data.get("nivel", "1")
        sku = form_data.get("sku", "---")
        registrar_enderecamento_estoque(turno_id, item_id, rua, prat, niv)
        flash(f"✅ Endereçamento de Estoque registrado! Posição: Rua {rua} → Estante {prat} → Nível {niv}", "success")

    elif etapa == "picking":
        item_id = form_data.get("item_id", "")
        codigo_bipado = form_data.get("codigo_bipado", "")
        pedido = form_data.get("pedido", "PED-8821")
        if item_id and codigo_bipado:
            sucesso, msg_feedback = validar_bipagem_picking(turno_id, item_id, codigo_bipado, pedido)
            flash(msg_feedback, "success" if sucesso else "danger")
        else:
            flash("✅ Separação de Picking registrada!", "success")

    elif etapa == "expedicao":
        item_id = form_data.get("item_id", "")
        doca = form_data.get("doca_saida", "Doca 01")
        conferente = form_data.get("conferente", "Conferente LogiQ")
        if item_id:
            registrar_expedicao_item(turno_id, item_id, doca, conferente)
        transp = form_data.get("transportadora", "TransLog Express")
        placa = form_data.get("placa", "ABC-1234")
        flash(f"✅ Expedição concluída! Veículo {placa} ({transp}) liberado na {doca}.", "success")

    if etapa in ("recebimento", "estoque", "picking", "expedicao"):
        etapas: List[str] = session.get("situacao_etapas", [])
        if etapa not in etapas:
            etapas.append(etapa)
        session["situacao_etapas"] = etapas


def _garantir_turno_sessao() -> Tuple[str, Dict[str, Any]]:
    """Garante que haja um turno operacional ativo na sessão do usuário e o retorna."""
    turno_id = session.get("turno_id")
    turno_id, turno = obter_ou_criar_turno(turno_id)
    session["turno_id"] = turno_id
    return turno_id, turno


@app.route("/situacao/registrar/<etapa>", methods=["POST"])
def situacao_registrar_etapa(etapa: str) -> Response:
    """
    Registra uma etapa operacional via requisição POST direcionada,
    mantendo compatibilidade com o fluxo de progresso e WMS Didático.
    """
    turno_id, _ = _garantir_turno_sessao()

    processar_registro_etapa(etapa, request.form.to_dict(), turno_id)
    return redirect(url_for("situacao"))


@app.route("/situacao", methods=["GET", "POST"])
def situacao() -> str:
    """
    Gerencia a página integradora de Situação do Turno Operacional com suporte
    a Bipagem de Código de Barras (WMS Didático / Phygital Lab).
    """
    if "situacao_etapas" not in session:
        session["situacao_etapas"] = []

    turno_id, turno = _garantir_turno_sessao()

    if request.method == "POST":
        etapa = request.form.get("etapa", "")
        if etapa:
            processar_registro_etapa(etapa, request.form.to_dict(), turno_id)
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
        turno=turno,
        itens=turno.get("itens", []),
    )


@app.route("/dashboard-turno")
def dashboard_turno() -> str:
    """
    Renderiza o Dashboard Operacional do Turno com tabela de itens bipados,
    gráficos Plotly interativos e opções de edição/exclusão.
    """
    turno_id, turno = _garantir_turno_sessao()

    itens = turno.get("itens", [])
    graf_funil = gerar_grafico_funil_turno(itens)
    graf_acuracia = gerar_grafico_acuracia_picking(
        turno.get("acertos_picking", 0),
        turno.get("erros_picking", 0),
    )
    graf_ocupacao = gerar_grafico_ocupacao_estantes(itens)

    return render_template(
        "dashboard_turno.html",
        turno=turno,
        itens=itens,
        graf_funil=graf_funil,
        graf_acuracia=graf_acuracia,
        graf_ocupacao=graf_ocupacao,
        hora=hora_atual(),
        data=data_atual(),
    )


@app.route("/dashboard-turno/editar/<item_id>", methods=["POST"])
def dashboard_turno_editar(item_id: str) -> Response:
    """Edita a quantidade e descrição de um item na tabela operacional do turno."""
    turno_id = session.get("turno_id", "")
    nova_qtd = parse_int_safe(request.form.get("quantidade", 1), default=1)
    nova_desc = request.form.get("descricao", "")
    if editar_item_turno(turno_id, item_id, nova_qtd, nova_desc):
        flash("✏️ Item atualizado com sucesso no WMS do turno!", "success")
    else:
        flash("⚠️ Item não encontrado.", "warning")
    return redirect(url_for("dashboard_turno"))


@app.route("/dashboard-turno/remover/<item_id>", methods=["POST"])
def dashboard_turno_remover(item_id: str) -> Response:
    """Remove uma caixinha que foi bipada ou adicionada por erro."""
    turno_id = session.get("turno_id", "")
    if remover_item_turno(turno_id, item_id):
        flash("🗑️ Item removido do turno com sucesso.", "info")
    else:
        flash("⚠️ Item não encontrado para remoção.", "warning")
    return redirect(url_for("dashboard_turno"))


@app.route("/dashboard-turno/exportar-planilha")
def dashboard_turno_exportar_planilha() -> Response:
    """
    Gera e baixa a planilha CSV/Excel do turno do aluno formatada em UTF-8 com BOM
    e separador ponto-e-vírgula. Requer que o usuário tenha identificado seu nome.
    """
    turno_id, turno = _garantir_turno_sessao()
    if turno.get("aluno", "Operador(a)") == "Operador(a)":
        flash("⚠️ Para baixar a planilha em CSV, você precisa primeiro informar o seu nome de Operador(a)!", "warning")
        return redirect(url_for("situacao"))

    conteudo_csv = gerar_csv_turno(turno_id)
    csv_com_bom = "\ufeff" + conteudo_csv
    headers = {
        "Content-Disposition": f"attachment; filename=relatorio_turno_logiq_{turno_id}.csv",
        "Content-Type": "text/csv; charset=utf-8",
    }
    return Response(csv_com_bom, mimetype="text/csv", headers=headers)


@app.route("/relatorio-turno")
def relatorio_turno() -> Response:
    """
    Renderiza o Relatório Oficial de Conferência e Performance Operacional do Turno.
    Permite impressão direta ou salvamento como documento PDF estruturado. Requer identificação do nome.
    """
    turno_id, turno = _garantir_turno_sessao()
    if turno.get("aluno", "Operador(a)") == "Operador(a)":
        flash("⚠️ Para emitir o Romaneio & Relatório Oficial do Turno, por favor informe o seu nome de Operador(a)!", "warning")
        return redirect(url_for("situacao"))

    itens = turno.get("itens", [])
    acertos = int(turno.get("acertos_picking", 0))
    erros = int(turno.get("erros_picking", 0))
    total_picking = acertos + erros
    acuracia = round((acertos / total_picking) * 100, 1) if total_picking > 0 else 100.0

    return render_template(
        "relatorio_turno.html",
        turno=turno,
        itens=itens,
        acuracia=acuracia,
        hora=hora_atual(),
        data=data_atual(),
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
# TUTOR INTERATIVO DE LOGÍSTICA (API REST)
# ─────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def api_chat() -> Response:
    """
    Endpoint da API REST para consulta ao Atlas.
    Recebe um JSON com a pergunta do aluno e retorna a explicação em JSON.
    Não utiliza cookies de sessão (stateless), respeitando o limite de 4 KB do Flask.
    """
    dados: Dict[str, Any] = request.get_json(silent=True) or {}
    pergunta = str(dados.get("pergunta", "")).strip()

    res = responder_duvida_logistica(pergunta)
    return jsonify(res)


# ─────────────────────────────────────────────
# TRATAMENTO DE ERROS E SEGURANÇA (HANDLERS GLOBAIS)
# ─────────────────────────────────────────────
@app.errorhandler(404)
def erro_404(e: Any) -> Response:
    """Trata erros 404 redirecionando para a página inicial com mensagem amigável."""
    flash("⚠️ Página não encontrada. Você foi redirecionado para o Início.", "warning")
    return redirect(url_for("inicio"))


@app.errorhandler(500)
def erro_500(e: Any) -> Response:
    """Trata erros internos de servidor (500) sem exibir stack trace ao usuário."""
    flash("⚠️ Ocorreu um erro interno na aplicação. Nossa equipe foi notificada.", "danger")
    return redirect(url_for("inicio"))


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
