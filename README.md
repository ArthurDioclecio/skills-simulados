# Skills para análise e confecção de simulados

Repertório de provas e fluxo pessoal para criar, revisar e exportar questões a partir de espelhos e controles XLSX. Configuração multibanca, com perfil inicial PAES e referência parcial SSA.

## Conteúdo

| Pasta | Função |
| --- | --- |
| [analisar-provas](skills/analisar-provas/SKILL.md) | Análise por exame, edição, etapa, matéria e tipo de questão; repertório versionado. |
| [questoes-espelho](skills/questoes-espelho/SKILL.md) | Autoria, revisão, correção, processamento de lotes e QPACK. |
| [humanizer](skills/humanizer/SKILL.md) | Revisão de texto autoral sem alterar conteúdo ou citações. |

Os [contratos dos agentes](skills/questoes-espelho/references/papeis-de-agentes.md) definem analista, coordenador, leitor de espelho, autor, revisor cego, auditores e integrador. São instruções de delegação utilizadas durante a tarefa. Os arquivos agents/openai.yaml são metadados das skills, não processos permanentes.

## Instalação e uso

Copie as três pastas dentro de skills para a pasta skills do seu CODEX_HOME (normalmente ~/.codex/skills). Preserve uma cópia de qualquer configuração existente antes de substituí-la. Mantenha as três pastas lado a lado para os links entre skills funcionarem.

Exemplos de pedidos:

> Use $analisar-provas para analisar estas provas e registrar os padrões no repertório.

> Use $questoes-espelho com estes espelhos e este controle XLSX. Faça os itens indicados e entregue um QPACK por prova.

As fontes de provas, controles e o executável do formatador não estão incluídos. Os caminhos locais documentam o ambiente de origem e precisam ser ajustados em outro computador. Não basta clonar este repositório para instalar plugins ou o formatador.

## Dependências externas

- Python 3 para os scripts auxiliares, que usam a biblioteca padrão.
- Plugins de PDF, planilhas e documentos, conforme os materiais e saídas.
- ImageGen quando houver criação/edição de imagem raster; navegador ou ferramentas de pesquisa para fontes reais.
- Formatador de Simulados: integração documentada com a versão 0.3.1, schemas e perfis incluídos na skill questoes-espelho; executável instalado separadamente.
- Skill de manutenção skill-creator quando for necessário revisar a configuração.

Essas ferramentas são fornecidas pelos respectivos plugins/ambiente e não foram redistribuídas aqui. O humanizer acompanha sua licença MIT original. As demais fontes e materiais de terceiros conservam seus direitos; não se atribui licença geral ao conteúdo das provas.

## Repertório e limites

O [catálogo](skills/analisar-provas/references/repertorio/index.json) distingue prova, edição, etapa e cobertura. PAES: análise anterior de 201 itens únicos e 340 ocorrências dos cadernos de 2025, com programas de 2026 separados. A rastreabilidade visual individual está parcial. SSA: perfil legado parcial. Não há perfis presumidos de outras bancas.

Inspeção visual, correção pedagógica e integridade do arquivo são verificações distintas. Dificuldade é estimativa editorial. Pedidos específicos do lote não viram regras universais. A preferência de imagens inéditas admite suporte único compartilhado quando autorizado.

## Manutenção

Este repositório é uma cópia versionada da configuração em 22/09/2026; alterações locais posteriores não são sincronizadas automaticamente. Atualize os arquivos correspondentes, confira o diff e faça um novo commit/push. Não adicione credenciais, conversas completas, provas, planilhas de trabalho ou QPACKs por engano.

snapshot.json registra hashes das skills copiadas antes da normalização de fim de linha pelo Git; não é um mecanismo de sincronização. O histórico Git registra as revisões publicadas.
