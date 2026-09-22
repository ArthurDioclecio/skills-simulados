# Papéis dos agentes

Estes contratos orientam subagentes temporários usados em lotes. Eles não substituem o perfil da prova nem autorizam aprovação automática. Herdar o modelo/esforço escolhido pelo usuário, salvo perfil de modelos previamente autorizado.

## Contexto comum aos papéis

Todos os papéis são multibanca. Consultar o perfil selecionado no [repertório](../../analisar-provas/references/repertorio/index.json), somente na edição/etapa coberta. Usar [contrato e versões](contrato-e-versoes.md) e [revisão visual](revisao-visual.md). `agents/openai.yaml` descreve a interface da skill; estes contratos governam a delegação, não agentes permanentes por exame.

## Analista de prova

Aplicar [analisar-provas](../../analisar-provas/SKILL.md). Entregar fichas com identidade, escrita, operação, dificuldade fundamentada e referências; registrar ocorrências/duplicações e lacunas. Distinguir padrão, exceção e defeito. Não escrever questões ao receber pedido apenas de análise. Revisor da análise confere cobertura e generalizações; coordenador publica o perfil versionado.

## Coordenador

- Identifica prova, edição, perfil, itens, dependências e fonte editorial.
- Define grupos por dependência e esforço; distribui tarefas sem enviar o histórico inteiro.
- Mantém matriz do lote com arquitetura, operação, suporte, fonte, dificuldade pretendida e posição provisória do gabarito.
- Inclui no contrato ativo os feedbacks que substituem sugestões anteriores: operação interpretativa/quantitativa, profundidade do conhecimento e unidade de entrega. Grupos internos de trabalho não determinam a quantidade de arquivos finais.
- É o único que consolida a fonte editorial, resolve conflitos e declara estados.
- Seleciona o perfil e a versão pertinentes, mantém contrato vigente e inventário de ativos. Restauração textual preserva correções visuais não revogadas e gera variante separada quando solicitada.
- Transmite finalidade e restrições do suporte; mantém intenção do autor fora da primeira revisão cega. Validação técnica e inspeção visual permanecem estados separados.
- Não transforma parecer positivo relativo em aprovação. “Melhor do lote” e “sem erro anulatório” continuam exigindo os demais critérios.

## Leitor de espelho

Recebe o espelho completo e o perfil aplicável. Devolve evidências, não uma questão pronta:

- identidade e páginas;
- ordem, gênero e função dos elementos;
- operação e percurso mínimo;
- necessidade de contas e grau de especificidade dos conhecimentos (reconhecimento geral versus terminologia/mecanismo específico);
- forma semântica das respostas e vetor visual depois da renderização;
- características locais versus recorrentes da prova;
- riscos de dependência, fonte ou apresentação.

Não simplifica a arquitetura para facilitar autoria.

## Autor

Recebe apenas o contrato do grupo, espelhos necessários, perfil da prova e restrições do usuário. Para cada item:

- concebe a solução antes da redação;
- usa fonte/visual que sustente a operação;
- não repete imagens entre questões nem usa imagens de questões antigas/espelhos, respeitada a exceção de estímulo único compartilhado expressamente autorizado; entrega procedência e identidade do ativo para a conferência do conjunto;
- evita reutilizar o mesmo excerto do espelho, salvo pedido expresso;
- preserva a representação das respostas e a função dos suportes;
- mantém o caráter interpretativo/quantitativo e a especificidade do espelho, salvo mudança pedida; não troca interpretação por contas nem reconhecimento funcional por memorização especializada por conveniência;
- cria distratores a partir de erros plausíveis distintos;
- executa teste de vazamento: procura no estímulo, título, imagem, equações e opções termos ou relações que entreguem a resposta;
- executa teste de remoção dos estímulos e registra o que cada um acrescenta;
- entrega item, solução verificável, gabarito, fontes e riscos. Não grava a fonte consolidada.
- Registra função de elementos visuais e distratores intencionais; não remove automaticamente contexto não citado. Confere sobreposições, setas, localização de rótulos e leitura no tamanho final. Aplica a sintaxe e os subtipos documentados da matéria, sem fórmula verbal única.

## Revisor cego de conteúdo

Primeiro recebe somente a versão estudantil completa e os ativos necessários. Sem gabarito, solução autoral, posição planejada, histórico de edição ou avaliação anterior:

- resolve o item;
- lista respostas defensáveis e ambiguidades;
- identifica o caminho mais curto, pistas, dados supérfluos e termos que nomeiam a conclusão;
- avalia plausibilidade dos distratores e nível efetivo.
- identifica se a solução exige cálculo ou informação especializada que o espelho/contrato não exigem; a segunda passagem verifica essas duas dimensões explicitamente.

Na primeira passagem, avalia o visual sem receber a intenção do autor. Na segunda, distingue seleção de informação de ruído acidental; intenção não justifica ilegibilidade. Classifica o nível pelo caminho mais curto e informa quando a cobrança não realiza a dificuldade pretendida.

Somente depois recebe espelho, contrato e solução do autor para conferir fidelidade. Uma coincidência de gabarito não encerra a revisão.

## Auditor de fontes e visuais

Recebe arquivos/fontes e o item, mas não precisa da justificativa do autor. Confere:

- autenticidade, rastreabilidade, tratamento editorial e uso adequado do gênero;
- exclusividade das imagens por questão, por identidade visual/procedência e hash; renomeação ou recorte não eliminam uma reutilização;
- necessidade de cada visual e compatibilidade com o espelho;
- qualidade editorial além de resolução: suporte reconhecível, densidade, legibilidade, escala, rótulos, setas, unidades e ausência de sobreposição;
- aparência repetitiva de template, cartões arredondados, paleta e iconografia genéricas;
- se a imagem revela a resposta ou apenas repete o texto;
- ativo a 100% e inserção no tamanho final.

Devolve decisão separada para fonte, função e execução visual. Alta resolução não implica aprovação. Aplica [revisão visual](revisao-visual.md): ativo e saída final, colisões texto/linha, rótulos e referentes, direção de setas, elementos pertinentes e distratores contextuais. Geometria e OCR geram alertas, não aprovação. Registra defeito/local/impacto e evidencia reinspeção após correção.

## Auditor do conjunto

Atua periodicamente e no final. Analisa o lote como sistema:

- distribuição de posições do gabarito e sequências suspeitas;
- distribuição de verdade por rótulo I–IV e combinações corretas recorrentes, incluindo atalhos de eliminação por uma única afirmativa;
- repetição de comandos, contextos, operações e frases de ligação;
- corretas sistematicamente mais longas, cautelosas ou completas;
- distratores com absolutos fáceis;
- concentração de fontes ou suportes e excesso de recursos autorais;
- uniformidade visual que denuncia produção em série;
- degradação das últimas questões e cobertura de todos os itens.

Não altera respostas para “balancear letras”. Reordenação só ocorre quando preserva relações, unicidade e arquitetura.

## Integrador `.qpack`

Recebe conteúdo congelado, ativos aprovados e o perfil correto. Não reescreve a questão para fazê-la caber. Monta a semântica do manifesto, executa empacotamento/validação/formatação e devolve artefatos e evidências. Se a saída não couber ou o visual perder legibilidade, devolve o problema ao coordenador para decisão editorial; não mascara com espaços, quebras ou edição manual do DOCX.

Respeita a unidade de entrega pedida. Não divide por matéria, agente ou caderno sem necessidade autorizada. Em arquivo único com números oficiais coincidentes de cadernos distintos, usa seções identificadas e metadados de espelho; preserva um só exemplar de cada item comum. Não renumera silenciosamente nem multiplica os itens para simular provas completas.
