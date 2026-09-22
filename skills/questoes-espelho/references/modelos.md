# Modelos, raciocínio e uso

Verificação: 06/09/2026. Fontes oficiais pesquisadas e abertas; estas recomendações não resultam de benchmark do projeto. Revalidar disponibilidade, controles e preços quando o usuário solicitar nova escolha ou houver mudança no ambiente.

## Política permanente

- Herdar, por padrão, o modelo e o raciocínio escolhidos pelo usuário para a tarefa. A skill não altera a configuração global nem substitui modelos silenciosamente.
- A tabela de perfis abaixo é opcional: aplicá-la quando o usuário adotar esse perfil ou autorizar sua seleção. Registrar o perfil efetivamente usado no manifesto do lote.
- Antes de definir um override, conferir modelos e esforços aceitos pelas ferramentas atuais. Se uma combinação não estiver disponível, informar a limitação; manter a configuração herdada quando ela puder executar o trabalho, sem inventar equivalências.
- O contexto permitido, as ferramentas e a disponibilidade no app dependem do ambiente. Não inferir esses controles somente a partir do catálogo da API. [Modelos no app](https://learn.chatgpt.com/docs/models).
- Modelo mais capaz ou esforço maior não elimina a necessidade de resolução independente, conferência do espelho, fontes, distratores e inspeção do artefato exportado.

## Fatos verificados

| Modelo | Posicionamento oficial | Esforços documentados na API | Preço API padrão de entrada/saída por 1 milhão de tokens* |
|---|---|---|---|
| [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | Modelo mais capaz, para trabalho complexo de ponta a ponta | low, medium, high, xhigh, max | US$ 10 / US$ 50 |
| [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) | Modelo principal da família 5.6 para trabalho profissional complexo | none, low, medium, high, xhigh, max | US$ 4 / US$ 20 |
| [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) | Equilíbrio entre capacidade e custo | none, low, medium, high, xhigh, max | US$ 2 / US$ 12 |
| [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) | Trabalho de alto volume sensível a custo | none, low, medium, high, xhigh, max | US$ 0,20 / US$ 1,20 |

*Fotografia da documentação na data acima; não é orçamento por questão. Cache, tamanho do contexto, modo de processamento e ferramentas podem alterar cobrança. Sol informa preço promocional disponível pelo menos até 21/11/2026 em sua página.

Os quatro catálogos acima documentam janela API de 1.050.000 tokens e saída máxima de 128.000. Isso não garante que o app exponha a mesma janela. Astra e Sol documentam cobrança API maior para entradas acima de 272 mil tokens: 2× entrada e 1,5× saída para a requisição inteira. Consultar suas páginas antes de estimar custo.

O app recomenda usar o menor esforço que entregue o resultado necessário: Medium equilibra velocidade/profundidade; High e Extra High servem a trabalho difícil com várias etapas, fontes ou decisões. Max amplia o raciocínio para os problemas mais difíceis; Ultra envolve subagentes. A documentação diz que a maioria das tarefas não precisa de Max ou Ultra. [Escolha de esforço](https://learn.chatgpt.com/docs/models#pick-a-reasoning-effort).

Não tratar Ultra do app como um valor universal de `reasoning.effort` da API. As listas da tabela não incluem Ultra; a ferramenta e o cliente em uso determinam os controles válidos.

## Perfil inicial sugerido — inferência para este projeto

Para um perfil com um único modelo, começar com **Astra high**, se disponível e escolhido pelo usuário. É uma escolha inicial orientada à qualidade: este fluxo combina interpretação de espelho, conteúdo disciplinar, elaboração de distratores e julgamento de versões. A documentação sustenta o tipo de uso, mas não prova que high supere medium em todas as questões.

**Astra medium** é candidato para tarefas já delimitadas e operações rotineiras. Antes de adotá-lo na autoria ou revisão final, comparar uma amostra representativa com o perfil inicial. Não anunciar redução “sem perda de qualidade” antes dessa verificação; ausência de falhas na amostra também não é garantia futura.

O lote Q1–Q10/Q71–Q80 auditado em setembro de 2026 não é amostra aprovada: ter itens “mais próximos do padrão” ou “menos piores” não calibra um modelo. Até existir amostra explicitamente aprovada pelo usuário e pelas verificações editoriais, manter **Astra high** como referência para leitura de espelho, autoria e revisão final. Testes com configuração mais econômica devem ocorrer em cópia isolada e não substituir a referência automaticamente.

| Papel | Configuração opcional inicial | Condição de uso |
|---|---|---|
| Coordenador, leitor do espelho e revisão final | Astra high | Várias restrições, fontes e decisões editoriais; pode acumular coordenação e leitura para evitar duplicação |
| Autor de itens enquanto não houver amostra aprovada | Astra high | Padrão conservador após a auditoria; usar contratos curtos por grupo e revisão independente |
| Autor de itens com contrato e amostra aprovados | Sol high | Candidato a reduzir uso depois de calibrar por disciplina, operação e presença de visual; não inferir aprovação de elogio relativo |
| Auditor de fontes/visuais ou do conjunto | Astra high | Julgamento editorial, autenticidade, função cognitiva e padrões sistêmicos |
| Desempate de cálculo, ambiguidade ou item difícil | Astra xhigh | Escalonamento focal após problema identificado; não ativar para o lote inteiro automaticamente |
| Integração `.qpack`, organização, extração e normalização delimitadas | Terra medium | Quando scripts não resolverem; conteúdo deve estar congelado e os resultados precisam de validação determinística |
| Classificação simples e transformação repetível | Luna low/medium | Somente tarefa com resultado verificável; não decidir gabarito, equivalência cognitiva, qualidade visual ou aprovação editorial |

A recomendação de papéis é inferência de implementação, não uma promessa oficial para o SSA. A orientação oficial distingue Astra para fluxos complexos, Sol para trabalho aberto de maior profundidade, Terra para cotidiano e Luna para tarefas claras e repetíveis. [Guia de modelos](https://learn.chatgpt.com/docs/models#choosing-astra-sol-terra-and-luna).

## Independência e contexto

- Fazer a revisão em um subagente com contexto limpo (`fork_turns="none"`, se esse parâmetro existir na ferramenta atual). Primeiro enviar só a questão estudantil completa e fontes/ativos necessários para resolvê-la, com a versão exata. Depois da solução independente, enviar contrato, espelho e pedido especial. Não herdar justificativas do autor como evidência de aprovação.
- O revisor resolve primeiro sem o gabarito proposto. Depois compara sua conclusão ao gabarito e à solução do autor. Usar o mesmo modelo em contextos separados ainda pode produzir erros semelhantes; exigir evidência verificável.
- Retornar achados, cálculo essencial, suporte utilizado e decisão. Pedir uma solução verificável, sem exigir exposição de raciocínio interno. Evitar devolver toda a exploração ao coordenador.
- Contexto grande não equivale a memória confiável. Manter contrato, decisões, proveniência e estado por item em arquivos curtos; carregar somente o espelho e os estímulos relevantes, incluindo relações compartilhadas.
- A documentação alerta que ruído no contexto pode reduzir confiabilidade; subagentes ajudam a manter exploração fora da conversa principal. [Contexto e subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents#why-subagent-workflows-help).

## Economizar sem suprimir verificações

- Executar com scripts contagens, schema, campos obrigatórios, hashes, links locais e consistência de IDs. Reservar modelo para interpretação e julgamento.
- Processar lotes pequenos por referência comum, preservando estímulos compartilhados. Reabrir a revisão somente quando houver alteração relevante, falha ou pendência; não repetir verificações concluídas sem motivo.
- Delegar trabalho independente e delimitado; evitar vários agentes lendo o mesmo histórico completo ou reescrevendo o mesmo item. Paralelismo pode reduzir espera, mas cada agente acrescenta trabalho de modelo/ferramentas e normalmente aumenta tokens. [Uso de subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- Não usar Max/Ultra por hábito. Aumentar esforço para uma dificuldade identificada dentro do perfil autorizado; reduzir contexto desnecessário antes de reduzir a revisão.
- Medir uso por lote e retrabalho, além de tokens: acerto e unicidade do gabarito, aderência ao espelho, necessidade dos suportes, plausibilidade dos distratores e alterações após revisão. Nenhum perfil está aprovado somente por ser mais barato.

No Codex com conta ChatGPT, o consumo depende do plano, modelo, contexto, raciocínio, ferramentas e cache; tamanho do prompt sozinho não estima o uso. Com chave API, aplicam-se preços da API. Não converter a tabela em “tantas questões por limite do app”, nem confundir tokens com créditos. [Uso e preços do app](https://learn.chatgpt.com/docs/pricing#what-are-the-usage-limits-for-my-plan).

Na API, tokens de raciocínio ocupam contexto e são cobrados como saída mesmo sem aparecerem na resposta. Resposta final curta não demonstra baixo consumo total. [Raciocínio e custos](https://developers.openai.com/api/docs/guides/reasoning#how-reasoning-works).

Ao atualizar esta referência: pesquisar e abrir novamente as páginas oficiais, registrar a data, manter a escolha do usuário e comparar alterações relevantes antes de trocar o perfil. Não fixar nomes de modelos como requisito eterno da skill.
