# Revisão visual para qualquer prova

O perfil da prova e o contrato do item orientam estas verificações. Preferências pessoais não são normas oficiais.


- Revisar separadamente a função didática e a execução gráfica de cada imagem. Uma imagem legível ainda pode fornecer a resposta, desviar a operação ou conter informação conceitualmente incorreta.
- Inspecionar o ativo original a 100% e sua inserção no tamanho final da prova. Conferir a versão efetivamente exportada; examinar apenas a imagem isolada ou suas dimensões não comprova legibilidade final.
- Manter textos, rótulos, números e legendas legíveis, sem sobreposição com linhas ou elementos gráficos. Reposicionar o texto, reservar espaço livre ou reorganizar a composição sem apagar informação necessária. Conferir também recortes, margens, contraste e correspondência entre rótulo e referente.
- Distinguir elementos essenciais à solução, contextualização pertinente, informação ou distrator visual intencional e ruído acidental. A pertinência depende da competência cobrada, do gênero do suporte e do contrato do item.
- Distratores visuais intencionais são admissíveis quando a seleção de informação integra a operação e o contexto permite sua presença. Não confundir esse recurso com texto ilegível, seta ambígua, sobreposição, escala incorreta ou outro defeito gráfico.
- Não remover automaticamente tudo o que o enunciado não cita. Verificar a contribuição interpretativa, contextual ou documental e o efeito da remoção na autenticidade e na dificuldade. Informação contextual legítima não precisa ser indispensável ao cálculo ou aparecer nominalmente no comando.
- Usar siglas e rótulos de modo seletivo e coerente com o público, a disciplina e a prova. Definir os que exigem definição para a leitura; reduzir acúmulo sem eliminar relações ou pistas contextuais legítimas. Não impor a expansão de siglas consagradas nem a remoção automática das não citadas.
- Conferir conteúdo e convenções: números, eixos, escalas, unidades, símbolos, legenda, orientação, direção, conexões e relações espaciais. Toda seta deve ter referente, função e sentido inequívocos; diferenciá-la dos traçados com os quais possa ser confundida.
- Reservar espaço livre suficiente para símbolos de orientação e outros elementos auxiliares. Seu tamanho e sua posição devem permitir leitura na saída final sem cobrir dados, rótulos ou feições relevantes.
- Executar teste de vazamento no visual: título, legenda, cores, destaques e rótulos não devem resolver involuntariamente a operação cobrada. Manter as informações necessárias e as âncoras diretas compatíveis com o espelho.
- Cada nova questão recebe imagens diferentes das usadas em outras questões, espelhos e produções anteriores, conforme a restrição vigente do usuário. Recortar, recolorir, redimensionar ou renomear não cria uma imagem nova. A revisão da mesma questão pode preservar sua imagem.
- Um suporte compartilhado expressamente autorizado constitui um único objeto, exibido uma vez e referenciado pelas questões dependentes. Não o duplicar para preencher páginas nem tratar o compartilhamento como licença geral de reutilização.
- Registrar origem, identidade visual, hash, questão de destino e eventual compartilhamento autorizado. Comparar identidade/procedência e aparência além do hash. Usar registros de exclusão disponíveis, sem abrir material antigo proibido ou alegar cobertura histórica não verificada.
- Quando houver dados geométricos, verificar limites de textos, rótulos e elementos, recortes e colisões. Essa verificação complementa a inspeção visual; não substitui a avaliação de referente, sentido e legibilidade.
- OCR pode alertar para texto perdido, truncado, trocado ou inesperado; confirmar cada alerta no ativo e na saída final. Não tratar ausência de alertas como aprovação nem declarar OCR infalível, especialmente para símbolos, fórmulas e textos pequenos.
- Emitir parecer separado sobre fonte/procedência, função didática e execução visual. Registrar o defeito, sua localização, o impacto e a correção necessária. Após mudança, reinspecionar o ativo ou a saída afetada e conferir novamente a relação com o item.

## Exemplos de aplicação, separados das regras gerais

- Mapa: uma rosa dos ventos exige área livre e tamanho legível, sem encobrir cidades, feições ou legenda. Ela só é necessária quando a convenção, o suporte ou a leitura solicitada a justificam.
- Mapa hidrográfico: a seta que indica uma direção precisa distinguir-se do traçado do curso d’água e apontar sem ambiguidade. Cor sozinha pode ser insuficiente na impressão em tons de cinza; forma, espessura, ponta e posição também ajudam.
- Mapa com siglas: manter apenas a rotulagem pertinente à leitura e ao contexto, sem concluir que toda sigla não mencionada no comando é um erro. Conferir o significado das siglas que o aluno precisa interpretar.
- Gráfico: uma série que não determina a resposta pode ser um distrator visual legítimo se a tarefa exige selecionar dados. Já rótulos sobrepostos ou eixos ilegíveis impedem a leitura e devem ser corrigidos.
- Documento, anúncio ou fotografia: informação periférica pode sustentar autenticidade e interpretação. Simplificá-la indiscriminadamente pode alterar o gênero ou entregar a seleção que caberia ao aluno.

## Apoio geométrico opcional

O script scripts/visual_preflight.py recebe um JSON com width, height e elements. Cada elemento contém id, kind e bbox [x, y, largura, altura], nas mesmas unidades da imagem. Use kind text para rótulos e line para linhas; background e container não geram colisões. allow_overlap_with lista IDs com sobreposição intencional. Execute python scripts/visual_preflight.py geometria.json a partir da pasta da skill.

O script sinaliza caixas cortadas e possíveis colisões de textos; não extrai geometria de imagens, não faz OCR e não decide pertinência pedagógica. Caixa de linha é aproximação e pode gerar falso positivo. Sempre inspecionar a imagem renderizada e sua apresentação final, inclusive quando não houver alertas.
