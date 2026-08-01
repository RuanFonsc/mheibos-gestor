# MHEIBOS INTELLIGENT OPERATING SYSTEM

# Inventário Oficial de Decisões Arquiteturais

**Status:** Oficial — Fonte normativa para elaboração dos RFCs  
**Versão:** 1.0  
**Data:** 30/07/2026  
**Fontes consolidadas:** RFC-0000, RFC-0001, RFC-0002, contexto e regras do projeto, e conversa integral de definição da Arquitetura Técnica.

---

## 1. Finalidade

Este documento é o inventário canônico das decisões arquiteturais já tomadas para o Mheibos.

Ele não é um RFC e não substitui os RFCs. Sua função é:

- registrar apenas decisões finais;
- eliminar alternativas descartadas ou substituídas;
- impedir duplicações e contradições entre documentos;
- indicar o RFC responsável por especificar cada decisão;
- servir como fonte obrigatória para todos os RFCs futuros.

Quando um RFC for escrito, ele deverá desenvolver somente as decisões que lhe foram atribuídas neste inventário. Uma decisão poderá ser citada por outros RFCs, mas deverá possuir um único RFC proprietário.

---

## 2. Mapa oficial dos RFCs

| RFC | Título | Responsabilidade principal |
|---|---|---|
| RFC-0000 | Manifesto do Projeto | Visão, propósito e razão de existir do Mheibos |
| RFC-0001 | Princípios Fundamentais | Restrições permanentes que nenhuma implementação pode violar |
| RFC-0002 | Modelo Operacional | Processos, objetivos, fluxos, estados e responsabilidades operacionais |
| RFC-0003 | Arquitetura Técnica da Plataforma | Topologia local, Central, Clientes, serviços, componentes e fronteiras técnicas |
| RFC-0004 | Arquitetura Cognitiva | Papel da IA, raciocínio, proatividade, explicabilidade e limites cognitivos |
| RFC-0005 | Modelo de Dados | Entidades, identidades, relacionamentos, estados, autoria e persistência |
| RFC-0006 | Eventos, Evidências e Auditoria | Registro de eventos, evidências, histórico imutável e rastreabilidade |
| RFC-0007 | Identidade, Permissões e Segurança | Autenticação, perfis, escopos, ações sensíveis e reautenticação |
| RFC-0008 | Operação Offline e Sincronização | Funcionamento sem a Central, dados locais, reconexão e incorporação global |
| RFC-0009 | Interface Viva e Intervenções | UI Orchestrator, personalização, alertas, criticidade e controle visual |
| RFC-0010 | Missões e Teamwork | Objetivos temporários, workspaces, colaboração, tarefas e progresso |
| RFC-0011 | Conhecimento, Memória e Aprendizado | Base de conhecimento, camadas, memória curta/longa e validação do aprendizado |
| RFC-0012 | Pendências, Lembretes e Escalonamento | Scheduler operacional, notificações, continuidade e decisões pendentes |
| RFC-0013 | Pedidos, Metas e Regras Financeiras | Pedido comercial, fluxos associados, metas, pagamentos, saldos e cobranças |
| RFC-0014 | Arquivos e Integrações | Referências de arquivos, documentos gerados, WhatsApp e integrações externas |
| RFC-0015 | Analytics, Dashboard e Simulação | Indicadores, análises assistenciais, cenários e simulação estratégica |
| RFC-0016 | Governança e Segurança da IA | Ensino, aprovação, confiança, princípios de recomendação e proteção humana |

---

# 3. Inventário de decisões

## A. Visão e princípios permanentes

### INV-001 — O Mheibos é uma memória operacional ativa

O Mheibos existe para acompanhar processos, lembrar compromissos, detectar bloqueios e iniciar intervenções, preservando a atenção humana.

**RFC proprietário:** RFC-0000 — Manifesto do Projeto  
**Situação:** já documentada.

### INV-002 — O sistema participa da operação sem substituir pessoas

O Mheibos deve orientar, lembrar, organizar e prevenir erros. Decisões críticas e sacrifícios conscientes permanecem sob responsabilidade humana.

**RFC proprietário:** RFC-0001 — Princípios Fundamentais  
**Situação:** já documentada.

### INV-003 — Segurança e qualidade têm prioridade sobre velocidade

Quando houver conflito entre rapidez e segurança, confiabilidade ou menor incidência de erros, o Mheibos deverá escolher a alternativa mais segura e consistente.

**RFC proprietário:** RFC-0001 — Princípios Fundamentais.

### INV-004 — Qualidade e atendimento não podem ser sacrificados pelo lucro

A IA não deverá recomendar uma alternativa mais lucrativa que reduza deliberadamente a qualidade do serviço ou do atendimento. Uma decisão humana externa ao sistema poderá contrariar essa orientação, mas não deverá ser originada como prática recomendada pelo Mheibos.

**RFC proprietário:** RFC-0001 — Princípios Fundamentais.

### INV-005 — Toda pendência relevante termina em decisão consciente

Uma pendência não poderá desaparecer apenas porque foi ignorada. Ela deverá terminar em resolução, adiamento consciente, delegação, justificativa, cancelamento autorizado ou solicitação de ajuda.

**RFC proprietário:** RFC-0001 — Princípios Fundamentais.

### INV-006 — A arquitetura deve manter o Mheibos acessível

As decisões de infraestrutura e IA da versão inicial deverão evitar custos e exigências computacionais incompatíveis com pequenas e médias gráficas.

**RFC proprietário:** RFC-0001 — Princípios Fundamentais.

---

## B. Modelo operacional

### INV-007 — Pedido e Processo possuem centralidades diferentes

O Pedido é a entidade central da relação comercial e financeira. O Processo é a entidade central da execução operacional. A arquitetura deverá priorizar a conclusão correta das demandas já assumidas.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-008 — A operação é compreendida por processos e estados

Módulos organizam funcionalidades da interface; processos e estados representam a realidade operacional. A IA deverá raciocinar sobre a realidade operacional, e não somente sobre telas.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-009 — Fluxos operacionais partem de modelos adaptáveis

Cada categoria de pedido deverá possuir um fluxo padrão formado por etapas obrigatórias, opcionais e condicionais. O usuário autorizado poderá ajustar o fluxo antes de sua confirmação.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-010 — O fluxo confirmado torna-se o processo oficial do pedido

Depois de confirmado, o conjunto de etapas escolhido deverá ser preservado como o processo oficial daquela instância, mantendo histórico de inclusões, remoções, dispensas e conclusões.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-011 — Ausência de criação de arte não significa arte disponível

O modelo operacional deverá distinguir, no mínimo, “arte fornecida e pronta”, “aguardando arquivo do cliente” e “criação de arte pela empresa”, pois produzem estados e caminhos diferentes.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-012 — Serviços imediatos possuem fluxos simplificados

Serviços concluídos no momento da venda poderão dispensar ou concluir etapas em sequência, inclusive por uma ação como “Pronto e Entregue”, sem perder histórico nem rastreabilidade e sem gerar notificações desnecessárias.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

### INV-013 — Procedimentos orientam, mas não engessam a execução

Quando o resultado exigido puder ser alcançado de formas diferentes e o usuário possuir autorização, o procedimento recomendado não deverá impedir improvisações ou métodos alternativos. O sistema poderá sugerir a forma mais segura e eficiente.

**RFC proprietário:** RFC-0002 — Modelo Operacional.

---

## C. Arquitetura da plataforma

### INV-014 — A versão inicial é desktop e local

O Mheibos será inicialmente uma aplicação desktop instalada nos computadores da empresa e operará em uma implantação local, testada e aprimorada primeiro na empresa piloto.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-015 — A plataforma é distribuída entre Central e Clientes

Uma Máquina Principal hospedará a Central e suas dependências. As estações executarão Clientes Mheibos subordinados à Central.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-016 — A Central é a autoridade global

A Central consolidará o estado global, autenticação, regras, permissões, serviços compartilhados, sincronização e conhecimento organizacional. Clientes terão autonomia local limitada e jamais criarão regras conflitantes com a Central.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-017 — A Máquina Principal é também uma estação administrativa

Na versão inicial, a Máquina Principal poderá oferecer acesso administrativo direto e facilitar o controle do servidor local e de suas dependências.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-018 — A indisponibilidade da Máquina Principal é prevista

Quedas de energia ou desligamentos da Máquina Principal são eventos normais que a arquitetura deverá suportar por meio do modo offline restrito.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-019 — A evolução para nuvem é posterior

A arquitetura em nuvem e o atendimento a múltiplas empresas fazem parte da evolução comercial futura. Não constituem a topologia da primeira versão e deverão ser definidos por revisão ou novo RFC.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-020 — O Gestor é uma aplicação integrada

Pedidos, clientes, processos, dashboards, notificações, IA e demais funções atuais estarão acessíveis em um único ambiente principal.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-021 — Módulos visíveis continuam sendo a navegação principal

A IA poderá acelerar a navegação e montar contextos de trabalho, mas os módulos e funções normais da interface permanecerão utilizáveis sem interação direta com a IA.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-022 — Aplicações especializadas futuras obedecerão à mesma Central

Mheibos Vendas, Mheibos Produção e outras aplicações poderão existir separadamente no futuro, mas deverão usar a mesma autoridade, identidades, permissões, processos e protocolos centrais.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

### INV-023 — A fundação deve operar com IA desligada

Na fase atual não será instalado modelo de IA local nem integração com IA por API. A estrutura deverá funcionar integralmente com a IA desligada. Qualquer provedor futuro será opcional e substituível, sem perda do conhecimento do Mheibos e sem autoridade sobre o estado oficial.

A IA é parte obrigatória da arquitetura final e será implementada na última fase. As fases anteriores deverão criar contratos, pontos de extensão, dados e fluxos correspondentes às funções cognitivas previstas, usando execução determinística ou humana enquanto a IA estiver desligada.

A ausência de IA não poderá parar, bloquear, adiar ou degradar processos operacionais nem travar partes independentes do desenvolvimento. Se existir lacuna lógica incontornável, impossível de resolver pelas fontes oficiais ou por alternativa determinística ou humana sem inventar regra, somente a parte afetada será interrompida; fontes e alternativas serão registradas como `DECISAO_HUMANA_NECESSARIA`, e o responsável humano será consultado.

**RFC proprietário:** RFC-0003 — Arquitetura Técnica da Plataforma.

---

## D. Eventos, evidências e auditoria

### INV-024 — Alterações relevantes geram eventos

Toda alteração operacional, comercial, financeira, administrativa ou de segurança relevante deverá produzir um evento com autoria, momento, origem e mudança realizada.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

### INV-025 — O usuário deve perceber a operação como imediata

O registro e o processamento de eventos não poderão introduzir atraso perceptível, perda de sincronização ou subnotificação. Consequências secundárias poderão ser processadas de forma desacoplada.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

### INV-026 — O histórico de auditoria é imutável

O sistema deverá preservar quem fez o quê, quando, em qual estação, em qual contexto, qual era o valor anterior e qual passou a ser o novo valor.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

### INV-027 — Exclusões são eventos, não destruição física

Apagar na interface significa remover do uso normal ou cancelar. O conteúdo anterior e o evento de apagamento deverão permanecer preservados para auditoria.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

### INV-028 — A auditoria inclui origem online ou offline

Eventos deverão registrar se foram produzidos com a Central disponível ou durante uma sessão offline, além da estação e usuário de origem.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

### INV-029 — Mudanças de regras e segurança também são auditadas

Alterações de perfis, permissões, exceções, ações sensíveis, critérios de metas e políticas administrativas deverão produzir registros imutáveis.

**RFC proprietário:** RFC-0006 — Eventos, Evidências e Auditoria.

---

## E. Identidade, acesso e segurança

### INV-030 — A autenticação é própria do Mheibos

Cada usuário possuirá credenciais individuais independentes da conta do Windows. A Central determinará identidade, perfil, permissões, responsabilidades e interface disponível.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-031 — Cada usuário possui exatamente um perfil

Não será permitido acumular múltiplos perfis. Necessidades específicas serão tratadas por exceções individuais auditadas.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-032 — Permissões são definidas por função e escopo

O controle de acesso deverá considerar ação, tipo de dado, propriedade, contexto e alcance. Não será suficiente ocultar telas ou botões; a autorização deverá ser aplicada na camada central e na persistência.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-033 — Perfis fornecem permissões padrão com exceções individuais

Perfis como Administrador, Gerente, Designer/Vendedor, Produção e Financeiro terão permissões padrão. Concessões ou restrições individuais serão possíveis e auditadas.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-034 — Usuários comuns acessam seus próprios indicadores por padrão

Um Designer/Vendedor poderá criar e editar pedidos, consultar suas vendas, metas, crescimento e relatórios próprios, sem acesso automático aos resultados globais ou de outros usuários. Gerentes e administradores poderão possuir visão global.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-035 — Ações sensíveis exigem reautenticação

Toda ação classificada como sensível deverá exigir confirmação com a senha do usuário que a executa.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-036 — Usuários comuns justificam ações sensíveis

Usuários comuns autorizados deverão informar motivo textual obrigatório. Administradores autorizados poderão executar sem justificativa obrigatória, mas nunca sem reautenticação e auditoria.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-037 — A política de ações sensíveis é configurável

O sistema fornecerá uma lista padrão, e administradores autorizados poderão incluir ou retirar classificações e determinar quais perfis podem executar cada ação. Toda mudança será auditada.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-038 — Edição concorrente usa bloqueio temporário

Ao entrar no modo de edição de um registro sensível, somente um usuário poderá alterá-lo. Os demais continuarão com leitura e verão quem mantém o bloqueio.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-039 — Bloqueios não podem ser abandonados indefinidamente

Bloqueios deverão ser liberados ao salvar, cancelar, fechar, desconectar, encerrar sessão, expirar por inatividade ou por intervenção administrativa autorizada.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

### INV-040 — A IA herda os limites do usuário autenticado

A IA não possui privilégios ocultos. Ela só poderá executar, preparar ou sugerir ações compatíveis com as permissões e o contexto do usuário atual.

**RFC proprietário:** RFC-0007 — Identidade, Permissões e Segurança.

---

## F. Operação offline e sincronização

### INV-041 — O modo offline é restrito, não completo

Sem a Central, os Clientes poderão consultar a última visão sincronizada e criar novos pedidos locais, mas não poderão alterar pedidos ou processos que já pertenciam ao estado global.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-042 — Pedidos offline são exclusivos da estação de origem

Durante a indisponibilidade, cada estação poderá visualizar e editar somente os novos pedidos que ela própria criou. Pedidos offline de outras estações permanecerão invisíveis até a sincronização.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-043 — O modo offline preserva a autoridade já concedida

Dentro do escopo permitido offline, o usuário poderá registrar cliente, itens, valores, pagamentos, descontos, fluxo, etapas e estado final com a mesma autoridade que possuiria online.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-044 — O identificador visível do pedido combina origem e sequência

Cada usuário autorizado a gerar pedidos possuirá um código exclusivo e permanente. O número visível será formado pelo código e pela sequência local, como `#J324`, evitando colisões offline.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-045 — Códigos de origem não são reutilizados

Um código que já tenha originado pedidos nunca poderá ser atribuído a outro usuário, mesmo após desligamento ou saída do colaborador.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-046 — A sincronização de retorno é automática e visível

Ao restabelecer a Central, o Cliente deverá avisar o usuário, iniciar a sincronização automaticamente e informar o resultado. A operação não dependerá de confirmação manual.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-047 — Falhas de sincronização permanecem locais e visíveis

Dados não sincronizados não poderão ser descartados. Deverão permanecer protegidos, marcados como pendentes, com nova tentativa automática, tentativa manual e motivo da falha.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-048 — A sincronização preserva integralmente o estado local

Pedido, cliente, itens, valores, pagamentos, descontos, fluxo, processos, etapas, datas, responsáveis, estado final e eventos serão incorporados exatamente como foram deixados pelo usuário, sem aprovação adicional apenas por terem sido criados offline.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-049 — Após sincronizar, o pedido torna-se global

Concluída a sincronização, o pedido poderá ser visualizado e editado por qualquer usuário autorizado e passará a seguir o bloqueio normal. O prefixo indica origem comercial, não propriedade permanente.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-050 — O login offline é vinculado à última identidade validada na estação

Uma sessão aberta continuará funcionando offline. O último usuário validado naquela estação poderá autenticar-se novamente com credenciais locais protegidas e permissões sincronizadas; a troca para outro usuário exigirá a Central.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

### INV-051 — Logout é bloqueado enquanto houver dados pendentes

O usuário não poderá encerrar a sessão enquanto existirem pedidos ou eventos locais ainda não sincronizados, salvo procedimento administrativo excepcional de recuperação.

**RFC proprietário:** RFC-0008 — Operação Offline e Sincronização.

---

## G. Interface viva e intervenções

### INV-052 — A IA controla a interface por uma API interna

A interface deverá expor ações controladas para abrir e fechar janelas, navegar, selecionar abas, focar campos, rolar listas, aplicar filtros e destacar elementos.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-053 — A interface é um meio de comunicação da IA

A IA poderá fazer botões, campos, linhas ou áreas pulsarem, brilharem ou receberem destaque; escurecer o restante da tela; apontar o próximo passo; e conduzir o usuário visualmente.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-054 — Alterações persistentes começam como sugestão

Antes de modificar dados, configurações, estados, responsáveis, mensagens ou decisões persistentes, a IA deverá explicar o que pretende fazer, mostrar o impacto e solicitar confirmação.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-055 — Adaptações temporárias podem ser locais e automáticas

A IA poderá reorganizar listas, abrir telas, destacar problemas ou aplicar filtros temporários sem alterar dados reais. Essas adaptações afetam somente a experiência do usuário atual.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-056 — Intervenções possuem níveis de criticidade

O padrão será um comentário flutuante não bloqueante. Situações mais relevantes poderão oferecer ações rápidas. Situações críticas poderão exigir reconhecimento ou uma ação mínima.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-057 — Situações normais exigem reconhecimento para restaurar a visão

Quando a IA reorganizar temporariamente uma interface por uma situação normal, qualquer usuário poderá retornar à visualização original após reconhecer o aviso.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-058 — Situações críticas tratam perfis de forma diferente

Usuários comuns somente poderão remover a apresentação crítica após uma ação mínima, como iniciar um plano, justificar, pedir ajuda, encaminhar ou resolver. Administradores poderão restaurar a interface após reconhecimento.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-059 — A personalização é individual

A IA poderá organizar interface, disposição, filtros, atalhos e contextos de forma diferente para usuários com a mesma função, sem mudar regras de negócio nem permissões.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-060 — Objetivos podem gerar uma interface focada

O usuário poderá declarar um objetivo, e a IA montará uma visão temporária reunindo módulos, listas, bloqueios e ações relevantes. Essa visão é uma “missão”, não uma substituição da interface normal.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-061 — Missões podem ser pausadas e retomadas

O usuário poderá suspender a interface focada para executar trabalho comum e retornar posteriormente à missão com contexto e progresso preservados.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-062 — Erros recorrentes acionam assistência progressiva

Ao detectar repetição de erro relevante, o sistema deverá intervir cedo — por padrão, já na terceira ocorrência configurável — com abordagem educada, gentil e preventiva, podendo iniciar treinamento guiado.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-063 — Assistência deve adaptar-se ao padrão de atenção do usuário

A IA deverá aprender padrões individuais de esquecimento, distração ou dificuldade de percepção e antecipar apoio, sem diagnosticar, rotular ou expor condições pessoais.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

### INV-064 — O tutorial possui divulgação progressiva

Ao ensinar um procedimento, a IA mostrará primeiro o caminho oficial essencial. Conteúdo complementar, alternativas e exploração da interface serão oferecidos por uma ação como “Ver mais”, em formato de tour guiado.

**RFC proprietário:** RFC-0009 — Interface Viva e Intervenções.

---

## H. Missões e Teamwork

### INV-065 — Missão representa um objetivo operacional temporário

Uma missão reúne objetivo, plano, tarefas, prazos, contexto, progresso e interface focada, podendo ser criada pelo usuário, sugerida pela IA ou atribuída pela gestão.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-066 — Teamwork só é ativado por concordância ou autoridade formal

Uma missão coletiva será criada quando os usuários concordarem em colaborar ou quando um gerente/administrador atribuí-la. A IA não poderá impor colaboração entre colegas.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-067 — Regras de saída dependem da origem da missão

Participantes poderão sair de missões coletivas espontâneas. Em missões atribuídas por gerente ou administrador, somente a autoridade responsável poderá retirar participantes ou encerrar a obrigação, preservado o direito de justificar, pedir ajuda ou solicitar revisão.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-068 — Teamwork mostra progresso e divide tarefas

A função deverá apresentar objetivo coletivo, progresso, dependências, tarefas e responsáveis, permitindo que a IA sugira distribuição conforme carga, habilidade e disponibilidade.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-069 — Ajuda entre colegas exige consentimento

Quando alguém concluir sua parte, a IA poderá sugerir que ofereça ajuda. A transferência ou compartilhamento de uma tarefa já atribuída exigirá aceite do responsável atual ou decisão da autoridade da missão.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-070 — A IA não transforma métricas em julgamento pessoal

A comunicação deverá descrever risco, atraso, carga e impacto do processo, evitando comparações depreciativas, rankings públicos ou rótulos de produtividade entre colegas.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-071 — Cada missão é um workspace persistente

A missão reunirá objetivo, participantes, plano, tarefas, progresso, histórico, conversas, notas, decisões e referências relacionadas.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

### INV-072 — Missões possuem chat e notas próprios

Conversas serão vinculadas à missão. Notas dos usuários serão preservadas separadamente como conhecimento consolidado, respeitando permissões e privacidade.

**RFC proprietário:** RFC-0010 — Missões e Teamwork.

---

## I. Conhecimento, memória e aprendizado

### INV-073 — O Mheibos possui base de conhecimento própria

Conhecimento do produto, empresa, operação e documentação deverá existir fora do modelo de linguagem, permitindo trocar o modelo sem perder a inteligência acumulada.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-074 — O conhecimento é separado em camadas, mas consultado de forma combinável

A base deverá distinguir, no mínimo: conhecimento universal do Mheibos, conhecimento da empresa, conhecimento operacional e contexto atual da conversa. A separação organiza e reduz contexto, mas não poderá impedir consultas cruzadas quando o problema exigir múltiplas camadas.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-075 — O sistema controla a recuperação de contexto

O modelo não deverá explorar indiscriminadamente todas as fontes. O Mheibos deverá selecionar fontes relevantes, limitar profundidade, definir critérios de parada e entregar relações operacionais próximas.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-076 — Não haverá grafo de conhecimento geral como pilar inicial

A primeira versão usará relações operacionais determinísticas já existentes — dependências, bloqueios, pertencimentos e autoria — em vez de permitir exploração livre de um grafo amplo pela IA.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-077 — Investigações amplas exigem consentimento

Quando o contexto inicial não for suficiente, a IA deverá informar o que encontrou e perguntar se o usuário deseja uma investigação mais ampla, em vez de iniciar automaticamente buscas potencialmente lentas.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-078 — Memória de curto e longo prazo são separadas

A memória curta sustentará sessão, telas, missão, conversa e adaptação diária. A memória longa consolidará conhecimento, histórico, CRM, padrões de comportamento e evolução organizacional.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-079 — O aprendizado inicial é privado e local à empresa

Na primeira fase, o aprendizado permanecerá na implantação local. Uma camada global e anônima poderá ser criada futuramente quando houver infraestrutura e governança adequadas.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-080 — O Mheibos aprende com acertos, erros e improvisações

Práticas bem-sucedidas alimentam recomendações. Práticas malsucedidas servem para prevenir repetição. Improvisações úteis podem ser classificadas como soluções emergentes e posteriormente propostas como boas práticas.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-081 — O Mheibos aprende também sobre o próprio produto

A IA poderá observar padrões de uso da interface, campos confusos, sequências frequentes, atalhos, telas pouco utilizadas e fricções, a fim de sugerir adaptações e melhorias do próprio sistema.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-082 — Conhecimento ensinado por usuários entra em validação

Um ensinamento novo deverá ser avaliado pela própria IA quanto a coerência e risco e encaminhado para validação de gestor antes de ser utilizado como conhecimento oficial para outros usuários.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-083 — Procedimentos emergentes podem ser sugeridos sem se tornarem obrigatórios

A IA poderá salvar e apresentar práticas úteis como recomendação ou resposta a dúvidas. Elas só se tornarão procedimento oficial mediante governança apropriada e não impedirão métodos autorizados que alcancem o resultado esperado.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

### INV-084 — Boas práticas globais serão biblioteca optativa

Em futuras implantações, melhorias aprovadas não serão aplicadas automaticamente. Serão apresentadas como biblioteca de boas práticas para escolha durante a implantação, respeitando a realidade de cada empresa.

**RFC proprietário:** RFC-0011 — Conhecimento, Memória e Aprendizado.

---

## J. Pendências, lembretes e escalonamento

### INV-085 — O sistema produz briefing de início do dia

No login ou em horário configurado, o Mheibos deverá apresentar prioridades, riscos, prazos, bloqueios, cobranças e missões relevantes ao perfil do usuário.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-086 — O briefing preserva continuidade pessoal

Pendências de ontem, missões pausadas, promessas, lembretes e notas pessoais deverão reaparecer no início do trabalho conforme contexto e prioridade.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-087 — Notas podem possuir gatilhos de lembrança

Uma nota poderá ser apenas registro, reaparecer em data ou horário, ser vinculada à abertura de cliente, pedido, módulo ou missão, ou permanecer ativa até resolução.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-088 — Notas pessoais são privadas por padrão

Notas pessoais somente serão compartilhadas por ação explícita do usuário ou quando criadas dentro de um espaço coletivo.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-089 — Pendências aumentam de importância com o risco

Tempo sem ação, prazo, impacto, dependências bloqueadas e adiamentos deverão elevar gradualmente a visibilidade e a exigência de resposta.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-090 — Pendências ignoradas podem forçar visualização

Ao atingir criticidade configurada, a interface poderá ser reorganizada para garantir que a pendência seja vista e que exista uma decisão consciente.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-091 — Escalonamento não remove o responsável original

Quando uma pendência for escalada, o responsável principal continuará recebendo alertas; gerente, financeiro ou outros supervisores serão adicionados sem transferência automática da responsabilidade.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

### INV-092 — Próximos lembretes são sugeridos e ajustáveis

Após uma tentativa de contato ou ação, o sistema sugerirá data, prioridade, mensagem e próximo responsável conforme o resultado, permitindo ajuste humano antes de salvar.

**RFC proprietário:** RFC-0012 — Pendências, Lembretes e Escalonamento.

---

## K. Pedidos, metas e regras financeiras

### INV-093 — Autoria comercial e execução operacional são separadas

O pedido deverá registrar criador comercial, autores de alterações, responsáveis operacionais e quem concluiu cada processo. A venda permanece atribuída ao criador para metas, salvo transferência específica, autorizada e auditada.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-094 — Cancelamento não altera automaticamente a meta

Em cancelamentos, devoluções ou estornos, gerente ou administrador autorizado decidirá se o valor permanece ou é retirado da meta, com senha, motivo e auditoria.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-095 — Critérios de metas são configuráveis por empresa

Metas poderão considerar pedidos criados, aprovados, produzidos, concluídos, entregues, pagos, valores recebidos ou combinações, com períodos, comissões e regras de cancelamento configuráveis.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-096 — Estados operacional e financeiro são independentes

Um pedido poderá estar operacionalmente concluído e financeiramente pendente. A interface e o modelo de dados não poderão reduzir ambos a um único status.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-097 — Alterações posteriores preservam pagamentos anteriores

Quando o valor total aumentar, pagamentos já registrados permanecerão intactos, o saldo adicional será calculado e o pedido receberá estado financeiro equivalente a “Aguardando pagamento adicional”.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-098 — Entrega com saldo aberto exige autorização superior

Usuário comum não poderá concluir a entrega com saldo pendente. Gerente ou administrador poderá autorizar com senha, motivo obrigatório, indicação visível e auditoria.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-099 — Entrega com saldo cria pendência financeira

A autorização deverá gerar automaticamente uma pendência vinculada ao pedido, com valor, cliente, vencimento, prioridade, responsável, supervisores, histórico, estados e alertas até a quitação ou encerramento autorizado.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-100 — O responsável de cobrança é configurável

Por padrão, a cobrança será atribuída ao usuário que fechou o pedido. A empresa poderá definir vendedor, financeiro, gerente, usuário específico ou responsável escolhido no momento da exceção.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

### INV-101 — Uma pendência pode ter vários destinatários e um responsável

Responsável principal, gerente e financeiro poderão receber notificações sobre a mesma pendência, sem duplicar o registro ou diluir a responsabilidade.

**RFC proprietário:** RFC-0013 — Pedidos, Metas e Regras Financeiras.

---

## L. Arquivos e integrações

### INV-102 — O Mheibos não é o repositório principal de arquivos

O sistema armazenará caminhos, referências, metadados e contexto operacional dos arquivos existentes na estrutura local, permitindo abertura pelo sistema operacional e pelo aplicativo associado.

**RFC proprietário:** RFC-0014 — Arquivos e Integrações.

### INV-103 — Documentos gerados permanecem no contexto da operação

Ordens de serviço em PDF, relatórios e outros documentos produzidos pelo sistema serão vinculados ao pedido, dashboard ou processo correspondente, sem exigir módulo documental próprio.

**RFC proprietário:** RFC-0014 — Arquivos e Integrações.

### INV-104 — O WhatsApp poderá ser integrado à interface do Gestor

A conversa poderá ocorrer dentro do Mheibos para que a IA associe pedidos, estados e dados contextuais e prepare sugestões de resposta.

**RFC proprietário:** RFC-0014 — Arquivos e Integrações.

### INV-105 — A IA não disputa a conversa com o humano

Durante atendimento conduzido por uma pessoa, a IA poderá observar, contextualizar, sugerir e preparar respostas, mas não enviará mensagem simultânea ou sem autorização.

**RFC proprietário:** RFC-0014 — Arquivos e Integrações.

### INV-106 — Webhooks e interface integrada são complementares

A supervisão por webhook poderá continuar existindo; a interface interna adicionará assistência contextual e controle humano direto.

**RFC proprietário:** RFC-0014 — Arquivos e Integrações.

---

## M. Arquitetura cognitiva e proatividade

### INV-107 — Existe um único Mheibos para toda a empresa

Os usuários interagem com uma única entidade cognitiva, que adapta respostas e acesso conforme identidade, perfil, permissões, contexto e responsabilidade.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-108 — A IA interpreta; os dados e regras oficiais pertencem ao sistema

A IA nunca será fonte oficial do estado. Motores determinísticos, dados e evidências validarão permissões, estados e transições.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-109 — A IA sugere antes de impor

Fluxos, reorganizações permanentes, procedimentos, mensagens e planos deverão ser apresentados como sugestões ou propostas, preservando decisão humana nas alterações reais.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-110 — O Mheibos detecta problemas e gera planos de ação

Ao identificar gargalos ou padrões anormais, a IA deverá apontar causas possíveis, produzir plano com tarefas e prazos para o responsável e informar a gestão sobre problema, plano e evolução.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-111 — O responsável recebe ajuda antes de substituição

O objetivo do plano de ação é permitir que o próprio usuário recupere a operação. A notificação ao gerente não transfere automaticamente sua responsabilidade.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-112 — Problemas recorrentes geram melhoria contínua

A IA deverá formular hipótese de causa raiz, propor melhoria permanente, acompanhar indicadores após aprovação e informar se a mudança funcionou.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-113 — A IA atua como planejadora operacional diária

Antes de solicitação explícita, ela poderá analisar a operação e propor prioridades e preparação do ambiente de trabalho, personalizadas por perfil e usuário.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-114 — Previsões de risco podem gerar planos para aprovação

Ao prever um problema, a IA poderá montar prioridades, responsáveis, prazos e impacto esperado, mas não executará alterações persistentes sem aprovação.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-115 — Alertas estratégicos são recomendações muito fortes

Mesmo com alta confiança, a IA não exigirá formalmente que o gestor aceite ou justifique uma decisão estratégica. Ela deverá destacar a gravidade e apresentar recomendação muito forte, mantendo a decisão humana.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-116 — Toda recomendação relevante é explicável

A IA deverá informar dados utilizados, fatos, relações, impacto de ignorar, nível de confiança, incertezas e, quando aplicável, simulação que sustentou a recomendação.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-117 — A IA responde cedo e aprofunda sob demanda

Ela deverá usar primeiro o contexto disponível, cruzar apenas fontes relevantes, responder com o que já sabe e pedir autorização para investigações mais amplas.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

### INV-118 — A IA preserva dignidade e privacidade internas

Análises deverão priorizar processos e causas, evitando exposição pública de pessoas. Identificação individual somente ocorrerá para usuários com autorização e quando necessária para assistência ou gestão.

**RFC proprietário:** RFC-0004 — Arquitetura Cognitiva.

---

## N. Governança e segurança da IA

### INV-119 — A IA avalia ensinamentos antes da aprovação humana

Conhecimento submetido por usuários deverá receber uma avaliação preliminar de coerência, conflito, evidência e risco antes da fila de aprovação.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

### INV-120 — Somente conhecimento aprovado torna-se oficial

Procedimentos, políticas e ensinamentos não poderão ser promovidos a padrão oficial da empresa sem aprovação de autoridade definida.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

### INV-121 — Melhorias de processo são propostas formais

Quando a IA detectar uma melhoria relevante, deverá criar proposta com impacto, benefícios, riscos, evidências e ganho estimado para aprovação ou rejeição da gestão.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

### INV-122 — A IA não impõe relações humanas de trabalho

A IA poderá sugerir colaboração, ajuda ou redistribuição, mas não poderá impor parceria espontânea, constranger usuários ou criar comparações pessoais como mecanismo de gestão.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

### INV-123 — A IA deve alertar com educação e gentileza

Mesmo quando a intervenção for obrigatória, a comunicação deverá ser respeitosa, objetiva, não acusatória e orientada à solução.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

### INV-124 — A IA não diagnostica pessoas

Padrões de atenção, esquecimento ou dificuldade poderão orientar personalização preventiva, mas o sistema não deverá produzir diagnósticos médicos, rótulos pessoais ou exposição indevida.

**RFC proprietário:** RFC-0016 — Governança e Segurança da IA.

---

## O. Analytics, dashboard e simulação

### INV-125 — O Gestor realizará análises financeiras assistenciais

O dashboard deverá permitir que a IA interprete indicadores financeiros e operacionais, explique situações e recomende ações sem substituir dados oficiais nem decisões humanas.

**RFC proprietário:** RFC-0015 — Analytics, Dashboard e Simulação.

### INV-126 — O Mheibos poderá simular cenários estratégicos

A arquitetura futura deverá suportar perguntas sobre contratação, preços, capacidade, estoque, fluxo de caixa, produção e atendimento, projetando impactos antes de qualquer decisão real.

**RFC proprietário:** RFC-0015 — Analytics, Dashboard e Simulação.

### INV-127 — Simulações respeitam princípios e restrições da empresa

Cenários que maximizem resultado financeiro violando qualidade, atendimento, segurança ou políticas não deverão ser apresentados como recomendação do Mheibos.

**RFC proprietário:** RFC-0015 — Analytics, Dashboard e Simulação.

---

# 4. Regras de uso deste inventário

1. **Nenhum RFC futuro poderá contradizer uma decisão deste inventário sem revisão explícita do próprio inventário.**
2. **Alternativas discutidas, mas não presentes aqui, não possuem status arquitetural.**
3. **Cada decisão deverá ser desenvolvida prioritariamente no RFC proprietário indicado.**
4. **RFCs poderão referenciar decisões de outros documentos, mas não duplicar sua especificação normativa.**
5. **Novas decisões deverão receber um novo identificador `INV-XXX` e um RFC proprietário.**
6. **Quando uma decisão for alterada, a versão anterior deverá ser marcada como substituída no histórico de revisão, sem ser silenciosamente apagada.**
7. **A elaboração dos RFCs deverá preservar a separação entre versão inicial local e evoluções futuras em nuvem.**

---

# 5. Ordem recomendada de documentação

Para reduzir dependências e evitar retrabalho, os próximos documentos deverão ser produzidos nesta ordem:

1. RFC-0003 — Arquitetura Técnica da Plataforma;
2. RFC-0006 — Eventos, Evidências e Auditoria;
3. RFC-0007 — Identidade, Permissões e Segurança;
4. RFC-0008 — Operação Offline e Sincronização;
5. RFC-0005 — Modelo de Dados;
6. RFC-0009 — Interface Viva e Intervenções;
7. RFC-0004 — Arquitetura Cognitiva;
8. RFC-0011 — Conhecimento, Memória e Aprendizado;
9. RFC-0016 — Governança e Segurança da IA;
10. RFC-0012 — Pendências, Lembretes e Escalonamento;
11. RFC-0010 — Missões e Teamwork;
12. RFC-0013 — Pedidos, Metas e Regras Financeiras;
13. RFC-0014 — Arquivos e Integrações;
14. RFC-0015 — Analytics, Dashboard e Simulação.

---

# 6. Declaração normativa

Este inventário passa a ser a fonte oficial de escopo e distribuição das decisões arquiteturais do Mheibos.

Os RFCs futuros deverão transformar estas decisões em especificações coerentes, testáveis e implementáveis, sem reabrir alternativas já encerradas, salvo quando houver uma proposta formal de revisão arquitetural.
