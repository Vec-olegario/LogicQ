"""
=============================================================================
  MÓDULO DE WMS DIDÁTICO & PHYGITAL LAB — LogiQ
  Responsabilidade: Gerenciar o fluxo encadeado das caixinhas bipadas entre as
  4 etapas do turno operacional, mantendo rastreabilidade, acurácia e exportação
  de relatórios para avaliação do professor.
=============================================================================
"""
import csv
import io
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Armazenamento em memória do estado dos turnos ativos (respeitando limite de cookie do Flask de 4 KB)
TURNOS_ATIVOS: Dict[str, Dict[str, Any]] = {}


def obter_ou_criar_turno(turno_id: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Recupera um turno operacional ativo pelo ID ou cria um novo turno zerado.

    Args:
        turno_id: Identificador único do turno salvo na sessão do usuário.

    Returns:
        Tuple contendo (turno_id, dicionario_com_dados_do_turno).
    """
    if not turno_id or turno_id not in TURNOS_ATIVOS:
        novo_id = str(uuid.uuid4())[:8]
        TURNOS_ATIVOS[novo_id] = {
            "id": novo_id,
            "aluno": "Aluno(a) LogiQ",
            "inicio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "acertos_picking": 0,
            "erros_picking": 0,
            "itens": [
                # Exemplo didático inicial para o aluno já visualizar no Dashboard
                {
                    "id": "item-101",
                    "codigo": "78910001",
                    "sku": "CX-PARAFUSOS-A",
                    "descricao": "Caixa Parafusos Aço 50mm",
                    "qtd": 20,
                    "fornecedor": "Acme Metalúrgica",
                    "condicao": "Aprovado - Lacrado",
                    "etapa": "estoque",
                    "rua": "01",
                    "prateleira": "A",
                    "nivel": "1",
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "status": "Endereçado na Rua 01",
                },
                {
                    "id": "item-102",
                    "codigo": "78910002",
                    "sku": "CX-ROLL-BEAR",
                    "descricao": "Rolamento Industrial B2",
                    "qtd": 10,
                    "fornecedor": "Rolamentos Brasil",
                    "condicao": "Aprovado - Lacrado",
                    "etapa": "recebimento",
                    "rua": "---",
                    "prateleira": "---",
                    "nivel": "---",
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "status": "Aguardando Endereçamento",
                },
            ],
        }
        return novo_id, TURNOS_ATIVOS[novo_id]

    return turno_id, TURNOS_ATIVOS[turno_id]


def registrar_bipagem_recebimento(
    turno_id: str,
    codigo: str,
    sku: str,
    descricao: str,
    qtd: int,
    fornecedor: str,
    condicao: str,
) -> Dict[str, Any]:
    """
    Registra uma nova mercadoria que deu entrada na doca de Recebimento via código de barras.

    Args:
        turno_id: ID do turno ativo.
        codigo: Código de barras da caixinha (EAN, QR ou SKU).
        sku: Código interno de referência.
        descricao: Descrição simples da caixinha.
        qtd: Quantidade de unidades.
        fornecedor: Nome do fornecedor da carga.
        condicao: Status da conferência física.

    Returns:
        Dicionário representando o novo item criado no turno.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    novo_item = {
        "id": f"item-{len(turno['itens']) + 101}",
        "codigo": codigo.strip() or "SEM-CODIGO",
        "sku": sku.strip() or "SKU-GERAL",
        "descricao": descricao.strip() or "Caixa Logística Didática",
        "qtd": max(1, int(qtd)),
        "fornecedor": fornecedor.strip() or "Fornecedor Padrão",
        "condicao": condicao.strip() or "Aprovado",
        "etapa": "recebimento",
        "rua": "---",
        "prateleira": "---",
        "nivel": "---",
        "timestamp": datetime.now().strftime("%H:%M"),
        "status": "Recebido na Doca",
    }
    turno["itens"].insert(0, novo_item)
    return novo_item


def registrar_enderecamento_estoque(
    turno_id: str,
    item_id: str,
    rua: str,
    prateleira: str,
    nivel: str,
) -> bool:
    """
    Movimenta uma caixinha do Recebimento para um endereço físico no Estoque.

    Args:
        turno_id: ID do turno ativo.
        item_id: Identificador do item na lista do turno.
        rua: Rua ou corredor do porta-paletes na sala.
        prateleira: Número da estante/prateleira.
        nivel: Nível (baixo, médio, alto).

    Returns:
        True se o item foi encontrado e atualizado com sucesso, False caso contrário.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    for item in turno["itens"]:
        if item["id"] == item_id:
            item["rua"] = rua
            item["prateleira"] = prateleira
            item["nivel"] = nivel
            item["etapa"] = "estoque"
            item["status"] = f"Endereçado: R{rua} - P{prateleira} - N{nivel}"
            item["timestamp"] = datetime.now().strftime("%H:%M")
            return True
    return False


def validar_bipagem_picking(
    turno_id: str,
    item_id: str,
    codigo_bipado: str,
    pedido: str,
) -> Tuple[bool, str]:
    """
    Verifica a acurácia da bipagem durante a separação de um pedido (Picking).
    O aluno deve bipar o código de barras exato da caixinha que está na estante.

    Args:
        turno_id: ID do turno ativo.
        item_id: Identificador do item sendo separado.
        codigo_bipado: Código lido pelo leitor de código de barras.
        pedido: Número do pedido simulado.

    Returns:
        Tuple (sucesso: bool, mensagem_feedback: str).
    """
    _, turno = obter_ou_criar_turno(turno_id)
    for item in turno["itens"]:
        if item["id"] == item_id:
            if codigo_bipado.strip() == item["codigo"].strip():
                item["etapa"] = "picking"
                item["status"] = f"Separado p/ Pedido {pedido}"
                item["timestamp"] = datetime.now().strftime("%H:%M")
                turno["acertos_picking"] += 1
                return True, f"✅ Bipagem correta! {item['descricao']} (Cód: {item['codigo']}) separado com sucesso para o Pedido {pedido}."
            else:
                turno["erros_picking"] += 1
                return False, f"❌ Erro de Acurácia: Você bipou o código '{codigo_bipado}', mas o item solicitado era '{item['codigo']}' ({item['descricao']}). Verifique a estante!"
    return False, "⚠️ Item não encontrado na lista operacional do turno."


def registrar_expedicao_item(
    turno_id: str,
    item_id: str,
    doca: str,
    conferente: str,
) -> bool:
    """
    Conclui o ciclo de uma caixinha transferindo-a do Picking para Expedição/Embarque.

    Args:
        turno_id: ID do turno ativo.
        item_id: Identificador do item sendo expedido.
        doca: Número da doca de saída.
        conferente: Nome de quem realizou a conferência cega.

    Returns:
        True se expedido com sucesso, False caso contrário.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    for item in turno["itens"]:
        if item["id"] == item_id:
            item["etapa"] = "expedicao"
            item["status"] = f"Expedido na Doca {doca} ({conferente})"
            item["timestamp"] = datetime.now().strftime("%H:%M")
            return True
    return False


def editar_item_turno(
    turno_id: str,
    item_id: str,
    nova_qtd: int,
    nova_descricao: str,
) -> bool:
    """
    Permite ao aluno ou professor editar quantidade ou descrição de uma caixinha no painel.

    Args:
        turno_id: ID do turno ativo.
        item_id: Identificador do item na lista do turno.
        nova_qtd: Nova quantidade inteira.
        nova_descricao: Nova descrição textual.

    Returns:
        True se o item foi atualizado com sucesso.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    for item in turno["itens"]:
        if item["id"] == item_id:
            item["qtd"] = max(1, int(nova_qtd))
            if nova_descricao.strip():
                item["descricao"] = nova_descricao.strip()
            return True
    return False


def remover_item_turno(turno_id: str, item_id: str) -> bool:
    """
    Remove uma caixinha que foi bipada por erro do turno operacional.

    Args:
        turno_id: ID do turno ativo.
        item_id: Identificador do item na lista do turno.

    Returns:
        True se o item foi removido com sucesso.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    tamanho_orig = len(turno["itens"])
    turno["itens"] = [it for it in turno["itens"] if it["id"] != item_id]
    return len(turno["itens"]) < tamanho_orig


def gerar_csv_turno(turno_id: str) -> str:
    """
    Gera uma planilha CSV com formatação compatível com Excel (incluindo separador
    ponto-e-vírgula e acentuação) pronta para ser avaliada pelo professor.

    Args:
        turno_id: ID do turno ativo.

    Returns:
        String formatada em CSV.
    """
    _, turno = obter_ou_criar_turno(turno_id)
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=";")

    # Cabeçalho Didático de Avaliação
    escritor.writerow(["=========================================================="])
    escritor.writerow(["  RELATÓRIO PRÁTICO DO TURNO — LogiQ (WMS DIDÁTICO)"])
    escritor.writerow(["=========================================================="])
    escritor.writerow(["ID do Turno:", turno["id"]])
    escritor.writerow(["Aluno / Turma:", turno["aluno"]])
    escritor.writerow(["Início do Turno:", turno["inicio"]])
    escritor.writerow(["Data do Relatório:", datetime.now().strftime("%d/%m/%Y %H:%M")])
    escritor.writerow(["Acertos em Picking (Bipagem Correta):", turno["acertos_picking"]])
    escritor.writerow(["Erros em Picking (Falha de Acurácia):", turno["erros_picking"]])
    escritor.writerow([])
    escritor.writerow([
        "CÓD. BARRAS",
        "SKU",
        "DESCRIÇÃO DA MERCADORIA",
        "QTD",
        "ETAPA ATUAL",
        "ENDEREÇO (RUA/PRAT/NIVEL)",
        "STATUS OPERACIONAL",
        "HORA",
    ])

    for item in turno["itens"]:
        endereco = f"R{item['rua']} / P{item['prateleira']} / N{item['nivel']}"
        escritor.writerow([
            item["codigo"],
            item["sku"],
            item["descricao"],
            item["qtd"],
            item["etapa"].upper(),
            endereco,
            item["status"],
            item["timestamp"],
        ])

    return saida.getvalue()
