# Lotes automáticos e revisão independente

## Entrada simples, execução segmentada

O usuário encomenda o lote inteiro uma vez. Os grupos são unidades internas de trabalho e recuperação; não exigem novos comandos. Planejar todos os itens encomendados e suas dependências antes de redigir, mas carregar no autor apenas o grupo corrente.

Segmentação de autoria/revisão não deve fragmentar a entrega. Gerar arquivos pela unidade pedida (por exemplo, um QPACK por etapa), preservando internamente identidades, estímulos compartilhados e referências de caderno. Auditar no conjunto tanto as letras corretas quanto os padrões de verdade das proposições I–IV.

Ao delegar, usar os contratos de [papeis-de-agentes.md](papeis-de-agentes.md). Os nomes dos agentes podem mudar; as responsabilidades e a separação de contexto permanecem.

Ponto de partida operacional: até 5 itens por grupo, reduzindo para 1–3 quando houver cálculo difícil, muitas fontes, visual complexo ou grande número de restrições. É uma heurística inicial, não limite do modelo nem tamanho cientificamente ótimo. Texto/imagem compartilhado mantém dependentes juntos, mesmo que excedam o alvo. Pode-se produzir em paralelo grupos independentes dentro dos slots disponíveis; preservar contexto e capacidade para revisão.

Um lote de 90 itens independentes em grupos de 5 gera 18 grupos. A revisão cobre cada questão; auditorias do conjunto podem ocorrer a cada aproximadamente 15 itens e ao final. Essas auditorias verificam posições do gabarito, repetição de operações/comandos, concentração de fontes, uniformidade visual, pistas de comprimento/tom e queda de qualidade nas últimas questões. Evitar reler a prova inteira após cada ajuste local.

O planejamento deve manter os números e a ordem estudantil. Se dependências atravessarem posições, agrupar o intervalo necessário. Não separar Q61 e Q62 de um mesmo estímulo só porque pertenciam a lotes diferentes.

Manter uma matriz breve do lote com, por item: espelho, operação, suporte/gênero, fonte prevista, necessidade visual, dificuldade pretendida e posição provisória do gabarito. Ela serve para detectar repetição antes da autoria. A posição é um plano editorial subordinado à correção; nunca forçar conteúdo para preencher uma letra.

## Planejador

O coordenador transforma a entrada natural/planilha em JSON interno; o usuário não preenche JSON. Exemplo:

```json
{
  "max_items": 5,
  "max_effort_units": 8,
  "required_mirror_fields": ["exam", "edition", "question"],
  "items": [
    {"id": "I001", "mirror": {"exam": "prova identificada", "edition": "edição", "question": "número"}, "complexity": "standard", "shared_stimulus_ids": []}
  ]
}
```

Executar `python scripts/plan_batches.py entrada.json --output plano.json` após conferir `--help`. Para SSA identificado, acrescentar `stage` e `day` aos campos necessários conforme o perfil. Para recorte avulso legível, usar identidade por arquivo/hash/página/ID local, configurar os campos realmente necessários e marcar explicitamente a bibliografia não identificada. Não inventar edição para satisfazer o helper.

O resultado informa cobertura, grupos, esforço, dependências acima do limite e metadados ausentes. Esforço é uma classificação de planejamento, não previsão de tokens ou dificuldade psicométrica. Corrigir só os campos cuja ausência impede a execução; seguir com os grupos independentes.

## Estado persistente

Guardar no diretório `work` da tarefa: entrada normalizada, plano, snapshots dos itens, revisões e um estado do lote. A planilha editorial continua autoridade se essa for a fonte escolhida. JSONs de item são snapshots de revisão e devem ser regenerados da fonte depois de cada alteração.

Cada item possui ID estável; número exibido, espelho, referência da linha e estímulos compartilhados são campos separados. Estados úteis: a preparar, redigido, em revisão, corrigindo, verificado automaticamente, pendente, aprovado pelo usuário. Registrar pendência concreta, sem confundir opinião automática com aprovação humana.

Atualizar o estado ao concluir cada grupo. Na retomada, conferir arquivos e fingerprints e continuar somente itens não concluídos ou revisões invalidadas. Arquivo chamado FINAL ou item com campo preenchido não comprova conclusão.

## Contrato de revisão

Primeira passagem: revisor recebe apenas o item estudantil completo (estímulos/ativos inclusive) e instrução para resolvê-lo, identificar ambiguidades, alternativas defensáveis e atalhos. Não enviar gabarito, solução, justificativa de distratores, nota de dificuldade do autor nem histórico que revele a resposta. Usar subagente com contexto novo (`fork_turns="none"` quando essa API estiver disponível), com caminhos absolutos apenas do pacote necessário. Não usar fork completo para chamar a revisão de cega.

Segunda passagem: depois de registrada a solução independente, fornecer espelho, pedido especial e solução autoral para conferir divergências e fidelidade. O revisor pode então avaliar cobrança, função de estímulos e erros dos distratores. A solução final entregue é uma explicação verificável apropriada ao aluno, não um pedido de raciocínio privado.

Itens com fonte ou visual relevante recebem auditoria específica, independente da revisão de gabarito. O auditor confere autenticidade, necessidade, legibilidade no tamanho final, suporte reconhecível, ausência de pistas/sobreposições e diversidade do conjunto. Não aceitar imagem apenas por ter muitos pixels ou por o arquivo abrir corretamente.

Autor corrige somente o que a crítica justifica. Se a crítica alterar um elemento válido ou violar pedido especial, o coordenador arbitra pela evidência. Duas rodadas sem progresso no mesmo defeito acionam outro revisor/abordagem; persistindo incerteza, marcar pendente, seguir os demais e reportar o item. Nenhum limite de tentativas autoriza aceitar uma questão defeituosa.

Uso sugerido de `review_state.py`:

```text
python scripts/review_state.py packet item.json --output cego.json
python scripts/review_state.py check estado.json
```

O item normalizado usa `id`, `student` (somente blocos estudantis e alternativas), `private` (gabarito/solução) e `spec` (espelho e restrições). `packet` gera ID/fingerprint/versão estudantil, rejeitando campos privados indevidos em `student`. Uma imagem pode conter pista visual; o helper não inspeciona seu conteúdo.

O estado para conferência usa `expected_item_ids` (todos os IDs encomendados, preservados desde a entrada), `required_checks` e `items`, cada item com `id`, `path` para snapshot e `reviews`. Cada review tem `check`, `item_sha256`, `result` e `evidence` (caminho de relatório existente). Por padrão, exigir `content`, `cognitive` e `mirror`; exportação final acrescenta `visual` e `technical`. O helper confere cobertura, versões e existência das evidências, sem julgar a veracidade delas. O coordenador deve ler os pareceres e arbitrar resultados.

## Encerramento e consumo

- Não encurtar resoluções ou simplificar as últimas questões para caber em uma resposta gigante. Salvar artefatos progressivamente e entregar o conjunto ao final.
- Não usar os itens “menos piores” do lote como few-shot positivo. Exemplos só entram no contexto de autoria quando aprovados explicitamente ou acompanhados dos defeitos que não devem ser copiados.
- Não enviar banco de feedback inteiro a cada especialista. Mandar critérios ativos pertinentes, entrada completa do item e dados essenciais.
- Só o coordenador consolida a fonte editorial. Evitar sobrescrita de planilha por agentes paralelos.
- Scripts cuidam de cobertura, duplicações, hashes e arquivos; modelos cuidam de concepção e julgamento. Usar apenas revisão suficiente para resolver riscos reais; não repetir checagens já válidas de itens inalterados.
- O runtime ativo pode executar vários grupos num pedido. Interrupção, limite de uso ou encerramento do app pode interromper a execução. Estado salvo permite retomar; execução futura sem turno ativo depende de recurso de agendamento explicitamente pedido.
- Saída final inclui contagem encomendada/concluída/pendente, arquivos e exceções que importam. Não chamar um lote de 90 concluído se só 85 foram revisados.
