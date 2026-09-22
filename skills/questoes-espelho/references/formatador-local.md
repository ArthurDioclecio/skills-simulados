# Formatador de Simulados local

Endereço fornecido pelo usuário e corrigido por inspeção em 06/09/2026. Usar esta configuração pessoal quando o pedido envolver o formatador existente. Em outro computador ou após atualização, revalidar a existência e o perfil, sem presumir que os caminhos permaneçam iguais.

## Executável selecionado

```text
C:\Users\arthu\Documents\Codex\2026-07-20\qua\SimuladoFormatter\release\FormatadorDeSimulados_0.3.0\FormatadorDeSimulados_0.3.1_UMA_QUESTAO_POR_PAGINA.exe
```

- Versão operacional: **0.3.1**, conforme indicação do usuário, nome do executável e README de recuperação.
- SHA-256 conferido: `CEC0DCB2198C5854B24E7D1DC6A0E664A6180F92D3D79CFAF0F89647ECFB028D`.
- O nome da pasta permanece `FormatadorDeSimulados_0.3.0`. Não há uma subpasta `FormatadorDeSimulados\_0.3.0`.
- Não escolher o arquivo vizinho `FormatadorDeSimulados.exe` por ter nome mais curto; o executável selecionado é o nome completo acima.
- Os metadados Windows de versão estão vazios e `pyproject.toml` do código recuperado ainda declara 0.3.0. Isso não deve substituir a versão operacional identificada.
- Cópia de recuperação com o mesmo hash: `C:\Users\arthu\Documents\Codex\2026-07-20\qua\SimuladoFormatter\release\FormatadorDeSimulados_0.3.1_RECUPERADO\FormatadorDeSimulados_0.3.1_UMA_QUESTAO_POR_PAGINA.exe`.

## Documentação e perfis

Base recuperada: `C:\Users\arthu\Documents\Codex\2026-07-20\qua\SimuladoFormatter\release\FormatadorDeSimulados_0.3.1_RECUPERADO`.
Nessa pasta, `README_RECUPERACAO_0.3.1.md` explica a versão; `codigo-fonte\src\simulado_formatter\cli.py` define os comandos e `formatter.py` aplica as regras do perfil.

O perfil histórico em `perfis\ssa_upe_2026_uma_questao_por_pagina.json` usa a numeração `{number}- `. O requisito editorial consolidado usa `{number}. `. O código 0.3.1 consulta `rules.question_number_format`, então passar explicitamente o perfil apropriado é necessário; não alterar o programa para essa preferência nem usar o perfil padrão sem conferência.

Para o SSA atual, os perfis empacotados nesta skill são [qpack/ssa_upe.json](qpack/ssa_upe.json) para estudante e [qpack/ssa_upe_com_gabarito.json](qpack/ssa_upe_com_gabarito.json) para revisão quando pedida. Eles explicitam a numeração com ponto e o formato editorial consolidado. Validar e inspecionar sua aplicação na saída real. Outra prova ou perfil solicitado prevalece sobre esses padrões.

Aplicar também [qpack-semantica.md](qpack-semantica.md): o manifesto descreve função/conteúdo e o perfil descreve aparência. Não transportar o perfil SSA para outra banca nem tentar reproduzir layout com espaços, tabulações ou quebras artificiais.

## Execução por CLI

O programa abre a interface quando executado sem argumentos; para automação usar os subcomandos. O teste `--help` encerrou com código 0 e sem texto de saída, comportamento compatível com a compilação sem console. Não existe opção `--version` no parser examinado. Código de saída e silêncio do comando não comprovam por si só que um artefato foi produzido corretamente.

Comandos confirmados no código recuperado:

```text
validate INPUT --profile PERFIL
format INPUT --profile PERFIL --output DOCX [--preview]
format-batch INPUTS --mode combined|separate --output DESTINO
pack MANIFEST --output QPACK [--assets-root DIR]
preview DOCX --output-dir DIR
```

Invocar o executável pelo caminho completo e citar os argumentos corretamente no PowerShell. Salvar saídas em `work` durante a conferência e em `outputs` para entrega; nunca sobrescrever referências/questões aprovadas incidentalmente. Evitar usar `format-batch` com renumeração implícita: conferir os IDs/números e a opção de preservação no parser antes da aplicação.

Na exportação efetiva: conferir manifesto/ativos, executar `validate` com o perfil selecionado, executar `format`, verificar que o arquivo esperado foi criado nesta execução e inspecionar com as skills Documents/PDF. Revalidar fontes efetivas, numeração, vetor das alternativas, gabarito visível/oculto, tabelas, imagens e paginação. Se a prévia por LibreOffice não estiver disponível, manter a distinção entre geração DOCX e inspeção visual pendente. Validação técnica, layout e qualidade editorial são resultados separados.

Integração técnica verificada em 17/09/2026 com o lote Q1–Q10/Q71–Q80: o executável empacotou, validou e formatou um `.qpack` de 20 questões/9 imagens sem erro de schema e gerou 20 páginas para inspeção. Essa evidência confirma o fluxo técnico da versão 0.3.1; a auditoria editorial posterior apontou problemas substanciais de conteúdo e direção de arte. Não chamar um lote de aprovado porque `validate` retornou zero ou o DOCX abriu.
