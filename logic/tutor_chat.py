"""
=============================================================================
  TUTOR INTERATIVO DE LOGÍSTICA (logic/tutor_chat.py) — LogiQ
  Módulo de resposta didática às dúvidas dos alunos sobre termos logísticos
  e processos operacionais de um Centro de Distribuição.
  
  Suporta execução híbrida (API externa de IA via variável de ambiente ou
  motor local de conhecimento para funcionamento 100% gratuito e offline).
=============================================================================
"""
import json
import os
import urllib.error
import urllib.request
from typing import Dict, Any, List, Optional
from config.settings import (
    API_KEY as CONFIG_API_KEY,
    PREFERED_IA_MODEL,
    MAX_OUTPUT_TOKENS,
    TIMEOUT_IA_SEGUNDOS,
)



# Banco de Conhecimento Operacional LogiQ (Palavras-chave e Explicação Didática)
BANCO_CONHECIMENTO_LOGISTICO: Dict[str, Dict[str, str]] = {
    "wms": {
        "titulo": "WMS — Sistema de Gerenciamento de Armazém",
        "texto": (
            "O **WMS** (*Warehouse Management System*) é o sistema computacional que funciona "
            "como o 'cérebro' do Centro de Distribuição. Ele indica onde cada caixa ou palete "
            "deve ser guardado, controla os saldos de estoque e orienta a separação de pedidos em tempo real."
        ),
    },
    "fifo": {
        "titulo": "FIFO / PEPS — Primeiro que Entra, Primeiro que Sai",
        "texto": (
            "No armazém, **FIFO** (*First In, First Out*) ou **PEPS** significa que os produtos "
            "que chegaram primeiro ao galpão devem ser separados e expedidos antes dos mais novos. "
            "Isso garante a rotatividade do estoque e evita encalhe de mercadorias antigas."
        ),
    },
    "fefo": {
        "titulo": "FEFO / PVPS — Primeiro que Vence, Primeiro que Sai",
        "texto": (
            "O **FEFO** (*First Expired, First Out*) ou **PVPS** prioriza a saída dos itens com "
            "a data de validade mais próxima do vencimento. É um padrão obrigatório em armazéns "
            "de alimentos, bebidas, cosméticos e produtos farmacêuticos."
        ),
    },
    "lifo": {
        "titulo": "LIFO / UEPS — Último que Entra, Primeiro que Sai",
        "texto": (
            "O **LIFO** (*Last In, First Out*) ou **UEPS** ocorre em estruturas de empilhamento "
            "blocado (drive-in), onde o último palete colocado é o mais acessível na frente do corredor "
            "e acaba sendo retirado primeiro."
        ),
    },
    "picking": {
        "titulo": "Picking — Separação de Pedidos",
        "texto": (
            "O **Picking** é a etapa de separação de pedidos. O operador segue uma lista do WMS "
            "(ou leitor de código de barras) e percorre os endereços das prateleiras para coletar "
            "os produtos exatos na quantidade solicitada para montar o pedido do cliente."
        ),
    },
    "5s": {
        "titulo": "Metodologia 5S — Organização e Limpeza",
        "texto": (
            "O **5S** é o programa de gestão de qualidade e organização do armazém baseado em 5 sensos: "
            "Utilização (Seiri), Organização (Seiton), Limpeza (Seiso), Padronização (Seiketsu) e Disciplina (Shitsuke). "
            "No galpão, ele garante um ambiente limpo, seguro, sem obstáculos nos corredores e com rotas de fluxo desimpedidas."
        ),
    },

    "recebimento": {
        "titulo": "Recebimento — Chegada de Cargas",
        "texto": (
            "O **Recebimento** é a porta de entrada do Centro de Distribuição. Envolve o agendamento "
            "de docas, o descarregamento das carretas, a conferência física e fiscal das Notas Fiscais "
            "e a etiquetagem para entrada oficial no estoque."
        ),
    },
    "estoque": {
        "titulo": "Estoque — Armazenagem e Endereçamento",
        "texto": (
            "A área de **Estoque** armazena os produtos de forma estruturada. Cada porta-paletes "
            "é organizado por **Ruas, Módulos, Níveis e Posições** (código de endereço), permitindo "
            "localizar qualquer caixa em segundos com acurácia."
        ),
    },
    "expedicao": {
        "titulo": "Expedição — Embalagem e Embarque",
        "texto": (
            "A **Expedição** é a última etapa do CD. Os pedidos separados são conferidos, embalados, "
            "agrupados por destino em um **Romaneio de Carga** e embarcados nos caminhões para transporte."
        ),
    },
    "inventario": {
        "titulo": "Inventário e Acurácia de Estoque",
        "texto": (
            "O **Inventário** é a contagem física das peças nas prateleiras. A **Acurácia de Inventário (IRA)** "
            "mede a exatidão entre o saldo físico real e o saldo registrado no WMS. O objetivo de todo galpão "
            "é manter 100% de acurácia!"
        ),
    },
    "5s": {
        "titulo": "Metodologia 5S no Galpão",
        "texto": (
            "O **5S** é o padrão de organização, limpeza e disciplina operacional. No armazém, a regra de ouro é: "
            "*'Um lugar para cada item, e cada item em seu lugar'*, prevenindo acidentes e acelerando o fluxo."
        ),
    },
    "otif": {
        "titulo": "OTIF — On-Time, In-Full",
        "texto": (
            "O **OTIF** (*On-Time, In-Full*) é o principal indicador de nível de serviço logístico. "
            "Mede a porcentagem de pedidos que foram entregues no prazo combinado (**On-Time**) e com "
            "todos os itens corretos e sem avarias (**In-Full**)."
        ),
    },
    "doca": {
        "titulo": "Docas de Carga e Descarga",
        "texto": (
            "As **Docas** são as plataformas niveladas na frente do galpão onde os caminhões e carretas "
            "estacionam para que as empilhadeiras ou transpaletes realizem a carga ou descarga com segurança."
        ),
    },
    "documentos_fiscais": {
        "titulo": "Documentos Fiscais no Armazém — NF-e, DANFE, CT-e e Romaneio",
        "texto": (
            "No Centro de Distribuição, toda movimentação de carga exige **documentação fiscal e operacional** correta:\n\n"
            "• **NF-e (Nota Fiscal Eletrônica):** Documento digital fiscal que comprova a operação de compra/venda, descrevendo impostos, itens e quantidades.\n"
            "• **DANFE:** Representação gráfica simplificada da NF-e impressa em papel, que acompanha a carga física e contém o código de barras para bipagem no Recebimento.\n"
            "• **CT-e (Conhecimento de Transporte Eletrônico):** Documento emitido pela transportadora cobrindo o frete e a prestação de serviço de transporte.\n"
            "• **Romaneio / Manifesto:** Lista operacional detalhada dos volumes e pedidos carregados em cada veículo na Expedição."
        ),
    },
    "cross_docking": {
        "titulo": "Cross-Docking — Transbordo Direto",
        "texto": (
            "O **Cross-Docking** é uma técnica de distribuição em que as cargas que chegam ao Recebimento são separadas e "
            "enviadas diretamente para as docas de Expedição (ou com estocagem mínima de poucas horas), eliminando custos de armazenagem de longo prazo."
        ),
    },
    "unitizacao": {
        "titulo": "Paletização, Strech e Unitização",
        "texto": (
            "A **Unitização** agrupa várias caixas ou embalagens menores em uma única unidade de carga maior, como o **Palete PBR**. "
            "A aplicação de filme stretch garante a estabilidade do palete para movimentação com empilhadeira e evita avarias."
        ),
    },
    "empilhadeira": {
        "titulo": "Equipamentos de Movimentação — Empilhadeiras e Transpaletes",
        "texto": (
            "As **Empilhadeiras** (elétricas ou a combustão) e **Transpaleteiras** são equipamentos essenciais de movimentação de carga. "
            "Sua operação exige treinamento obrigatório de segurança (**NR-11**), respeito à capacidade de carga do garfo e velocidade controlada."
        ),
    },
    "epi_seguranca": {
        "titulo": "Segurança no Galpão e EPIs Obrigatórios",
        "texto": (
            "No Centro de Distribuição, o uso de **EPIs (Equipamentos de Proteção Individual - NR-6)** é obrigatório: "
            "bota de segurança com biqueira (contra quedas de paletes), colete refletivo (para visibilidade perante empilhadeiras), luvas e capacete."
        ),
    },
    "logistica_reversa": {
        "titulo": "Logística Reversa e Tratamento de Devoluções",
        "texto": (
            "A **Logística Reversa** gerencia o retorno de mercadorias ao CD por devolução do cliente, avaria, recall ou validade. "
            "O item devolvido passa por inspeção de qualidade para decidir se retorna ao estoque, vai para conserto ou é descartado."
        ),
    },
    "codigo_barras_rfid": {
        "titulo": "Código de Barras, EAN-13, DUN-14 e RFID",
        "texto": (
            "A identificação de mercadorias no WMS ocorre via **Código de Barras (EAN-13 para unitários, DUN-14 para caixas)** ou **Etiquetas RFID**. "
            "A bipagem óptico-eletrônica elimina erros humanos de digitação e acelera a conferência no Recebimento e Picking."
        ),
    },
    "curva_abc": {
        "titulo": "Curva ABC de Estoque (Pareto 80/20)",
        "texto": (
            "A **Curva ABC** classifica os itens de estoque por importância e volume de saída:\n\n"
            "• **Curva A:** Itens de altíssimo giro (ficam nas posições mais baixas e próximas à Expedição para coleta rápida).\n"
            "• **Curvas B e C:** Itens de médio e baixo giro, alocados nos níveis superiores ou fundos dos corredores."
        ),
    },
    "lead_time": {
        "titulo": "Lead Time — Tempo de Ciclo Operacional",
        "texto": (
            "O **Lead Time Logístico** é o tempo total gasto desde o momento em que o cliente faz o pedido até a chegada do produto "
            "em suas mãos. No armazém, trabalhamos para reduzir ao máximo o lead time de separação e expedição."
        ),
    },
    "conferencia_cega": {
        "titulo": "Conferência Cega no Recebimento",
        "texto": (
            "A **Conferência Cega** é o método onde o conferente conta as caixas e bipa os produtos no Recebimento **sem ter acesso** "
            "às quantidades escritas na nota fiscal. O sistema WMS compara a contagem e acusa divergências automaticamente."
        ),
    },
    "kanban_jit": {
        "titulo": "Just in Time (JIT) e Kanban",
        "texto": (
            "O **Just in Time (JIT)** busca produzir ou comprar apenas o necessário, no tempo exato da demanda, sem estoques parados. "
            "O **Kanban** usa cartões ou sinais visuais para autorizar a reposição de itens assim que atingem o estoque mínimo."
        ),
    },
    "kpi_indicadores": {
        "titulo": "KPIs e Indicadores de Desempenho do CD",
        "texto": (
            "Os principais **KPIs Logísticos** do armazém são:\n\n"
            "• **Acurácia de Estoque (IRA):** Exatidão do inventário.\n"
            "• **OTIF:** Entregas completas e no prazo.\n"
            "• **Tempo de Permanência em Doca:** Rapidez na carga/descarga.\n"
            "• **Produtividade de Picking:** Linhas ou itens separados por operador/hora."
        ),
    },
    "etapas_cd": {
        "titulo": "As 4 Grandes Etapas do Centro de Distribuição",
        "texto": (
            "O fluxo contínuo de um CD se divide em 4 etapas conectadas:\n\n"
            "1. **Recebimento:** Chegada, agendamento de doca, conferência cega e etiquetagem.\n"
            "2. **Estoque:** Alocação nos porta-paletes (Rua-Módulo-Nível-Posição).\n"
            "3. **Picking:** Separação dos itens do pedido via lista/bipagem.\n"
            "4. **Expedição:** Conferência final, embalagem, romaneio e carregamento nos caminhões."
        ),
    },
    "logiq": {
        "titulo": "Sobre o Sistema LogiQ",
        "texto": (
            "O **LogiQ** é um Centro de Treinamento Logístico interativo criado para qualificar alunos e "
            "trabalhadores operacionais. Explore as 4 etapas do galpão, registre uma simulação em "
            "**Situação** e teste seus conhecimentos no **Quiz**!"
        ),
    },
}




def _buscar_resposta_local(pergunta: str) -> str:
    """
    Busca uma explicação didática local baseada nas palavras-chave presentes
    na pergunta do aluno.

    Args:
        pergunta (str): Texto da dúvida enviada pelo usuário.

    Returns:
        str: Explicação formatada com título e texto em português simples.
    """
    texto_norm = pergunta.lower().strip()

    # Mapeamento estendido de variações sintáticas para os termos chave
    sinonimos: Dict[str, List[str]] = {
        "documentos_fiscais": [
            "nota fiscal", "nf", "nfe", "nf-e", "danfe", "cte", "ct-e",
            "documento", "documentos", "imposto", "romaneio", "manifesto",
            "conferir nota", "nota", "fiscais", "fiscal", "faturamento", "xml"
        ],
        "empilhadeira": [
            "empilhadeira", "empilhadeiras", "transpalete", "transpaleteira",
            "paleteira", "operador de empilhadeira", "nr11", "nr-11", "garfo", "empilhamento"
        ],
        "epi_seguranca": [
            "epi", "epis", "segurança", "seguranca", "bota", "capacete", "colete",
            "nr6", "nr-6", "acidente", "acidentes", "proteção", "protecao"
        ],
        "logistica_reversa": [
            "reversa", "devolução", "devolucao", "devoluções", "devolucoes",
            "avaria", "avariado", "recall", "retorno", "sac", "troca"
        ],
        "codigo_barras_rfid": [
            "código de barras", "codigo de barras", "barras", "bipagem", "bipar",
            "leitor", "ean", "ean13", "dun14", "rfid", "etiqueta", "qr", "qrcode"
        ],
        "curva_abc": [
            "curva abc", "abc", "curva a", "curva b", "curva c",
            "pareto", "80/20", "giro", "alto giro", "rotatividade"
        ],
        "lead_time": [
            "lead time", "leadtime", "tempo de ciclo", "tempo de entrega",
            "tempo de pedido", "prazo de entrega"
        ],
        "conferencia_cega": [
            "cega", "conferência cega", "conferencia cega", "contagem cega",
            "sem nota", "conferência de entrada", "conferencia de entrada"
        ],
        "kanban_jit": [
            "jit", "just in time", "kanban", "enxuto", "lean", "estoque mínimo", "reposição automática"
        ],
        "kpi_indicadores": [
            "kpi", "kpis", "indicador", "indicadores", "meta", "metas",
            "desempenho", "produtividade", "permanência", "ocupação", "ocupacao"
        ],
        "etapas_cd": [
            "etapa", "etapas", "passo a passo", "fluxo", "como funciona",
            "setores", "setor", "centro de distribuição", "centro de distribuicao", "galpão", "galpao", "armazém general", "cd general", "logística"
        ],
        "wms": ["wms", "sistema", "software", "programa"],
        "fifo": ["fifo", "peps", "primeiro que entra", "ordem de entrada"],
        "fefo": ["fefo", "pvps", "vencimento", "validade", "primeiro que vence"],
        "lifo": ["lifo", "ueps", "último que entra", "ultimo que entra"],
        "picking": ["picking", "separação", "separacao", "separar", "coleta"],
        "recebimento": ["recebimento", "receber", "chegada", "conferir carga", "descarregamento"],
        "estoque": ["estoque", "armazém", "armazem", "rua", "estante", "endereçamento", "enderecamento", "posição"],
        "expedicao": ["expedição", "expedicao", "expedir", "embarque", "carregamento", "entrega", "despacho"],
        "inventario": ["inventário", "inventario", "acurácia", "acuracia", "ira", "contagem", "auditoria"],
        "5s": ["5s", "organização", "organizacao", "limpeza", "ordem", "seiri", "seiton"],
        "otif": ["otif", "indicador de serviço", "serviço logístico", "on time", "in full"],
        "doca": ["doca", "plataforma", "caminhão", "caminhao", "carreta", "baia"],
        "cross_docking": ["cross docking", "cross-docking", "transbordo", "passagem direta"],
        "unitizacao": ["embalagem", "strech", "filme", "palete", "paletização", "paletizacao", "unitização", "unitizacao", "volume"],
        "logiq": ["logiq", "curso", "treinamento", "ajuda", "sobre"],
    }


    termos_encontrados: List[str] = []
    for chave, lista_sinonimos in sinonimos.items():
        if any(sin in texto_norm for sin in lista_sinonimos):
            termos_encontrados.append(chave)

    if not termos_encontrados:
        return (
            "Olá! Sou o **Atlas** ⚡. Posso te explicar com exemplos práticos qualquer conceito ou procedimento do nosso Centro de Distribuição:\n\n"
            "• **Documentos & Faturamento:** NF-e, DANFE, CT-e, Romaneio e Manifesto\n"
            "• **Sistemas & Métodos:** WMS, FIFO, FEFO, LIFO, 5S, Cross-Docking\n"
            "• **Setores do Galpão:** Recebimento, Estoque, Picking, Expedição\n"
            "• **Indicadores & Operação:** Inventário, Acurácia (IRA), OTIF, Paletização e Docas\n\n"
            "Sobre qual tema operacional você gostaria de saber mais?"
        )


    respostas: List[str] = []
    for chave in termos_encontrados[:2]:  # Limita até 2 conceitos por resposta para concisão
        dados = BANCO_CONHECIMENTO_LOGISTICO.get(chave)
        if dados:
            respostas.append(f"### {dados['titulo']}\n\n{dados['texto']}")

    return "\n\n---\n\n".join(respostas)


PROMPT_DIDATICO_SISTEMA = (
    "Você é o Atlas, o especialista operacional didático de um Centro de Distribuição (CD).\n"
    "Sua missão é explicar conceitos de logística de forma simples, prática e direta para alunos e operadores.\n"
    "REGRAS IMPORTANTES:\n"
    "1. Seja conciso e direto ao ponto. NUNCA corte ou deixe uma frase incompleta. Conclua totalmente todas as seções.\n"
    "2. Não use siglas ou termos em inglês sem antes explicar em português simples.\n"
    "3. OBRIGATORIAMENTE estruture sua resposta com estes 3 tópicos curtos e objetivos:\n"
    "### O que é\n"
    "Definição clara e simples do conceito (2 a 3 frases).\n\n"
    "### Exemplo no Galpão\n"
    "Um caso prático curto do dia a dia no armazém (recebimento, pallets, bipagem, picking, 5S ou expedição).\n\n"
    "### 💡 Dica do Atlas\n"
    "Uma dica rápida de ouro para evitar erros na operação ou melhorar o indicador."
)




def _consultar_ia_generativa(pergunta: str, api_key: str) -> Optional[str]:
    """
    Realiza chamada HTTP leve (sem bibliotecas externas pesadas) para API generativa de IA.
    Suporta formato REST padrão do Google Gemini (AIza...) e formato compatível OpenRouter/Groq.
    Em caso de falha de rede, timeout ou erro de chave, retorna None para acionar o fallback.

    Args:
        pergunta (str): Dúvida do aluno a ser explicada.
        api_key (str): Chave da API externa de IA.

    Returns:
        Optional[str]: Resposta gerada pela IA ou None em caso de indisponibilidade.
    """
    try:
        if api_key.startswith("AIza"):
            # Chave Google Gemini: Prioriza o modelo Flash rápido e leve
            modelos = [
                PREFERED_IA_MODEL,
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-2.5-flash-lite",
            ]
            modelos_unicos = list(dict.fromkeys(modelos))
            for mode in modelos_unicos:
                try:
                    url = (
                        "https://generativelanguage.googleapis.com/v1beta/models/"
                        f"{mode}:generateContent?key={api_key}"
                    )
                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {
                                        "text": f"{PROMPT_DIDATICO_SISTEMA}\n\nPERGUNTA DO ALUNO:\n{pergunta}"
                                    }
                                ]
                            }
                        ],
                        "generationConfig": {
                            "temperature": 0.3,
                            "maxOutputTokens": MAX_OUTPUT_TOKENS,
                        },
                    }

                    data = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(
                        url,
                        data=data,
                        headers={"Content-Type": "application/json"},
                    )
                    with urllib.request.urlopen(req, timeout=TIMEOUT_IA_SEGUNDOS) as response:
                        result = json.loads(response.read().decode("utf-8"))
                        parts = result["candidates"][0]["content"]["parts"]
                        if parts:
                            return parts[-1]["text"]
                except Exception:
                    continue
            return None
        else:
            # Chave Groq / OpenRouter / OpenAI compatível (gsk_ ou AQ.)
            url = os.getenv(
                "API_URL", "https://api.groq.com/openai/v1/chat/completions"
            )
            model = os.getenv("API_MODEL", "llama-3.1-8b-instant")
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": PROMPT_DIDATICO_SISTEMA},
                    {"role": "user", "content": pergunta},
                ],
                "max_tokens": MAX_OUTPUT_TOKENS,
                "temperature": 0.3,
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT_IA_SEGUNDOS) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
    except Exception:
        return None



def responder_duvida_logistica(pergunta: str) -> Dict[str, Any]:
    """
    Processa a pergunta do aluno e retorna uma resposta didática clara.
    Utiliza de forma híbrida: se houver chave 'API_KEY' ou 'GEMINI_API_KEY' configurada,
    consulta a API de inteligência artificial em tempo real. Se não houver chave ou
    ocorrer erro de rede, recorre automaticamente ao banco de conhecimento LogiQ.

    Args:
        pergunta (str): Texto da mensagem digitada pelo aluno.

    Returns:
        Dict[str, Any]: Dicionário contendo 'resposta' (str) e 'origem' (str).
    """
    pergunta_limpa = pergunta.strip()
    if not pergunta_limpa:
        return {
            "resposta": "Por favor, digite uma dúvida sobre logística para que eu possa te ajudar!",
            "origem": "logiq_didatico",
        }

    # Verifica se há chave de API externa configurada no ambiente (Render, local ou em settings.py)
    api_key: Optional[str] = (
        os.getenv("API_KEY") or os.getenv("GEMINI_API_KEY") or CONFIG_API_KEY
    )
    if api_key and len(api_key) > 5:
        resposta_ia = _consultar_ia_generativa(pergunta_limpa, api_key)
        if resposta_ia:
            return {
                "resposta": resposta_ia,
                "origem": "logiq_api",
            }

    resposta_texto = _buscar_resposta_local(pergunta_limpa)
    return {
        "resposta": resposta_texto,
        "origem": "logiq_didatico",
    }

