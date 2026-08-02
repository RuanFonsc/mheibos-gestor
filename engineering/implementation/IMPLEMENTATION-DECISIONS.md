# Decisões da Implementação

## DEC-IMP-013 — Cache offline após dupla confirmação, sem exportar hash

- **Decisão:** a senha informada no login permanece apenas na memória do Cliente; após sessão central aceita e Estação autenticada, é cifrada localmente junto ao snapshot não secreto.
- **Alternativa rejeitada:** transmitir o hash persistido do operador. Esse material seria reutilizável e ampliaria o impacto de interceptação ou vazamento do cache.
- **Dupla confirmação:** sessão identifica a pessoa; segredo protegido identifica a Estação. Nenhuma das duas provas isolada atualiza a identidade offline.
- **Escopo:** somente a última identidade validada é mantida; uma nova confirmação substitui conscientemente a anterior.
- **Falha:** candidato inválido não apaga cache anterior; divergência de nome ou falha de rede mantém estado seguro.
- **Situação:** definitiva para aquisição do cache; bootstrap e validação local usarão o conteúdo cifrado sem criar catálogo de múltiplas identidades.

## DEC-IMP-012 — Segredos locais sob proteção do sistema operacional

- **Decisão:** credenciais persistentes do Cliente usam `safeStorage` do Electron/Windows; JSON local contém somente Base64 do conteúdo cifrado.
- **Falha segura:** se o cofre do sistema não estiver disponível, o setup não persiste a configuração e explica a falha.
- **Abrangência:** segredo da Estação e senha PostgreSQL existente seguem o mesmo contrato; nenhuma compatibilidade mantém nova gravação em texto.
- **Provisionamento:** administrador reautenticado cria Estação na Central; o segredo é revelado uma vez e a Central conserva apenas hash verificável.
- **Migração:** campos legados legíveis são aceitos apenas em memória para conversão imediata e removidos ao regravar.
- **Limite:** segredo decifrado pode existir somente em memória durante a execução/autenticação do processo local; não entra em logs, eventos, argumentos de linha de comando ou documentação.
- **Situação:** definitiva para armazenamento; rotação e revogação visual entram após o primeiro fluxo conectado.

## DEC-IMP-011 — Transporte central autenticado por Estação

- **Decisão:** a incorporação HTTP usa UUID público da Estação e segredo Bearer de alta entropia, persistido na Central somente por hash do Django.
- **Motivo:** sessão web do usuário não é prova suficiente da origem técnica offline; Estação e autoria humana precisam permanecer identidades separadas.
- **Limite:** o segredo não será colocado no `.env` definitivo do Cliente. IMP-008C deve usar armazenamento protegido do sistema operacional antes de habilitar envio real.
- **Validação:** Estação ativa, correspondência com envelope, checksum, schema, código permanente da autoria e idempotência são verificados antes de persistir.
- **Resposta:** confirmação expõe somente código, ID global e UUID offline; não devolve payload ou segredo.
- **Situação:** definitiva para a fronteira central; rotação, expiração e interface de provisionamento serão ampliadas sem alterar o envelope causal.

## DEC-IMP-010 — Um backend executável em papéis separados, sem banco compartilhado offline

- **Decisão:** reutilizar casos de uso e schema do backend nos papéis `central` e `client_offline`, mantendo processos e bancos fisicamente separados por execução.
- **Motivo:** o Electron já empacota o backend; iniciar um serviço local reduz duplicação de regras sem transformar indisponibilidade da Central em indisponibilidade do Cliente.
- **Proibição preservada:** o Cliente nunca acessa diretamente o banco central e não considera uma tabela central como fila local.
- **Identidade:** Pedido local usa UUID próprio; código visível combina código permanente da pessoa e sequência durável da Estação. PK de banco local não participa da identidade entre nós.
- **Fila:** unidade causal é imutável; apenas estado de envio, tentativas e falhas evoluem. Nenhuma remoção comum é permitida.
- **Incorporação:** a Central aceita unidade completa em transação, preserva autoria/origem e reconhece reenvios pela chave idempotente.
- **Compatibilidade:** `MHEIBOS_RUNTIME_ROLE=central` é o default e não altera o funcionamento existente.
- **Situação:** definitiva para a fronteira; SQLite local, transporte e política exata de retentativa permanecem decisões técnicas das próximas fatias.

## DEC-IMP-009 — Fundação cognitiva antecipada, opcional e sem autoridade

- **Decisão humana:** em 01/08/2026, foi autorizada a entrada antecipada de IA por API, com retomada posterior do IMP-008.
- **Interpretação:** antecipar somente Gateway substituível, adaptador e um uso assistivo de leitura; não declarar concluídas a arquitetura cognitiva, analytics ou governança dependentes das RFCs 0015/0016 futuras.
- **Fontes preservadas:** RFC-0003 §10.9; RFC-0004; RFC-0006; RFC-0011. Nenhuma RFC foi alterada silenciosamente.
- **Provider:** Gemini fica atrás do Gateway; modelo e provider são configuração, não regra de domínio.
- **Falha segura:** IA desligada, sem chave ou indisponível produz fallback determinístico; processos oficiais continuam sem degradação de autoridade.
- **Dados:** o primeiro uso envia apenas ID técnico e projeção de estados; exclui dados pessoais, financeiros, texto livre e arquivos.
- **Autoridade:** resultado não persiste fatos, não autoriza transições e não substitui decisão humana ou regra determinística.
- **Segredo:** chave somente em variável de ambiente; nunca em código, documentação, teste, evento ou log.
- **Situação:** definitiva para a fronteira e regra de não bloqueio; capacidades cognitivas ampliadas permanecem futuras.

## DEC-IMP-008 — Pendência estrutural sem política temporal presumida

- **Decisão:** implementar a entidade Pendência e integrar bloqueios de Processo, mantendo scheduler, cadência, criticidade automática e escalonamento fora do código até aprovação da RFC-0012.
- **Motivo:** RFC-0005 e Inventário fecham estrutura e invariantes, enquanto RFC-0012 v0.0 proíbe inventar as escolhas temporais.
- **Fontes:** RFC-0005 §18; RFC-0009 §§10–14 e 30.8; INV-085 a INV-092; RFC-0012 v0.0.
- **Fluxo:** bloqueio cria uma Pendência idempotente; retomada/conclusão resolve; cancelamento autorizado encerra; eventos preservam autoria e forma.
- **Responsabilidade:** responsável da Etapa permanece responsável principal; destinatários adicionais não transferem automaticamente responsabilidade.
- **Interface:** lista textual não bloqueante, acessível pelo módulo normal; usuário comum vê apenas itens próprios/destinados, administrador vê o conjunto autorizado.
- **Situação:** definitiva para estrutura; política temporal é `DECISAO_HUMANA_NECESSARIA` registrada em Blockers.

## DEC-IMP-007 — Processo prevalece na projeção operacional

- **Decisão:** todas as interfaces consomem `ProjecaoPedido`; quando existe Processo formal, seu estado é oficial, e `Pedido.status` só serve de fallback marcado para legado.
- **Motivo:** elimina interpretações concorrentes sem apagar pedidos antigos nem exigir backfill especulativo.
- **Fontes:** RFC-0003 §§9 e 12.6; RFC-0005 §§3.1, 12 e 16; RFC-0009 §§5–7 e 30; ENG-0006 §9.
- **Abrangência:** lista e detalhe do Gestor, fila de Produção, Vendas, dashboard individual e relatório comercial.
- **Autorização:** a projeção é somente leitura e não amplia acesso; cada view preserva seu recorte e identidade atuais.
- **Compatibilidade:** pedidos sem Processo mostram a fonte `Compatibilidade legada`; a condição de remoção é a migração explícita dos fluxos proprietários.
- **Falhas:** nenhuma IA ou integração participa da projeção; ausência dessas camadas não afeta navegação nem operação.
- **Situação:** definitiva para precedência e contrato; formatos visuais poderão evoluir.

## DEC-IMP-006 — Piloto aditivo de Processo de Produção

- **Decisão:** instanciar um Processo nativo `PRODUCAO_PEDIDO`, com snapshot do Modelo de Fluxo versão 1 e Etapa `PRODUZIR`, nas novas transições para produção.
- **Motivo:** transforma uma operação real existente no primeiro corte observável de Processo/Etapa sem inferir processos históricos nem copiar responsabilidades financeiras do Pedido.
- **Fontes:** RFC-0002 §§Processo Operacional, Conceitos e Quebra de Fluxo; RFC-0005 §§12–16 e 27; RFC-0006 §§7, 11 e 13; ENG-0006 §8.
- **Migração:** schema exclusivamente aditivo e sem backfill; Pedidos antigos continuam legíveis e recebem Processo somente numa nova transição explícita.
- **Histórico:** Modelo de Fluxo usado torna-se imutável; nova definição exige nova versão, enquanto Processo preserva código e versão em snapshot.
- **Transições:** entrar em produção inicia; pronto conclui; rejeição bloqueia com motivo; retomada desbloqueia; cancelamento cancela; processo final não reabre pelo status legado.
- **Auditoria:** `ProcessoConfirmado`, `EtapaConcluida`, `ProcessoBloqueado`, `ProcessoDesbloqueado` e `ProcessoCancelado` compartilham a transação da mudança.
- **Compatibilidade:** `Pedido.status` ainda dispara o piloto até as projeções consumirem Processo/Etapa no IMP-006.
- **Situação:** piloto definitivo como fronteira; catálogo completo de fluxos, dependências e evidências entra em ciclos posteriores.

## DEC-IMP-005 — Estados registrados e derivados do Pedido

- **Decisão:** persistir estado comercial e estado de entrega; derivar o estado financeiro do total e dos pagamentos confirmados.
- **Motivo:** mantém as dimensões independentes sem criar uma segunda fonte da verdade financeira.
- **Fontes:** RFC-0005 §§10, 16, 17 e 26; RFC-0013 §2; INV-096 a INV-099; ENG-0006 §7.
- **Compatibilidade:** `Pedido.status` permanece temporariamente como projeção operacional legada até Processo/Etapa no IMP-005.
- **Migração:** cancelado, pronto e entregue são mapeados; entregue somente vira comercialmente concluído quando os pagamentos comprovam quitação.
- **Segurança:** entrega com saldo é recusada até existir autorização superior com reautenticação, motivo, auditoria e pendência.
- **Reversibilidade:** campos são aditivos; o backfill não altera nem exclui o status legado.
- **Situação:** definitiva para a separação; vocabulário poderá ser ampliado somente por fonte normativa.

## DEC-IMP-004 — Evento aditivo na mesma transação do caso de uso

- **Decisão:** persistir o evento oficial na mesma transação da mudança primária; consequências secundárias serão desacopladas posteriormente.
- **Motivo:** impede estado alterado sem auditoria e entrega valor funcional antes de escolher barramento ou outbox.
- **Fontes:** RFC-0006 §§6, 13, 17, 18 e 23.
- **Alternativas rejeitadas:** log técnico; sinal Django implícito; infraestrutura assíncrona sem consumidor.
- **Impacto:** falha ao registrar o evento reverte a transição.
- **Migração:** tabela exclusivamente aditiva; não converter histórico antigo por inferência.
- **Reversibilidade:** migration reversível enquanto não houver consumidores externos.
- **Situação:** definitiva para atomicidade; transporte secundário permanece substituível.

## DEC-IMP-002 — Migração oportunista de senhas legadas

- **Decisão:** senhas novas usam o hasher do Django; credenciais antigas em texto são aceitas uma única vez e convertidas somente após validação correta.
- **Motivo:** remove texto legível sem exigir conhecimento da senha original e sem bloquear usuários existentes.
- **Fontes:** RFC-0007 §§5.2, 6.1–6.4; INV-030; ENG-0007.
- **Alternativas rejeitadas:** manter texto até migração manual; invalidar todas as senhas; tentar hash em migration sem distinguir valores já protegidos.
- **Impacto funcional:** login permanece compatível; senha inválida nunca provoca conversão.
- **Migração:** gradual, sem inferência e sem reversão para texto legível.
- **Reversibilidade:** código reversível; hashes produzidos não devem ser revertidos.
- **Situação:** definitiva. Compatibilidade com texto legado será removida quando auditoria confirmar ausência desses valores.

## DEC-IMP-003 — Sessão usa identificador técnico

- **Decisão:** `operador_id` é a identidade da sessão; `operador_nome` permanece somente como compatibilidade e apresentação.
- **Motivo:** nome pode mudar e não é identidade estável.
- **Fontes:** RFC-0005 §§6.1, 6.3, 8.1 e 8.3; RFC-0007 §§5.1 e 5.6.
- **Alternativas rejeitadas:** continuar por nome; introduzir imediatamente um segundo modelo de usuário paralelo.
- **Impacto funcional:** renomear usuário não encerra a sessão.
- **Migração:** sessões antigas são promovidas ao serem resolvidas.
- **Reversibilidade:** compatibilidade por nome permite rollback temporário.
- **Situação:** definitiva para identidade técnica; remoção da chave legada será feita após estabilização.

## DEC-IMP-001 — Primeiro corte pelo fluxo de mudança de status

- **Decisão:** migrar primeiro mudanças de status para um caso de uso transacional, preservando a interface atual.
- **Motivo:** é uma operação crítica, duplicada e atualmente nem sempre auditada; cria fronteira utilizável para autorização e eventos posteriores.
- **Fontes:** ENG-0006 §§3–6; RFC-0006 §§5–9; RFC-0007.
- **Alternativas rejeitadas:** criar infraestrutura genérica de eventos sem consumidor; redesenhar telas antes do domínio.
- **Impacto funcional:** mesma ação visível, agora com regra única e histórico.
- **Migração:** novo vínculo opcional de autoria; históricos antigos permanecem sem autoria inferida.
- **Reversibilidade:** migration reversível; views podem ser restauradas pelo Git.
- **Situação:** definitiva para a fronteira do caso de uso; histórico atual é compatibilidade temporária até o evento oficial.

## DEC-IMP-014 — Bootstrap offline conservador pela entrada padrão

- **Decisão:** materializar a credencial confirmada em um SQLite local novo por comando restrito ao papel offline, recebendo o snapshot cifrado/decriptado pelo Electron exclusivamente pela entrada padrão.
- **Motivo:** habilita autenticação offline com o mecanismo existente sem exportar hash da Central nem expor senha em arquivo, argumento ou variável de ambiente.
- **Proteção:** Estação, papel e permissões são validados; a presença de outra identidade interrompe a transação sem alterar o banco.
- **Alternativas rejeitadas:** transportar hash da Central; passar senha na linha de comando; substituir ou desativar operadores preexistentes; criar catálogo local de várias identidades.
- **Situação:** definitiva para o bootstrap; orquestração pelo Electron pertence à fatia seguinte.

## DEC-IMP-015 — Fallback local em porta e papel dedicados

- **Decisão:** quando a Central estiver indisponível na abertura, o Cliente prepara um SQLite exclusivo e inicia o mesmo backend no papel `client_offline`, em porta local distinta da instalação Central.
- **Motivo:** reaproveita contratos e autenticação determinísticos sem transformar tabela central em cache, e evita confundir um serviço local preexistente com o fallback.
- **Segurança:** somente a identidade anteriormente confirmada e cifrada para a mesma Estação pode ser materializada; falhas interrompem a abertura sem criar credenciais padrão.
- **Alternativas rejeitadas:** operar diretamente no banco central; usar a mesma porta do servidor local; liberar o primeiro administrador no cliente; guardar senha em parâmetro ou ambiente.
- **Situação:** definitiva para a partida offline; retorno e sincronização permanecem responsabilidade de IMP-008D.

## DEC-IMP-016 — Tentativa registrada antes da rede e confirmação validada depois

- **Decisão:** persistir `ENVIANDO` e incrementar a tentativa antes de qualquer I/O; somente uma confirmação central coerente muda a unidade para `INCORPORADA`.
- **Motivo:** permite recuperar quedas em qualquer lado da requisição sem apagar pacote, duplicar efeito ou presumir sucesso.
- **Recuperação:** estados intermediários são reelegíveis e o endpoint central responde idempotentemente; falha temporária recebe backoff e recusa normativa exige atenção humana.
- **Alternativas rejeitadas:** remover da fila antes do POST; considerar qualquer HTTP 2xx como confirmação; repetir recusas permanentes indefinidamente.
- **Situação:** definitiva para o ciclo local; transporte concreto pertence à próxima fatia.

## DEC-IMP-017 — Transporte executado pelo backend offline, agendado pelo Electron

- **Decisão:** o Electron dispara um comando periódico, mas o backend offline seleciona unidades, constrói envelopes, envia, valida respostas e persiste transições.
- **Motivo:** mantém autoridade de negócio fora da interface e evita acesso direto do processo desktop ao SQLite.
- **Segurança:** credencial da Estação vem do cofre, redirects são recusados e nenhuma resposta encerra unidade sem confirmação semântica coerente.
- **Operação:** execução imediata e a cada 30 segundos não se sobrepõe; indisponibilidade não bloqueia criação de novos Pedidos locais.
- **Alternativas rejeitadas:** manipular fila pelo JavaScript; apagar item após HTTP 2xx; seguir redirects; repetir em loop sem backoff.
- **Situação:** definitiva para o transporte; comutação de sessão continua separada.

## DEC-IMP-018 — Retorno online explícito após prova de fila zerada

- **Decisão:** oferecer retorno somente quando a Central responder e o backend local provar ausência de unidades não incorporadas; revalidar ambos após a confirmação humana.
- **Motivo:** evita abandonar dados locais, interromper formulários silenciosamente ou confiar em contagem mantida pela interface.
- **Preservação:** o backend local é encerrado, mas o SQLite permanece; nenhuma limpeza automática acompanha a troca.
- **Experiência:** continuar offline é o padrão seguro e o aviso não se repete na mesma sessão quando recusado.
- **Alternativas rejeitadas:** comutação automática imediata; verificar fila em JavaScript; excluir banco após sincronização; considerar apenas disponibilidade de rede.
- **Situação:** definitiva; smoke empacotado permanece como evidência humana pendente.

## DEC-IMP-019 — Arquivo oficial é vínculo imutável, não campo nem binário

- **Decisão:** representar cada arte oficial por entidade UUID vinculada ao Pedido, com identidade física imutável, proveniência, integridade, metadados e autoria; nunca armazenar o conteúdo binário.
- **Motivo:** RFC-0014 admite vários arquivos e torna nome/localização parte da identidade, enquanto o campo único legado não preserva história nem integridade.
- **Migração:** cada caminho legado não vazio gera vínculo `LEGADO/NAO_VERIFICADO`, com autoria nula; o campo antigo permanece até todos os consumidores e dados serem validados.
- **Auditoria:** novo vínculo e evento confirmam atomicamente; exclusão direta é proibida e revisão anual usará encerramento explícito.
- **Alternativas rejeitadas:** ampliar o `CharField`; guardar upload/binário; inferir autoria; renomear caminho existente; apagar vínculo ao cancelar Pedido.
- **Situação:** definitiva para identidade e persistência; criação/monitoramento serão adicionados incrementalmente.

## DEC-IMP-020 — Reconhecimento de alerta preserva a discrepância

- **Decisão:** separar o estado de integridade do reconhecimento humano; `Eu entendi` registra ciência, autoria e instante, mas mantém o arquivo em `ALERTA` até uma verificação física sem discrepâncias.
- **Motivo:** a confirmação exigida pela RFC-0014 é evidência de consciência, não autorização para transformar falha física em integridade.
- **Revalidação:** toda verificação substitui a fotografia anterior e limpa o reconhecimento, impedindo que um aceite antigo cubra uma discrepância nova.
- **Limite:** a leitura inicial cobre propriedades universais do sistema de arquivos; propriedades gráficas específicas serão adicionadas somente com extratores determinísticos por formato.
- **Situação:** definitiva.

## DEC-IMP-021 — Arte de referência encerra vínculo sem apagar o arquivo

- **Decisão:** adaptar temporariamente `ArtePedido` como representação explícita da arte de referência da Ordem de Produção e trocar exclusão por desvinculação auditada.
- **Motivo:** a RFC-0014 distingue referência visual de arquivo oficial; a implementação legada misturava linguagem e apagava fisicamente a imagem ao remover ou excluir o Pedido.
- **Histórico:** vínculos encerrados ficam fora das projeções operacionais, mas preservam arquivo, metadados, hash, autoria e eventos; a proteção do Pedido impede cascata destrutiva.
- **Compatibilidade:** o nome técnico legado permanece até migração própria; `Pedido.artes_ativas` torna a intenção explícita nos consumidores.
- **Alternativas rejeitadas:** renomear tabela/modelo na mesma fatia; apagar o arquivo físico; reutilizar `ArquivoOficialArte`; ocultar vínculos encerrados por gerenciador implícito.
- **Situação:** definitiva para o ciclo de vida; nomenclatura física ainda temporária.

## DEC-IMP-022 — Anexo é conteúdo opaco com duplicidade decidida por pessoa

- **Decisão:** representar anexos gerais em entidade própria, sem interpretação, usando SHA-256 apenas como metadado técnico para detectar conteúdo repetido.
- **Motivo:** RFC-0014 exige lista única, não interpretação e decisão humana sobre duplicidades; arquivo oficial e referência visual possuem responsabilidades diferentes.
- **Duplicidade:** recusar por padrão e exigir marcação explícita para manter outra cópia; a decisão é persistida no evento de vínculo.
- **Preservação:** desvinculação mantém o arquivo físico e o registro histórico; falha anterior à constituição do vínculo pode limpar somente a cópia órfã criada pela tentativa.
- **Segurança:** armazenamento privado não expõe URL de mídia; o download autorizado força resposta como anexo e recurso alheio não revela existência.
- **Alternativas rejeitadas:** analisar extensão/conteúdo; abrir arquivo para validar senha; fundir com arte oficial; sobrescrever duplicado; apagar físico ao remover da lista.
- **Situação:** definitiva.

## DEC-IMP-023 — Pesquisa de artes integra a consulta de Pedidos

- **Decisão:** centralizar em serviço de leitura os critérios da RFC-0014 e aplicá-lo à lista existente de Pedidos, exibindo nomes de arquivos oficiais ativos no próprio resultado.
- **Motivo:** localizar uma arte significa localizar seu contexto operacional; uma tela ou índice paralelo duplicaria Pedido e tenderia a divergir da fonte oficial.
- **Escopo:** consulta inclui campos comerciais, telefones, itens, referências e metadados técnicos; vínculos encerrados são excluídos da projeção operacional sem apagar histórico.
- **Portabilidade:** JSON é convertido para texto pela camada ORM e números técnicos usam igualdade tipada, mantendo o contrato entre SQLite e PostgreSQL.
- **Alternativas rejeitadas:** pesquisa por IA; índice externo prematuro; pesquisa somente por nome; incluir vínculos encerrados como resultado operacional.
- **Situação:** definitiva para semântica; estratégia de indexação permanece evolutiva.

## DEC-IMP-024 — Extração técnica é incremental por formato

- **Decisão:** executar leitura automática somente para extensões raster suportadas pela dependência Pillow já instalada; formatos sem extrator permanecem válidos e preservam seus metadados anteriores.
- **Motivo:** RFC-0014 exige propriedades “quando possível”, sem autorizar dependências inseguras, interpretação aproximada ou bloqueio de CDR/AI/SVG.
- **Discrepância:** falha em extensão declaradamente suportada é evidência de inconsistência técnica; formato ainda não suportado é capacidade ausente, não erro do arquivo.
- **Persistência:** propriedades específicas ficam sob `propriedades_tecnicas.leitura_raster`; dimensões e DPI também ocupam campos tipados para consulta.
- **Alternativas rejeitadas:** tentar abrir todo arquivo; apagar metadados de extrator anterior; tratar formato não suportado como alerta; usar IA para inferir dimensões.
- **Situação:** definitiva para política incremental; conjunto de extratores pode crescer.

## DEC-IMP-025 — Encerramento rompe operação, não história nem arquivo físico

- **Decisão:** encerrar vínculo oficial por ação administrativa explícita, persistindo autoria/contexto e mantendo integralmente identidade e fotografia técnica.
- **Motivo:** RFC-0014 declara vínculos físicos não permanentes, mas exige história, auditoria, metadados, nome e informações técnicas após o encerramento.
- **Backup:** registrar somente a declaração opcional de backup prévio; não presumir execução nem condicionar o encerramento onde a RFC diz “podendo”.
- **Projeção:** encerrado deixa de abrir, verificar e aparecer em pesquisa operacional, mas permanece legível no detalhe histórico.
- **Alternativas rejeitadas:** exclusão; mover/renomear arquivo; apagar metadados; exigir backup; inferir período anual pela data do Pedido ou pelo caminho.
- **Situação:** definitiva para encerramento individual; agrupamento temporal é decisão pendente separada.

## DEC-IMP-026 — Lacunas de configuração isolam o restante da RFC-0014

- **Marcador:** `DECISAO_HUMANA_NECESSARIA` apenas para criação física, backup e agrupamento anual; as partes independentes permanecem válidas.
- **Fontes consultadas:** RFC-0014; Inventário Oficial; diagnóstico e relatório funcional; `MAPA_MIGRACAO.md`; preferências persistentes; handlers Electron de arquivo; implementação IMP-009A–G.
- **Criação física — pergunta:** qual é a raiz oficial, qual data forma Ano/Mês/Dia, quais programas/extensões podem ser escolhidos e como cada software deve criar um arquivo vazio com suas configurações padrão?
- **Alternativas de criação, sem escolha:** raiz corporativa global ou raiz por estação/empresa; data do início da Etapa de Arte, data de criação do vínculo ou outra data normativa; automação específica por programa ou templates oficiais controlados.
- **Backup — pergunta:** cada provedor será integrado por API ou por destino de arquivos já sincronizado/montado, e quais são retenção, credenciais e prova de conclusão?
- **Alternativas de backup, sem escolha:** adaptadores por API; cópia para pasta/unidade configurada; orquestrador externo com confirmação verificável devolvida ao Mheibos.
- **Revisão anual — pergunta:** qual data atribui o vínculo a um ano e o que “arquivar período” e “manter ano ativo” alteram operacionalmente?
- **Alternativas anuais, sem escolha:** data do início da Etapa de Arte; data de criação do vínculo; data comercial do Pedido; competência administrativa explícita.
- **Impacto:** não é seguro criar pastas/arquivos, declarar backup executado ou encerrar em lote por ano antes dessas respostas. Vínculo manual, integridade, pesquisa e encerramento individual continuam operacionais.
- **Situação:** `COMPLETED_WITH_GAPS` para IMP-009; retomar as partes afetadas quando houver decisão normativa, sem bloquear IMP-010 e ciclos independentes.

## DEC-IMP-027 — Missão nasce como workspace próprio sem duplicar operação

- **Decisão:** iniciar IMP-010 pela missão individual voluntária planejada, com contrato mínimo persistente e sem participantes, tarefas ou referências implícitas.
- **Motivo:** valida identidade, persistência, autorização, auditoria e retomada antes de introduzir consentimento coletivo e autoridade administrativa.
- **Separação:** Missão guarda apenas seu objetivo temporário e critério de conclusão; Pedido, Processo, Etapa e Pendência não são copiados nem recebem estado paralelo.
- **Autoridade:** na criação voluntária individual, criador e responsável principal são a mesma identidade ativa; origem e estado não são selecionados livremente pela interface.
- **Offline:** a primeira versão é somente consulta; o middleware existente recusa a mutação global sem criar exceção para Missões.
- **IA:** a origem `IA_ACEITA` reserva vocabulário normativo, mas não cria missão automaticamente nem participa desta fatia.
- **Situação:** definitiva para a fundação; colaboração e ciclo de vida evoluem por serviços transacionais próprios.

## DEC-IMP-028 — Estado da missão muda por autoridade explícita e preserva obrigações

- **Decisão:** no ciclo individual voluntário, somente o responsável principal inicia, pausa, retoma, bloqueia e conclui; administrador não recebe autoridade apenas por conseguir consultar.
- **Motivo:** RFC-0010 separa líder/autoridade de permissões administrativas globais e exige menor exposição e autoridade formal.
- **Transições:** `PLANEJADA → ATIVA`; `ATIVA → PAUSADA`; `PAUSADA → ATIVA`; `ATIVA|PAUSADA → BLOQUEADA`; `BLOQUEADA → ATIVA`; `ATIVA|EM_REVISAO → CONCLUIDA`. Estado final não reabre nesta fatia.
- **Idempotência:** cada transição relê e bloqueia a missão na transação; repetir comando que já alcançou seu estado-alvo retorna a mesma missão sem novo evento, e demais transições incompatíveis são recusadas.
- **Bloqueio:** a fotografia atual é estruturada nos cinco elementos normativos; ao retomar, os campos correntes são limpos, mas o evento imutável preserva a evidência.
- **Conclusão:** texto livre não é destino formal de obrigação. Enquanto tarefas ou pendências remanescentes não puderem ser concluídas, canceladas com autoridade, transferidas ou incorporadas, a missão não deve concluir.
- **Revisão:** `EM_REVISAO` permanece no vocabulário, porém sua entrada aguarda participante aprovador ou autoridade identificável; não criar revisão sem destinatário.
- **Situação:** definitiva para missão individual; missões atribuídas e coletivas terão matriz de autoridade própria.

## DEC-IMP-029 — Consentimento é vínculo histórico, não lista muitos-para-muitos implícita

- **Decisão:** representar cada participação por entidade própria com papel, estado, autoria, convite, resposta, manifestação e encerramento; manter no máximo um vínculo corrente por pessoa e missão.
- **Motivo:** uma relação simples apagaria recusa, saída, reconvite, autoria e cronologia exigidos pela RFC-0010.
- **Criação espontânea:** criador nasce como líder aceito; terceiros nascem somente como convidados. A missão fica `AGUARDANDO_ACEITE` até o primeiro aceite e então se torna `PLANEJADA`.
- **Consentimento:** pedir informação ou ajuste não equivale a aceitar; recusar encerra o convite sem julgamento e um reconvite cria nova ocorrência histórica.
- **Saída:** somente vínculo aceito não líder pode sair unilateralmente; liderança exige transferência futura para impedir workspace sem coordenação explícita.
- **Visibilidade:** vínculo corrente convidado ou aceito torna o workspace visível, mas não amplia permissões sobre Pedido, Processo, Etapa ou futura referência restrita.
- **Encerramento:** convite pendente deve receber destino antes da conclusão; participação de missão final é história imutável.
- **Atribuição administrativa:** adiada de modo intencional até tarefas, prazo e impacto existirem, pois a RFC exige apresentar esses elementos ao participante atribuído.
- **Situação:** definitiva para missões coletivas espontâneas; tipos atribuídos preservam vocabulário sem produzir obrigação incompleta.

## DEC-IMP-030 — Convergência visual elimina Vendas e especializa Produção

- **Decisão humana:** descontinuar o Mheibos Vendas como aplicação e experiência duplicada; migrar suas capacidades necessárias para o Mheibos Gestor integrado.
- **Produção:** manter uma visão especializada da mesma aplicação, ativada pela função/permissão do usuário ou pelo contexto da Etapa do Pedido, sempre sobre os mesmos contratos, estados e componentes oficiais.
- **Fluxo operacional:** reprojetar a relação entre “assistência de envio” e “assistência de entrega” como visualizações coerentes do Processo, Fluxo e Etapas do Pedido, em vez de ilhas independentes baseadas apenas em status legado.
- **Interface:** adotar `docs/UI-STANDARDS-MHEIBOS.md` e `docs/VISUAL-QUALITY-GATE-MHEIBOS.md` como normas complementares aos ENGs e RFCs, sem colocar autoridade de negócio na camada visual.
- **Tela-piloto:** usar inicialmente o detalhe do Pedido por concentrar navegação, projeção, estados, Processo/Etapa, entrega, conteúdo longo e intervenção contextual.
- **Compatibilidade:** rotas e marcadores legados podem existir somente durante migração explícita, com responsável e plano de remoção; não justificam uma segunda experiência permanente.
- **Situação:** definitiva para a direção de produto; execução registrada como IMP-006B e condicionada aos gates visuais e à aprovação humana da tela-piloto antes da migração em massa.

## DEC-IMP-031 — Arte bloqueia deterministicamente o avanço à Produção

- **Decisão:** Pedido sem arte de referência ativa permanece em `AGUARDANDO_ARTE` e não entra em Produção nem em estados posteriores.
- **Motivo:** decisão humana de 02/08/2026; a proteção não pode depender de memória do usuário, aparência da tela ou disponibilidade de IA.
- **Aplicação:** caso de uso único de transição, criação direta como pronto, ações individuais, em massa e rota de compatibilidade da antiga Assistência.
- **Interface:** Preparação de arte e Assistência de Impressão permanecem funções distintas no mesmo fluxo; nomes técnicos legados de rota podem permanecer temporariamente apenas por compatibilidade.
- **Lacuna isolada:** Pendência formal de pré-produção, scheduler, cadência e escalonamento aguardam a versão normativa completa da RFC-0012 e a modelagem da Etapa de arte; a fila e a trava determinísticas continuam funcionando.

## DEC-IMP-032 — Referência visual não integra o ciclo de vida do arquivo oficial

- **Decisão humana:** a arte de referência é somente uma imagem inserida na criação ou edição do Pedido e usada como referência visual operacional.
- **Edição:** adicionar, atualizar ou desvincular referências continua restrito ao fluxo de edição do Pedido já existente.
- **Separação:** referência visual não cria, converte, renomeia, move, substitui nem atualiza arquivo oficial de arte; também não herda automaticamente nome, caminho, formato ou integridade do arquivo oficial.
- **Arquivo oficial:** criação automática por programa gráfico, preferência de formato, nome oficial e estrutura Ano/Mês/Dia permanece fluxo próprio da RFC-0014 e da lacuna registrada no IMP-009.
- **Interface:** a Preparação de arte apresenta ações separadas para editar referências visuais e consultar/vincular arquivos oficiais, sem sugerir promoção automática entre os dois conceitos.

## DEC-IMP-033 — Ciclo operacional da arte oficial e preferências

- **Decisão humana (02/08/2026):** um arquivo físico só se torna arte oficial quando é criado ou vinculado explicitamente pela interface do Mheibos; presença, nome semelhante ou cópia manual na pasta nunca produz adoção automática.
- **Criação:** o Mheibos cria arquivo vazio com nome `#Pedido - Cliente - Tema.ext`; colisões recebem ` - 02`, ` - 03` e assim por diante. Programas oferecidos: CorelDRAW, Illustrator, Photoshop, Inkscape, GIMP, Affinity Designer, Affinity Photo e PDF.
- **Preferência:** o programa/formato padrão é preferência do usuário, visível em Perfil, mas qualquer usuário autorizado à Preparação de Arte pode alterá-lo para cada criação.
- **Diretório:** a empresa define raiz compartilhada acessível às instâncias. A estrutura criada sob ela é `Usuário/Ano/Mês/Dia`; o caminho pode chegar como UNC ou unidade mapeada e sua apresentação é responsabilidade do Mheibos.
- **Conclusão:** conteúdo, tamanho ou modificação não concluem a arte. A conclusão pertence ao conjunto da arte do Pedido e exige confirmação humana.
- **Inatividade:** após duas horas sem alteração e sem conclusão, alertar com `Concluir`, `Ainda estou trabalhando`, `Lembrar depois` (30 minutos) e, apenas nos dois primeiros alertas, `Deixar a arte para amanhã` mediante senha do responsável. O adiamento é proibido dentro do prazo crítico da categoria.
- **Ajuda e transferência:** prazo crítico oferece solicitação urgente de ajuda; gerente pode transferir responsabilidade imediatamente mediante senha. O arquivo permanece na pasta do criador; autoria e responsabilidade atual são distintas.
- **Integridade:** renomear arquivo oficial é proibido. Modificação posterior à conclusão exige que o autor escolha manter conclusão ou voltar à preparação. Qualquer profissional de Preparação de Arte pode abrir e modificar; cartão mostra a última alteração e detalhe/auditoria mostram histórico completo.
- **Ausência:** arquivo desaparecido produz alerta crítico persistente e não dispensável. O usuário deve restaurar o nome oficial e usar `Vincular arquivo restaurado`; divergência de conteúdo exige confirmação e escolha do estado da arte.
- **Exceção:** operação sem arquivo ausente exige senha e justificativa gerencial por ação ou transição; não remove o alerta.
- **Offline:** indisponibilidade do compartilhamento permite criação provisória local e transferência posterior. Após validação, o usuário decide remover ou mover a cópia para a área local de cópias; retenção é preferência empresarial e exclusão antecipada exige integridade do oficial.
- **Configurações:** Perfil lista todas as preferências do usuário, editáveis ou somente leitura; Perfil da Empresa faz o mesmo para preferências empresariais; Aparência lista somente opções permitidas pela norma visual. Cadastro/manutenção de usuários sai do Perfil e permanece na área Usuários.
- **Entrega incremental:** IMP-009H implementa preferência, raiz, nome, diretório, criação vazia, vínculo e auditoria. Monitoramento temporal, conclusão, exceções gerenciais, restauração e sincronização entram em fatias seguintes sobre o mesmo contrato, sem simular capacidade na interface.
