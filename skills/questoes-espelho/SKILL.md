---
name: questoes-espelho
description: Criar, revisar e corrigir questões de simulados a partir de espelhos de provas ou de uma planilha de encomenda, com instruções por item, revisão independente e processamento automático de lotes. Use também para continuar esses lotes; não para apenas resolver uma questão enviada pelo aluno.
metadata:
  version: "1.3.0"
---

# Questões-espelho

Produzir questões com a cobrança, arquitetura e apresentação do espelho, incorporando o conteúdo e as exceções pedidos pelo usuário. Aceitar uma imagem, PDF, DOCX, texto, referência identificável, seleção de planilha ou lote. O usuário pode enviar só o espelho; não exigir um formulário, novos nomes de colunas ou comandos por microlote. Tratar o espelho e o perfil da prova como evidências próprias daquele exame: regras de SSA, ENEM, Fuvest ou outra banca não são intercambiáveis sem verificação.

## Entrada e autorização

- Inferir prova/etapa/edição e restrições a partir do material e do projeto ativo; confirmar a referência por leitura real. Se edição ou número não forem identificáveis em uma imagem completa, registrar espelho avulso com arquivo/hash/página e ID local; não inventar metadados nem bloquear autoria por rótulo bibliográfico dispensável. Perguntar apenas quando a ambiguidade muda o conteúdo ou o espelho a usar.
- Sem tema substituto: escolher situação própria no mesmo conteúdo/competência e nível do espelho. Sem pedido de formato: entregar a questão completa, resolução e gabarito separados do material estudantil, usando o padrão do projeto quando estabelecido.
- Precedência: pedido atual específico > instrução específica da linha selecionada > restrições do lote > ficha do espelho > perfil da prova > regras comuns. Uma mudança autorizada vale no eixo indicado; não apaga restrições independentes.
- “Mais difícil/mais fácil” autoriza ajustar a exigência e registrar a diferença pretendida. Trabalhar por decisões, integração, pistas e percurso; não por texto inchado, números maiores ou conteúdo fora do programa. Não alegar dificuldade idêntica ao espelho quando houve mudança deliberada.
- Autoria, revisão e correção interna necessárias fazem parte da encomenda. Executar todos os microlotes sem exigir “continue” ou aprovação a cada um. Preservar uma pausa pedida expressamente pelo usuário. Um pedido completo de geração e entrega autoriza as exportações nele incluídas; não ressuscitar uma aprovação antiga já satisfeita ou substituída pelo pedido atual.
- Não alterar o controle de encomenda. Criar/atualizar a fonte editorial e suas saídas conforme o pedido. Pedido de análise ou diagnóstico isolado não autoriza reescrever questões existentes.
- Adjetivos comparativos ou relativos em feedback — como “sólido”, “melhor”, “mais próximo” ou “menos pior” — descrevem posição dentro do conjunto analisado. Só registrar aprovação, prontidão ou uso como modelo quando o usuário disser isso explicitamente.

## Carregar apenas o necessário

- Entrada por planilha: ler [entrada-planilha.md](references/entrada-planilha.md) e usar a skill Spreadsheets disponível.
- Qualquer elaboração/revisão: ler [criterios-editoriais.md](references/criterios-editoriais.md).
- Identificação/adaptação da prova: ler [perfis-de-prova.md](references/perfis-de-prova.md). SSA/UPE também exige [ssa-upe.md](references/ssa-upe.md). Para outra prova, consultar ou construir seu perfil no repertório com a skill analisar-provas, fundamentado nos espelhos/edital fornecidos, sem transportar números, tipografia, paginação ou cinco alternativas do SSA por padrão.
- Consultar o [repertório de provas](../analisar-provas/references/repertorio/index.json) por exame/etapa/edição. Sem perfil suficiente, aplicar [analisar-provas](../analisar-provas/SKILL.md); análise isolada não inicia autoria. PAES/Unimontes: usar [acesso ao perfil](references/paes-unimontes.md), sem transformar pedidos de lote em regras da banca.
- Imagens: aplicar [revisão visual](references/revisao-visual.md). Feedbacks, dificuldade e restaurações: aplicar [contrato e versões](references/contrato-e-versoes.md).
- Lotes, retomadas ou delegação: ler [lotes-e-revisao.md](references/lotes-e-revisao.md). Ao usar subagentes, aplicar os contratos de [papeis-de-agentes.md](references/papeis-de-agentes.md), com contexto mínimo e responsabilidades separadas.
- Exportação `.qpack`: ler [qpack-semantica.md](references/qpack-semantica.md). Para o Formatador de Simulados do usuário, ler também [formatador-local.md](references/formatador-local.md), que identifica o executável 0.3.1 e os comandos locais.
- Escolha ou economia de modelo: ler [modelos.md](references/modelos.md). Herdar modelo e nível escolhidos pelo usuário; não trocar a configuração global. A tabela é recomendação, não benchmark deste projeto.

## Executar

1. Identificar entrada, fonte editorial, prova/perfil aplicável, itens selecionados e dependências. Para lote, planejar distribuição de operações, suportes e posições de gabarito antes da redação. Um item avulso não exige matriz de 90 posições.
2. Ler cada espelho por inteiro, incluindo continuações. Registrar arquitetura, função dos estímulos, comando, operação, percurso mínimo, dificuldade/trabalhosidade, representação das respostas e padrão das alternativas. Distinguir o que pertence à banca do que é circunstancial daquele item e da exceção autorizada.
3. Conceber a cobrança e uma resolução correta. Selecionar fontes/visuais compatíveis; ajustar a concepção se a fonte disponível não sustenta o item. Construir distratores a partir de erros plausíveis distintos. Testar se texto, figura, título, fórmula ou opção revelam a resposta antes da operação cobrada. Registrar uma solução verificável e justificativas breves, sem exigir exposição de raciocínio privado.
4. Redigir o item estudantil e revisar sua necessidade de dados/estímulos. Aplicar humanizer ao texto autoral quando útil, respeitando conteúdo, termos técnicos, citações e forma da banca. Não humanizar excertos atribuídos a terceiros.
5. Encaminhar versão estudantil a um revisor independente sem gabarito/solução do autor. Usar contexto novo e o menor pacote suficiente. Depois da solução independente, confrontar gabaritos, espelho, dificuldade solicitada, atalhos e distratores. Corrigir e repetir apenas as verificações afetadas.
6. Consolidar na fonte editorial. Um único responsável grava essa fonte; subagentes entregam propostas por item e evidências. Atualizar o registro de progresso depois de cada grupo concluído.
7. Para exportação pedida, gerar a partir da fonte consolidada e verificar a saída real. Utilizar as skills Documents/PDF/Spreadsheets e os perfis do formatador quando aplicáveis. Uma prévia própria não comprova compatibilidade com o formatador de destino.
8. Revisar o conjunto: cobertura de todos os itens, dependências, repetição de operações, distribuição da carga e dos gabaritos, diversidade/autenticidade de fontes e suportes, pistas recorrentes e uniformidade visual indevida. Entregar arquivos e relatório conciso de exceções/pendências. Só declarar concluído o que foi efetivamente verificado; validade técnica não equivale a qualidade editorial.

## Revisão e estado

- Preferência explícita deste projeto: não repetir imagens entre questões nem reutilizar imagens de questões antigas, incluindo espelhos e produções anteriores. Um estímulo compartilhado expressamente autorizado é um objeto único ligado aos itens dependentes. Aplicar a autores, revisores e exportação; detalhes em [criterios-editoriais.md](references/criterios-editoriais.md). Manter uma imagem na revisão da mesma questão não é reutilizá-la em outra questão.

- Separar correção do conteúdo, qualidade da cobrança, fidelidade ao espelho/exceções, qualidade visual e integridade dos arquivos. Cada resultado aponta para a versão do item e uma evidência verificável.
- Ao mudar dado, comando, alternativa, imagem ou espelho, invalidar as revisões afetadas. Revalidar gabarito após polimento que altere conteúdo. Mudança tipográfica exige conferir layout/vetor.
- Se um defeito se repetir, procurar o mesmo padrão no lote inteiro; corrigir só itens atingidos. Não limitar a revisão ao último microlote.
- Uma questão problemática não paralisa as independentes. Após duas rodadas sem resolver a mesma divergência, mudar de abordagem/revisor; se continuar sem solução confiável, registrá-la como pendente e continuar o restante. Não promover por esgotamento de tentativas.
- Aprovação editorial do usuário é um estado separado da revisão automática. Não inventar aprovação; não exigir confirmação por rotina se a encomenda já autoriza a execução.
- Não promover um item porque foi o melhor de um lote ruim ou recebeu elogio relativo. “Sem erro anulatório”, “solucionável” e “tecnicamente válido” são estados diferentes de “pronto para prova”.

## Economia e continuidade

- Um pedido pode conter 90 itens. Processar internamente em grupos pequenos e continuar autonomamente durante a execução ativa; salvar o estado permite retomar após interrupção. A skill não é um serviço que continua rodando com o app fechado.
- Carregar regras estáveis uma vez e passar aos especialistas somente os itens, referências e restrições pertinentes. Não copiar o histórico completo para cada agente.
- Usar scripts para contagens, vínculos e fingerprints. `scripts/plan_batches.py` planeja grupos; `scripts/review_state.py` prepara pacotes sem campos privados e confere evidências/versionamento. Eles não certificam correção pedagógica.
- Se subagentes não estiverem disponíveis, fazer a conferência em passagem separada e declarar a limitação de independência; não simular que houve outro revisor. Não criar tarefas na barra lateral sem pedido específico.
- Em respostas de progresso, informar avanço e impedimentos úteis. Na entrega, mostrar questões/arquivos, sem despejar rascunhos, matrizes internas ou logs salvo solicitação.
