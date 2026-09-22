# `.qpack`: semântica e perfis

O manifesto informa **o que cada elemento é**; o perfil informa **como ele aparece**. O pacote padroniza a saída, mas não corrige fonte ruim, visual artificial, estímulo que entrega a resposta, dificuldade inadequada ou distratores fracos.

## Estrutura e integridade

- `manifest.json` fica na raiz do `.qpack`; ativos efetivamente usados ficam em `assets/` com caminhos exatos.
- JSON sem comentários ou vírgulas finais; IDs únicos para questões e blocos identificados.
- Registrar o número estudantil em `number` e a referência oficial em campo separado, como `mirror`. Não depender de `start_number` em lotes descontínuos.
- A unidade de entrega segue o pedido do usuário, não os microlotes de produção. Quando pedir um pacote por prova/etapa, consolidar os itens únicos nesse pacote; identificar internamente blocos/cadernos necessários para desambiguar números oficiais repetidos. Manter IDs únicos e o mapa de números por caderno; não criar várias cópias de um item comum nem renumerá-lo sem informar.
- O manifesto preserva a resposta correta; o perfil decide se ela é visível. Exigir a quantidade e o tipo de respostas definidos pelo perfil da prova.
- Usar `runs` para negrito, itálico, títulos de obras, sobrescrito e subscrito. Não usar Markdown, espaços ou tabulações para simular aparência.
- Preferir blocos nativos de texto, fonte, tabela, imagem e colunas. Não converter fórmulas simples ou tabelas em imagem por conveniência.

## Ordem funcional

Reorganizar a entrega “por prova” muda o agrupamento do lote em trabalho, não seu escopo. Não incorporar lotes anteriores já entregues em separado sem pedido explícito de consolidação histórica.

A ordem dos blocos reproduz o item, não um formulário fixo. Não acrescentar título, legenda ou imagem só para preencher uma estrutura. O número deve aparecer no primeiro elemento previsto pelo perfil; não escrevê-lo manualmente se o perfil o gera.

Manter estímulos, fontes, imagens, legendas e comando como elementos separados. Usar o campo superior `prompt` quando esse for o padrão do schema; não duplicar o comando em bloco e campo.

Materiais compartilhados precisam de vínculo explícito. Pela preferência do usuário, imagens aparecem uma única vez, inclusive com paginação de uma questão por página: fazer remissão ao suporte ou manter transcrição suficiente quando a cobrança for verbal. Não duplicar imagens por conveniência de paginação. Imagens de questões antigas e dos espelhos não são ativos para novos itens; aplicar a verificação de identidade/procedência de criterios-editoriais.md.

## Conteúdo versus aparência

Ficam no manifesto: textos, ordem, imagem, tabela, fonte, comando, alternativas, resposta, palavra em itálico, índice, expoente e relação compartilhada.

Ficam no perfil: página, margens, fonte/tamanho globais, alinhamentos, recuos, espaçamentos, formato da numeração e das alternativas, limite de imagens, paginação e visibilidade do gabarito.

Não colocar parâmetros globais de SSA no manifesto nem reutilizar o perfil SSA para outra prova. Criar/selecionar o perfil da banca conforme [perfis-de-prova.md](perfis-de-prova.md).

## Imagens, fontes e tabelas

- Dimensionar cada imagem pela função, respeitando o limite do perfil. Um único percentual para todos os ativos cria artificialidade e pode prejudicar leitura.
- Conferir textos, números, eixos e legendas no tamanho final, não apenas na resolução original.
- Não repetir crédito dentro da arte e em bloco externo. Informações de produção como “peça autoral” não aparecem ao estudante salvo função real no item.
- Usar referência curta visível e metadados completos para rastreabilidade. Não deixar URL azul/sublinhada se o perfil da prova não usa isso.
- Tabelas permanecem estruturadas, com cabeçalhos, unidades e bordas/alinhamentos definidos pelo perfil. Não simular tabela com barras, espaços ou imagem.

## Validação e inspeção

1. Congelar conteúdo e ativos revisados.
2. Gerar manifesto e pacote.
3. Validar schema, IDs, respostas, referências de ativos e regras da prova.
4. Formatar com o perfil explicitamente selecionado.
5. Inspecionar a saída real: numeração, ordem, fontes, runs, recuos, vetores de alternativas, tabelas, escala/legibilidade de imagens, dependências e paginação.
6. Corrigir a fonte editorial, o manifesto ou o perfil; nunca apenas o DOCX derivado.
7. Regenerar e repetir somente as verificações afetadas.

Registrar separadamente: integridade do pacote, compatibilidade com o formatador, qualidade do layout e aprovação editorial. `validate` com código zero comprova apenas as verificações implementadas pelo programa.
