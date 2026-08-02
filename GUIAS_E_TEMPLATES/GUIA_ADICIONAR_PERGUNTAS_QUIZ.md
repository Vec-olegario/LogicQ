# Guia: Adicionando Perguntas ao Quiz — LogiQ

Bem-vindo ao guia de criação de conteúdo para o módulo de avaliação do **LogiQ — Centro de Treinamento e Simulação Logística**. Este documento explicará como as perguntas são estruturadas no código e fornecerá exemplos e templates para você expandir o banco de dados.

---

## 1. Estrutura de Dados da Pergunta

As perguntas ficam armazenadas em uma lista de dicionários tipados no arquivo `logic/perguntas.py` na constante `BANCO_PERGUNTAS`. Cada dicionário **deve** conter os seguintes campos:

```python
{
    "id": "R04",                 # Identificador único (Setor + Número)
    "topico": "Recebimento",     # "Recebimento", "Estoque", "Picking" ou "Expedição"
    "dificuldade": "Média",      # "Fácil", "Médio" ou "Difícil"
    "pergunta": "Texto da pergunta aqui?",
    "opcoes": [                  # Exatamente 4 opções
        "Opção A",
        "Opção B",
        "Opção C",
        "Opção D"
    ],
    "correta": 1,                # Índice da resposta correta na lista (0=A, 1=B, 2=C, 3=D)
    "explicacao": "Explicação que aparece após o usuário responder."
}
```

---

## 2. Exemplos Adicionais (12 Novas Perguntas)

Aqui estão 12 perguntas extras prontas para copiar e colar no `BANCO_PERGUNTAS`:

### Recebimento
```python
{
    "id": "R04",
    "topico": "Recebimento",
    "dificuldade": "Fácil",
    "pergunta": "O que é uma 'Doca' em um centro de distribuição?",
    "opcoes": [
        "A área de descanso dos funcionários.",
        "A plataforma onde os caminhões encostam para carga e descarga.",
        "O sistema de resfriamento do galpão.",
        "O documento que autoriza a entrada do caminhão."
    ],
    "correta": 1,
    "explicacao": "A doca é a estrutura física (geralmente elevada) que conecta o galpão à carroceria do caminhão, facilitando a movimentação de mercadorias."
},
{
    "id": "R05",
    "topico": "Recebimento",
    "dificuldade": "Médio",
    "pergunta": "Qual a importância da leitura de código de barras (Bipagem) no recebimento?",
    "opcoes": [
        "Apenas para verificar o preço de venda do produto.",
        "Garantir a entrada precisa no WMS, evitando divergências de estoque.",
        "É obrigatório apenas para produtos perecíveis.",
        "Para imprimir a nota fiscal."
    ],
    "correta": 1,
    "explicacao": "A bipagem (scanning) garante que o sistema registre exatamente o SKU e a quantidade física que está entrando no galpão, eliminando erros de digitação."
},
{
    "id": "R06",
    "topico": "Recebimento",
    "dificuldade": "Difícil",
    "pergunta": "No contexto de recebimento, o que é SLA (Service Level Agreement)?",
    "opcoes": [
        "Sistema de Logística Avançada.",
        "Acordo de Nível de Serviço, que define metas de tempo para a descarga de um veículo.",
        "Selo de Limpeza de Armazém.",
        "Software de Leitura Automática."
    ],
    "correta": 1,
    "explicacao": "O SLA define os padrões de performance esperados, como, por exemplo, garantir que todo caminhão seja descarregado em no máximo 2 horas após a chegada."
},
```

### Estoque
```python
{
    "id": "E04",
    "topico": "Estoque",
    "dificuldade": "Fácil",
    "pergunta": "O que significa FIFO?",
    "opcoes": [
        "First In, First Out (Primeiro a Entrar, Primeiro a Sair).",
        "Fast In, Fast Out (Entrada Rápida, Saída Rápida).",
        "First In, Final Out (Primeiro a Entrar, Último a Sair).",
        "Final Inventory For Optimization."
    ],
    "correta": 0,
    "explicacao": "FIFO é a regra onde o lote mais antigo no estoque deve ser o primeiro a ser expedido, essencial para produtos perecíveis."
},
{
    "id": "E05",
    "topico": "Estoque",
    "dificuldade": "Médio",
    "pergunta": "Qual tecnologia usa ondas de rádio para identificar paletes sem necessidade de contato visual (sem bipagem com laser)?",
    "opcoes": [
        "Código de Barras",
        "QR Code",
        "RFID (Radio-Frequency Identification)",
        "Bluetooth"
    ],
    "correta": 2,
    "explicacao": "O RFID usa tags (etiquetas) que emitem sinais de rádio, permitindo a leitura de múltiplos paletes de uma só vez, mesmo à distância e sem linha de visão direta."
},
{
    "id": "E06",
    "topico": "Estoque",
    "dificuldade": "Difícil",
    "pergunta": "O que é inventário rotativo ou cíclico?",
    "opcoes": [
        "Contar todo o estoque do galpão no dia 31 de dezembro.",
        "Contagem contínua de pequenas partes do estoque ao longo do ano, sem parar a operação.",
        "Rodar os paletes de lugar para evitar danos na estrutura.",
        "Inventário feito apenas de produtos devolvidos."
    ],
    "correta": 1,
    "explicacao": "O inventário cíclico dilui a contagem ao longo do ano (ex: contar 5 corredores por dia), garantindo alta acuracidade do estoque sem precisar fechar o CD."
},
```

### Picking
```python
{
    "id": "P04",
    "topico": "Picking",
    "dificuldade": "Fácil",
    "pergunta": "O que é 'Voice Picking'?",
    "opcoes": [
        "Um rádio amador para comunicação.",
        "Sistema onde o operador recebe instruções e confirma coletas por comando de voz via headset.",
        "Gritar as ordens de serviço no galpão.",
        "Tocar alarmes sonoros quando um erro é cometido."
    ],
    "correta": 1,
    "explicacao": "O Voice Picking mantém as mãos e os olhos do operador livres, pois ele interage com o WMS conversando pelo headset."
},
{
    "id": "P05",
    "topico": "Picking",
    "dificuldade": "Médio",
    "pergunta": "Como funciona o sistema 'Put-to-Light'?",
    "opcoes": [
        "Luzes se acendem no chão indicando a rota da empilhadeira.",
        "Luzes se acendem nos escaninhos indicando onde o operador deve COLOCAR o produto separado.",
        "É apenas um sistema de iluminação de emergência.",
        "Usa lasers para cortar caixas."
    ],
    "correta": 1,
    "explicacao": "No Put-to-Light, o operador escaneia um item em lote, e luzes se acendem indicando em qual caixa (pedido de cliente) ele deve colocar aquele item."
},
{
    "id": "P06",
    "topico": "Picking",
    "dificuldade": "Difícil",
    "pergunta": "No Picking Discreto (Discrete Picking), como é feito o trabalho?",
    "opcoes": [
        "Um operador separa um pedido inteiro por vez, percorrendo todo o trajeto necessário.",
        "Vários operadores separam o mesmo pedido simultaneamente.",
        "Os pedidos são separados sem registros no sistema.",
        "As mercadorias são embaladas antes da separação."
    ],
    "correta": 0,
    "explicacao": "É o método mais tradicional e simples: um homem, um pedido. Porém, é o que gera maior deslocamento físico pelo galpão."
},
```

### Expedição
```python
{
    "id": "EX04",
    "topico": "Expedição",
    "dificuldade": "Fácil",
    "pergunta": "O que significa 'Roteirização' na expedição?",
    "opcoes": [
        "Criar a rota de fuga do galpão.",
        "Definir o melhor caminho de entrega para o caminhão economizar tempo e combustível.",
        "Instalar roteadores de internet nas docas.",
        "Limpar a pista de acesso das carretas."
    ],
    "correta": 1,
    "explicacao": "Roteirizar é planejar a sequência ótima de paradas para entrega (ex: cliente A, depois B, depois C), minimizando distâncias e custos."
},
{
    "id": "EX05",
    "topico": "Expedição",
    "dificuldade": "Médio",
    "pergunta": "Qual documento acompanha obrigatoriamente as mercadorias no transporte no Brasil?",
    "opcoes": [
        "Comprovante de residência.",
        "Nota Fiscal Eletrônica (NF-e) / DANFE.",
        "Apenas a fatura do cartão de crédito.",
        "Carta de recomendação."
    ],
    "correta": 1,
    "explicacao": "A NF-e (e o seu documento auxiliar impresso, o DANFE) é obrigatória para atestar a legalidade fiscal do transporte das mercadorias."
},
{
    "id": "EX06",
    "topico": "Expedição",
    "dificuldade": "Difícil",
    "pergunta": "No carregamento, o que é 'Cubagem'?",
    "opcoes": [
        "Pesar o caminhão na balança.",
        "Relação entre o volume ocupado pela carga e o seu peso, visando otimizar o espaço do caminhão.",
        "Medir a temperatura da câmara fria em graus cúbicos.",
        "Contar caixas em formato de cubo."
    ],
    "correta": 1,
    "explicacao": "A cubagem considera altura x largura x profundidade. Um caminhão pode encher o espaço físico com produtos leves (isopor) antes de atingir o limite de peso, ou vice-versa."
}
```

---

## 3. Template Vazio (Copie e Cole)

```python
{
    "id": "___",
    "topico": "___",
    "dificuldade": "___",
    "pergunta": "___",
    "opcoes": [
        "___",
        "___",
        "___",
        "___"
    ],
    "correta": 0,
    "explicacao": "___"
},
```

---

## 4. Dicas para Boas Perguntas Educativas

1. **Evite pegadinhas cruéis:** O foco é educativo. Se o aluno errar, a `explicacao` deve ensiná-lo, não fazê-lo se sentir punido.
2. **Respostas Distratoras Plausíveis:** Evite opções absurdas demais (ex: "Alienigenas pegam o palete"). Crie opções que representem erros comuns no dia a dia do galpão.
3. **Clareza na Explicação:** Aproveite o campo `explicacao` para reforçar a teoria. É o momento de maior aprendizado do usuário.
4. **Alinhamento com o App:** Certifique-se de que o conteúdo da pergunta foi mencionado nos vídeos ou textos da página do setor correspondente.

---

## 5. Como Organizar por Nível de Dificuldade

- **Fácil:** Conceitos básicos e definições diretas (O que é X? O que significa a sigla Y?).
- **Médio:** Aplicação de conceitos, fluxos de processo (Qual a próxima etapa após X? Como funciona a ferramenta Y?).
- **Difícil:** Cenários sistêmicos, exceções, lógica complexa de WMS/Estratégia (Se um problema Z ocorre no inventário rotativo, qual a consequência em Y?).

---

## 6. FAQs (Perguntas Frequentes)

**P: Posso colocar mais ou menos de 4 opções?**
R: O layout atual do `07_Quiz_Avaliacao.py` foi desenhado para comportar bem 4 opções. Se alterar, pode ser necessário ajustar o CSS da grid.

**P: Como mudo a pontuação?**
R: No código Python, cada acerto vale 1 ponto. Você pode alterar a função `responder_pergunta()` para dar pesos diferentes baseados na dificuldade (ex: Fácil=10, Médio=20, Difícil=30).

**P: Posso adicionar imagens nas perguntas?**
R: O dicionário atual aceita apenas texto. Para adicionar imagens, adicione um campo `"imagem": "caminho_da_imagem.jpg"` no dicionário e modifique o bloco de UI no Python usando `st.image(pergunta_atual['imagem'])`.
