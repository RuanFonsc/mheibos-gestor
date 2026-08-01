# ENG-0010 — Glossário Oficial do Mheibos

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** consolidar o vocabulário canônico usado pela Engenharia do Mheibos e impedir ambiguidades entre conceitos oficiais.  
**Dependências:** todas as RFCs existentes e ENG-0000 a ENG-0009.

---

## 1. Regra de uso

Usar o termo completo quando a forma curta puder representar conceitos diferentes. Este glossário descreve termos das fontes; a RFC proprietária continua sendo autoridade sobre comportamento.

## 2. Produto e plataforma

**Mheibos:** Sistema Operacional Empresarial e memória operacional ativa da empresa.

**Mheibos Gestor:** aplicação principal integrada da primeira versão.

**Central Mheibos:** autoridade global da instalação, responsável por estado oficial, contratos e serviços compartilhados.

**Cliente Mheibos:** aplicação instalada em uma estação e subordinada à Central. Não confundir com Cliente comercial.

**Máquina Principal:** equipamento que hospeda a Central na implantação local.

**Estação:** computador autorizado a executar um Cliente Mheibos.

**Instalação:** implantação do Mheibos para uma organização.

**Organização:** empresa cuja operação é representada.

**Aplicação especializada:** Cliente futuro que usa contratos da mesma Central, sem criar sistema ou verdade paralela.

## 3. Pessoas, identidade e acesso

**Usuário:** pessoa autenticada com identidade própria do Mheibos.

**Perfil:** conjunto principal de responsabilidades e permissões de um usuário.

**Permissão:** autorização determinística para ação em recurso e contexto.

**Exceção individual:** complemento explícito ao Perfil; não é privilégio implícito.

**Sessão:** contexto autenticado de atuação de um usuário.

**Identidade técnica:** identidade atribuída a integração, webhook ou serviço.

**Ação sensível:** operação que exige proteção adicional, como reautenticação, motivo e auditoria.

**Responsável atual:** pessoa com obrigação operacional vigente. Não confundir com autor.

**Autor:** origem humana ou técnica de uma criação/alteração.

**Criador comercial:** autor original da venda para histórico e metas.

**Executor:** pessoa que realiza trabalho em Processo/Etapa.

**Aprovador:** pessoa autorizada a aceitar decisão ou exceção.

## 4. Relações comerciais

**Cliente comercial:** pessoa ou organização que compra da empresa usuária do Mheibos.

**Fornecedor terceirizado:** empresa externa que executa impressão, fabricação ou serviço. Suas mensagens não são correlacionadas automaticamente a Pedido.

**Pedido:** centro comercial e financeiro. Contém relação de venda, itens, valores e vínculos; não representa toda execução.

**Item do Pedido:** produto/serviço comercializado com descrição e condições históricas próprias.

**Número visível do Pedido:** identificação humana não ambígua; não substitui identidade técnica.

**Pagamento:** registro próprio de valor, forma, data e estado.

**Saldo:** valor derivado de total e pagamentos oficiais; não é Pagamento.

**Meta:** critério configurável de desempenho comercial; não transfere autoria ou autoridade.

**Entrega:** dimensão distinta da execução e do financeiro.

## 5. Operação

**Processo:** instância de execução operacional com objetivo, fluxo, etapas, responsabilidades e conclusão.

**Processo Operacional:** conceito geral de atividade organizada; no modelo persistente, realizado por Processo.

**Objetivo:** resultado identificável que justifica Processo ou Missão.

**Modelo de Fluxo:** definição reutilizável e versionável.

**Fluxo Instanciado:** caminho preservado de um Processo confirmado.

**Etapa:** unidade identificável de trabalho dentro de Processo.

**Dependência:** relação explícita que condiciona trabalho ou conclusão.

**Critério de conclusão:** condição determinística/evidenciável para encerrar Processo, Etapa, Missão ou Pendência.

**Estado:** condição atual de uma entidade ou dimensão.

**Estado comercial:** condição da relação de venda.

**Estado operacional:** condição da execução derivada de Processos/Etapas.

**Estado financeiro:** condição de pagamentos e saldo.

**Estado de entrega:** condição logística/entrega.

**Status:** termo evitado isoladamente. Qualificar a dimensão ou entidade.

**Transição:** mudança relevante entre estados, validada por regra.

## 6. Fatos e memória operacional

**Comando:** intenção de realizar operação; pode ser rejeitada.

**Evento:** fato estruturado ocorrido, com identidade, autoria/origem, momento, alvo, mudança e contexto.

**Evidência:** elemento verificável que sustenta fato, estado ou decisão.

**Registro de Auditoria:** trilha protegida e aditiva de ação relevante.

**Histórico:** evolução preservada; não é apenas estado atual.

**Projeção:** visão derivada para consulta; não cria segunda verdade.

**Notificação:** comunicação sobre fato; não substitui Evento.

**Log técnico:** diagnóstico de software; não substitui auditoria de negócio.

**Correlação:** vínculo entre eventos da mesma operação.

**Causalidade:** relação entre fato causador e consequências.

**Idempotência:** propriedade que impede duplicação de efeito em repetição/reenvio.

## 7. Pendências e intervenções

**Pendência:** obrigação não encerrada que exige acompanhamento e decisão consciente.

**Responsável principal:** pessoa que mantém a obrigação, mesmo com múltiplos destinatários.

**Escalonamento:** aumento de visibilidade/supervisão sem remover automaticamente o responsável.

**Lembrete:** reapresentação contextual de compromisso ou pendência.

**Intervenção:** comunicação ativa que busca reconhecimento, decisão ou ação.

**Criticidade:** combinação de risco, urgência, impacto e tempo usada para intensidade.

**Briefing:** síntese contextual de prioridades, riscos e continuidades.

O proprietário normativo definitivo destes termos depende da resolução do elaboração normativa pendente da RFC-0012.

## 8. Colaboração

**Missão:** workspace persistente orientado a objetivo temporário.

**Teamwork:** modo colaborativo de Missão ativado por aceite ou autoridade formal.

**Participante:** usuário vinculado a Missão com papel e estado.

**Tarefa de Missão:** trabalho específico ou referência a Processo/Etapa; não duplica processo oficial.

**Conversa:** comunicação cronológica.

**Nota:** conteúdo consolidado, diferente de mensagem.

**Plano de ação:** proposta estruturada de tarefas, responsáveis, prazos e acompanhamento.

## 9. Arquivos e integrações

**Referência de Arquivo:** caminho/localização, metadados e vínculo operacional; não exige binário no banco.

**Arquivo oficial de arte:** arquivo formalmente escolhido para produção.

**Anexo:** arquivo relacionado, mas não necessariamente oficial.

**Documento gerado:** PDF/ordem/relatório vinculado à entidade que lhe dá contexto.

**Adaptador de Integração:** fronteira que encapsula sistema externo.

**Webhook:** entrada técnica autenticada; não possui autoridade implícita.

**WhatsApp integrado:** canal de cliente comercial assistido com contexto e controle humano.

## 10. Offline e sincronização

**Estado global:** visão oficial consolidada pela Central.

**Estado local persistente:** cache, preferência ou operação permitida preservada no Cliente.

**Estado local exclusivo:** registro ainda não incorporado pela Central.

**Estado temporário:** seleção, rascunho ou adaptação sem autoridade oficial.

**Operação offline:** comando permitido sob regras previamente fornecidas.

**Sincronização:** incorporação e atualização automática, visível, idempotente e recuperável.

**Conflito de sincronização:** incompatibilidade entre operações/versões que exige política ou decisão.

**Origem:** usuário, estação, sessão, integração ou sistema que produziu dado/operação.

## 11. Interface

**Interface Viva:** capacidade de adaptar temporariamente apresentação e atenção por contexto autorizado.

**Orquestrador de Interface:** componente do Cliente que traduz comandos estruturados em ações visuais.

**Adaptação temporária:** mudança visual reversível; não é preferência persistente.

**Preferência individual:** configuração do usuário sem efeito sobre regra de negócio.

**Configuração organizacional:** política que altera comportamento oficial, versionável e auditável.

## 12. Inteligência e conhecimento

**IA / camada cognitiva:** componente que interpreta, explica, sugere, planeja e acompanha.

**Gateway de IA:** única fronteira autorizada entre plataforma e modelo.

**Modelo de linguagem:** mecanismo substituível; não armazena verdade oficial.

**Saída estruturada:** resposta do modelo submetida a schema, permissões e validação.

**Hipótese:** explicação possível ainda não confirmada.

**Recomendação:** proposta justificável, não ordem nem regra.

**Conhecimento oficial:** conteúdo aprovado com autoridade, origem, escopo e vigência.

**Conhecimento operacional:** fato atual derivado de fontes do sistema.

**Procedimento emergente:** prática útil ainda não obrigatória.

**Ensinamento pendente:** conteúdo submetido e não aprovado.

**Memória curta:** contexto imediato e temporário.

**Memória longa:** conhecimento/histórico consolidado e revisável.

**Recuperação de contexto:** seleção controlada do menor conjunto suficiente.

**Explicabilidade:** capacidade de mostrar fatos, fontes, relações, confiança e incerteza.

## 13. Engenharia

**RFC:** fonte normativa de arquitetura ou produto.

**Inventário Oficial:** distribuição canônica de decisões e RFCs proprietárias.

**ENG:** documento de engenharia subordinado às RFCs.

**ADR:** registro aprovado de escolha técnica que não cria regra de produto.

**Quality Gate:** critério cumulativo de conclusão.

**Compatibilidade temporária:** ponte limitada com dono e remoção.

**Correção normativa:** mudança porque implementação contradiz fonte superior.

**Decisão pendente:** ausência de autoridade suficiente para agir.

**DECISAO_HUMANA_NECESSARIA:** marcador formal de parada.

## 14. Termos proibidos ou condicionais

- “cliente” isolado quando puder ser comercial ou Cliente Mheibos;
- “status” sem dimensão;
- “usuário” quando papel específico importa;
- “arquivo” quando oficial, anexo, referência ou evidência importam;
- “IA decidiu” para autorização ou transição oficial;
- “excluir” sem dizer lógico, físico, vínculo, cancelamento ou arquivamento;
- “sincronizado” sem distinguir aceito pela Central;
- “concluído” sem critério e gates.

## 15. Lacunas

- responsabilidade de Pendências/Lembretes/Escalonamento depende da RFC-0012 reservada e ainda não elaborada;
- Analytics/Simulação e Governança/Segurança da IA aguardam RFC-0015/0016;
- nomes físicos finais de entidades/código podem ser definidos por implementação/ADR, preservando o conceito.

## 16. Relatório de validação

O glossário foi revisado contra RFC-0000 a RFC-0014, Inventário e ENG anteriores. Termos possuem fronteiras e não recebem comportamento novo.

| Gate | Resultado |
|---|---|
| Fonte Normativa | APROVADO COM LACUNAS |
| Arquitetura | APROVADO |
| Domínio | APROVADO |
| Dados | APROVADO |
| Eventos/Auditoria | APROVADO |
| Segurança | APROVADO |
| IA | APROVADO |
| UX | APROVADO |
| Código | NÃO APLICÁVEL |
| Testes | APROVADO — termos e referências revisáveis |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
