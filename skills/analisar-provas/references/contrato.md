# Contrato de análise v1

`analise.json` é produzido pelo agente, nunca formulário obrigatório para o usuário. Campos:

- `schema_version`: 1; `exam`: nome; `exam_id`: chave do catálogo; `editions`: lista; `status`: partial ou complete; `inventory_complete`: booleano, verdadeiro só após inventário integral dos arquivos declarados.
- `sources`: objetos `id`, `path`, `sha256`, `kind` (exam/program/answer_key), `pages` quando conhecido. Hash é de arquivo real; caminho original preservado mesmo se não mais disponível.
- `expected_occurrences`: lista de chaves de ocorrências identificadas no inventário. Chaves únicas distinguem fonte/caderno, língua e número; não são apenas o número.
- `items`: objetos `id` canônico, `stage`, `subject`, `content`, `operation`, `difficulty` (fácil/média/difícil/indeterminada), `difficulty_reason`, `annulled`, `read_complete`, `visual_required`, `visual_checked`, `occurrences`. Cada ocorrência tem `key`, `source_id`, `pages` (lista de páginas PDF), `number`, `booklet`, `language` quando aplicável. Questão compartilhada aponta várias ocorrências; cada ocorrência pertence a um item.
- `claims`: objetos `id`, `text`, `scope`, `strength` (observed/recurring/hypothesis), `evidence`. Evidências são `item_id` ou `source_id` + `pages`. Recorrência requer múltiplos itens distintos ou uma fonte que documente a contagem; uma fonte de programa sustenta regra formal, não frequência observada. `frequency` opcional: `numerator`, `denominator`, `basis` (unique_items/physical_occurrences ou universo textual explicado), e `population` quando usa subconjunto. Não inventar frequência.
- `limitations`: lista de lacunas, incluindo confiança de leitura e representatividade; `provenance`: registro de análise prévia ou nova; `review`: escopo, revisor e limitações reais.

Completude exige inventário conhecido, ocorrências esperadas presentes e leitura integral de todos os itens, incluindo visuais necessários. Completude documental não transforma uma edição em regra histórica. O validador rejeita `complete` incompatível com cobertura e referências inválidas; `partial` é estado legítimo. Dificuldade indeterminada fica fora da distribuição classificada e deve aparecer como pendência.

Para arquivos grandes, manter texto analítico por disciplina em Markdown separado e apontar seus caminhos no perfil. Não guardar textos integrais de provas dentro deste JSON: fichas, sínteses e referências bastam.

## Diagnóstico editorial complementar

Em novas análises ou revisões dos itens pertinentes, registrar em `items[].editorial_diagnostics` ou em ficha Markdown vinculada: `prior_knowledge`, `provided_information`, `effective_operation`, `curriculum_evidence` (fonte/trecho e se documentada, inferida ou ausente), `length_profile` (componentes separados, vetor de alternativas, unidade/convenção e empates), `information_blocks`, `answer_leakage`, `writing_features`, `preserve`, `vary` e `avoid`. Valores descritivos devem apontar evidências do item; campo não examinado fica explicitamente não avaliado. Esses registros complementam o schema v1 sem invalidar acervos antigos. O validador estrutural atual não certifica sua qualidade nem sua presença; não anunciar retroanálise dos perfis legados sem relê-los.
