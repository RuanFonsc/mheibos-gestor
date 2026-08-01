# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0008 — Operação Offline e Sincronização

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0005, RFC-0006, RFC-0007  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-041 a INV-051

---

## 1. Resumo

Esta RFC define como os Clientes Mheibos deverão funcionar quando a Central estiver temporariamente indisponível e como os dados produzidos nesse período serão incorporados ao estado global após a reconexão.

O modo offline da primeira versão será **restrito, explícito e orientado à continuidade comercial**. Sem acesso à Central, o usuário poderá consultar a última visão sincronizada e criar novos pedidos locais, mas não poderá alterar pedidos, processos ou demais registros que já pertenciam ao estado global.

Cada pedido criado offline permanecerá exclusivo da estação que o originou até a sincronização. Outras estações não poderão visualizá-lo nem alterá-lo enquanto a Central estiver indisponível.

Dentro do escopo permitido, o usuário conservará a autoridade que possuía quando suas permissões foram sincronizadas. Ele poderá registrar cliente, itens, valores, pagamentos, descontos, fluxo, etapas, responsáveis e estado final do novo pedido local sem depender de aprovação posterior apenas pelo fato de a operação ter ocorrido offline.

Os pedidos utilizarão identificadores visíveis formados por um código permanente de origem e uma sequência local, como `#J324`. Essa composição impedirá colisões entre estações desconectadas e preservará a autoria comercial do pedido.

Quando a Central retornar, o Cliente deverá informar a reconexão, iniciar automaticamente a sincronização e apresentar o resultado. Dados que não puderem ser incorporados permanecerão protegidos localmente, visíveis como pendentes e disponíveis para novas tentativas.

O usuário não poderá encerrar normalmente a sessão enquanto existirem pedidos ou eventos locais ainda não sincronizados, salvo procedimento administrativo excepcional de recuperação, protegido e auditado.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- o que o usuário pode fazer quando a Central estiver indisponível;
- quais dados permanecem apenas para consulta;
- quais operações podem criar estado local novo;
- por que registros globais existentes não podem ser alterados offline;
- como pedidos offline ficam isolados por estação;
- como permissões e identidade são preservadas durante a indisponibilidade;
- como pedidos recebem identificadores sem colisão;
- como eventos locais são armazenados e ordenados;
- quando e como a sincronização deve começar;
- como o estado local é incorporado ao estado global;
- como falhas, repetições e interrupções de sincronização são tratadas;
- como o sistema impede perda silenciosa de dados;
- quando um pedido deixa de ser local e passa a ser global;
- por que o logout é bloqueado enquanto existirem pendências locais;
- como ocorre a recuperação administrativa excepcional.

Esta RFC não define a tecnologia concreta de replicação, o banco local definitivo, o protocolo de transporte, o formato físico dos pacotes de sincronização nem a interface visual final. Essas escolhas pertencem à implementação, mas deverão respeitar integralmente as decisões aqui estabelecidas.

---

## 3. Decisões fundamentais

A arquitetura de Operação Offline e Sincronização adota as seguintes decisões:

1. O modo offline será restrito e não reproduzirá integralmente a operação online.
2. O Cliente poderá consultar a última visão sincronizada do estado global.
3. Registros que já pertenciam ao estado global não poderão ser alterados offline.
4. O usuário poderá criar novos pedidos locais enquanto a Central estiver indisponível.
5. Cada pedido offline será visível e editável somente na estação que o criou.
6. Pedidos offline de outras estações não serão compartilhados antes da sincronização.
7. Dentro do escopo permitido, o usuário conservará as permissões previamente sincronizadas.
8. O pedido offline poderá ser concluído integralmente no Cliente, inclusive com cliente, itens, valores, pagamentos, descontos, fluxo, etapas, responsáveis e estado final.
9. Cada usuário autorizado a gerar pedidos possuirá um código de origem exclusivo e permanente.
10. O identificador visível do pedido combinará código de origem e sequência local.
11. Códigos de origem utilizados nunca serão reutilizados por outra pessoa.
12. A reconexão será detectada automaticamente.
13. A sincronização de retorno começará automaticamente e será visível ao usuário.
14. A sincronização preservará integralmente o estado produzido offline.
15. Um pedido sincronizado passará a integrar o estado global sem aprovação adicional apenas por sua origem offline.
16. Depois da sincronização, o pedido obedecerá às mesmas regras de acesso, bloqueio e edição dos demais pedidos globais.
17. Falhas de sincronização não poderão descartar, ocultar ou corromper os dados locais.
18. Reenvios do mesmo conteúdo não poderão criar duplicações.
19. A última identidade validada na estação poderá continuar ou retomar a sessão offline dentro dos limites definidos.
20. A troca para outro usuário exigirá disponibilidade da Central.
21. O logout normal será bloqueado enquanto houver pedidos ou eventos pendentes de sincronização.
22. Recuperações administrativas excepcionais serão sensíveis, explícitas e auditadas.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- detecção de indisponibilidade da Central;
- entrada e saída do modo offline;
- consulta de dados sincronizados;
- restrições de alteração sobre estado global;
- criação de pedidos locais;
- isolamento por estação;
- persistência local durável;
- sequência local de pedidos e eventos;
- identificação visível sem colisão;
- permissões sincronizadas;
- autenticação offline da última identidade validada;
- fila local de operações e eventos;
- reconexão automática;
- preparação, envio e incorporação dos dados;
- preservação do estado local;
- idempotência e repetição segura;
- falhas, retentativas e diagnóstico;
- transição de pedido local para pedido global;
- bloqueio de logout com pendências;
- recuperação administrativa excepcional;
- observabilidade do processo de sincronização.

### 4.2 Fora do escopo

Não são definidos aqui:

- banco de dados local definitivo;
- banco de dados central definitivo;
- ORM;
- protocolo definitivo de comunicação;
- criptografia concreta do transporte;
- algoritmo de hash de senha;
- mecanismo definitivo de descoberta da Central;
- interface visual detalhada do estado offline;
- política completa de backup da estação;
- sincronização entre várias Centrais;
- arquitetura em nuvem;
- operação multitenant;
- edição offline de registros globais;
- resolução colaborativa de conflitos sobre o mesmo registro global;
- funcionamento offline completo da IA;
- sincronização geral de arquivos externos.

A exclusão desses temas não autoriza implementações que contradigam as invariantes desta RFC.

---

## 5. Conceitos fundamentais

### 5.1 Central disponível

A Central está disponível quando o Cliente consegue estabelecer comunicação válida, autenticar a sessão quando necessário e utilizar os serviços centrais dentro dos limites normais de tempo e segurança.

Uma conexão de rede aparente não significa, por si só, que a Central esteja operacional.

### 5.2 Central indisponível

A Central está indisponível quando o Cliente não consegue utilizar com segurança os serviços necessários à operação global.

A indisponibilidade poderá resultar de:

- queda de energia da Máquina Principal;
- encerramento dos serviços centrais;
- falha da rede local;
- reinicialização;
- manutenção;
- falha de comunicação;
- erro de autenticação técnica;
- incompatibilidade temporária de versão;
- falha de persistência central.

### 5.3 Modo offline restrito

É o estado operacional em que o Cliente continua oferecendo somente as capacidades expressamente autorizadas sem a Central.

O modo offline não deverá ser apresentado como operação online normal.

### 5.4 Estado global

É a realidade oficial compartilhada e consolidada pela Central.

Pedidos, processos, clientes e demais registros já sincronizados pertencem ao estado global.

### 5.5 Estado local offline

É o conjunto de dados produzidos ou mantidos exclusivamente por uma estação durante a indisponibilidade da Central.

Na primeira versão, esse estado será usado principalmente para novos pedidos locais e seus eventos relacionados.

### 5.6 Visão sincronizada

É a última cópia local autorizada de informações globais recebidas da Central.

Ela poderá ser consultada offline, mas não deverá ser tratada como a versão mais recente da empresa.

### 5.7 Pedido local

É um pedido criado na estação enquanto a Central estava indisponível e que ainda não foi incorporado ao estado global.

### 5.8 Pendência de sincronização

É qualquer pedido, evento ou consequência local durável que ainda não tenha sido aceito e confirmado pela Central.

### 5.9 Incorporação

É o processo pelo qual a Central valida a integridade técnica do conteúdo recebido, reconhece sua identidade, persiste seus dados e eventos e o torna parte do estado global.

Incorporação não é uma nova aprovação comercial do conteúdo offline.

### 5.10 Origem comercial

É o usuário cujo código permanente participa do identificador visível do pedido e preserva a origem da venda.

Origem comercial não significa propriedade permanente do pedido após a sincronização.

---

## 6. Princípio de continuidade controlada

### 6.1 Continuidade sem simulação de normalidade

O Mheibos deverá permitir que a empresa continue registrando novas vendas durante a indisponibilidade da Central, sem fingir que toda a instalação permanece sincronizada.

### 6.2 Prioridade da primeira versão

A continuidade offline priorizará:

- consulta do último estado conhecido;
- criação de novos pedidos;
- preservação integral dos dados produzidos;
- retorno seguro ao estado global.

### 6.3 Limite deliberado

O Cliente não deverá tentar reproduzir toda a autoridade da Central.

A restrição reduz:

- conflitos entre estações;
- sobrescritas silenciosas;
- divergência de estados;
- complexidade de reconciliação;
- risco financeiro;
- necessidade de resolver edições concorrentes sem coordenação.

### 6.4 Segurança sobre conveniência

Quando uma operação depender da visão atual, de bloqueio global, de autorização atualizada ou de coordenação entre usuários, ela deverá permanecer indisponível offline.

---

## 7. Detecção de conectividade

### 7.1 Verificação funcional

O Cliente deverá determinar a disponibilidade da Central por uma verificação funcional e autenticada, não apenas por teste de presença da rede.

### 7.2 Estados de conectividade

A implementação deverá representar estados equivalentes a:

- online;
- conectividade degradada;
- Central indisponível;
- reconectando;
- sincronizando;
- sincronização com falhas;
- sincronizado.

### 7.3 Transições estáveis

Oscilações rápidas não deverão alternar repetidamente a interface entre online e offline.

A implementação deverá utilizar confirmação, retentativas ou mecanismo equivalente para reduzir falsos estados.

### 7.4 Informação ao usuário

O usuário deverá conseguir identificar claramente:

- que está offline;
- desde quando;
- quais capacidades permanecem disponíveis;
- quais operações estão bloqueadas;
- quantos dados aguardam sincronização;
- se a reconexão ou sincronização está em andamento.

### 7.5 Não interrupção indevida

A perda da Central não deverá fechar a aplicação nem apagar o trabalho já salvo localmente.

---

## 8. Entrada no modo offline

### 8.1 Sessão já aberta

Uma sessão autenticada deverá continuar funcionando offline dentro dos limites desta RFC quando a Central ficar indisponível.

### 8.2 Preservação do contexto

O Cliente deverá preservar, conforme autorizado:

- identidade da sessão;
- permissões sincronizadas;
- estação;
- rascunhos locais;
- pedidos locais existentes;
- fila de eventos;
- última visão sincronizada.

### 8.3 Alteração em andamento sobre registro global

Se a Central cair enquanto um usuário estiver editando um registro global, o Cliente não poderá confirmar essa alteração como mudança oficial offline.

O sistema deverá, quando possível:

- preservar o conteúdo como rascunho local não aplicado;
- informar que o registro global não pode ser salvo offline;
- permitir revisão posterior após a reconexão;
- evitar apresentar o rascunho como estado oficial.

### 8.4 Entrada explícita

O modo offline deverá ser um estado técnico visível, não uma escolha silenciosa do Cliente para contornar falhas da Central.

---

## 9. Capacidades permitidas offline

### 9.1 Consulta da última visão sincronizada

O usuário poderá consultar dados previamente sincronizados e autorizados para sua sessão.

A interface deverá indicar que os dados podem estar desatualizados.

### 9.2 Criação de novo pedido

O usuário autorizado poderá criar um novo Pedido local.

### 9.3 Conteúdo do pedido local

Dentro de suas permissões sincronizadas, o usuário poderá registrar:

- cliente existente disponível localmente;
- novo cliente necessário ao pedido;
- contatos;
- itens;
- descrições;
- quantidades;
- preços;
- descontos;
- pagamentos;
- formas de pagamento;
- prazos;
- fluxo operacional;
- etapas;
- responsáveis conhecidos;
- estados comerciais, operacionais, financeiros e de entrega permitidos;
- referências locais necessárias;
- observações;
- eventos e evidências relacionados.

### 9.4 Edição do próprio pedido local

Enquanto não estiver sincronizado, o pedido poderá ser editado somente na estação de origem e por uma identidade autorizada conforme as regras desta RFC.

### 9.5 Conclusão local

O pedido poderá alcançar localmente qualquer estado que o mesmo usuário pudesse registrar online dentro daquele fluxo, inclusive ser marcado como pronto, entregue, pago ou concluído, quando as regras sincronizadas permitirem.

### 9.6 Persistência antes da confirmação visual

O Cliente somente deverá apresentar a operação local como concluída depois que os dados e eventos essenciais tiverem sido gravados de forma durável na estação.

---

## 10. Operações proibidas offline

### 10.1 Alteração de registros globais

Não será permitido alterar offline:

- pedidos já sincronizados;
- processos globais existentes;
- etapas globais existentes;
- pagamentos globais existentes;
- clientes globais fora do contexto de um novo pedido local, quando a alteração afetar o cadastro oficial;
- perfis;
- permissões;
- usuários;
- políticas;
- configurações oficiais;
- metas;
- auditoria;
- bloqueios globais;
- missões globais;
- pendências globais.

### 10.2 Ações que exigem autoridade atual

Não serão permitidas operações que dependam de:

- permissão concedida após a última sincronização;
- revalidação global obrigatória;
- bloqueio de edição da Central;
- aprovação simultânea de outro usuário;
- leitura de estado atualizado de terceiros;
- coordenação entre várias estações;
- alteração de regra oficial.

### 10.3 Comunicação externa que dependa da Central

Integrações externas poderão ficar indisponíveis offline quando dependerem da Central.

A ausência da integração não poderá transformar uma mensagem não enviada em mensagem concluída.

### 10.4 IA central

Recursos cognitivos dependentes do modelo hospedado na Máquina Principal poderão ficar indisponíveis.

A indisponibilidade da IA não deverá impedir a criação determinística do pedido local.

---

## 11. Isolamento por estação

### 11.1 Exclusividade

Um pedido offline pertencerá tecnicamente à estação que o criou até a incorporação global.

### 11.2 Visibilidade

Durante a indisponibilidade da Central:

- a estação de origem poderá visualizar seus pedidos locais;
- outras estações não poderão visualizá-los;
- nenhuma estação deverá assumir sequências ou estados produzidos por outra origem.

### 11.3 Motivo do isolamento

O isolamento impede a criação de uma falsa visão compartilhada sem autoridade central.

### 11.4 Estação e autoria

A estação de origem e o usuário autor deverão ser registrados separadamente.

A estação identifica a origem técnica. O usuário identifica a autoria humana e comercial.

### 11.5 Transferência antes da sincronização

Não haverá transferência comum de pedido offline entre estações.

Qualquer recuperação em outra máquina dependerá de procedimento administrativo excepcional, conforme seção 25.

---

## 12. Identidade e autenticação offline

### 12.1 Continuidade da sessão

Uma sessão já autenticada poderá continuar offline.

### 12.2 Última identidade validada

A última identidade validada online naquela estação poderá autenticar-se novamente offline com credenciais locais protegidas.

### 12.3 Vinculação à estação

A autenticação offline deverá ser válida somente na estação em que a identidade foi previamente validada e autorizada.

### 12.4 Troca de usuário

A troca para outro usuário exigirá acesso à Central.

A estação não deverá manter um catálogo de múltiplas identidades capaz de substituir a autoridade central de autenticação.

### 12.5 Permissões utilizadas

A sessão offline deverá usar a última versão sincronizada das permissões efetivas do usuário.

### 12.6 Expiração e revogação desconhecida

O Cliente deverá reconhecer que permissões locais podem estar desatualizadas.

Por essa razão, elas somente poderão autorizar as operações offline expressamente permitidas nesta RFC.

### 12.7 Proteção das credenciais

Credenciais, verificadores e dados necessários à autenticação offline deverão ser armazenados de forma protegida e nunca em texto legível.

### 12.8 Auditoria

Login offline aceito ou recusado deverá produzir evento local de segurança para posterior sincronização.

---

## 13. Permissões no modo offline

### 13.1 Autoridade preservada

Dentro do conjunto de operações offline permitido, o usuário conservará a mesma autoridade previamente sincronizada.

### 13.2 Não ampliação de privilégios

O modo offline não poderá:

- conceder uma permissão inexistente;
- transformar indisponibilidade em exceção de segurança;
- permitir ações administrativas globais;
- ignorar limites de desconto, pagamento ou fluxo conhecidos localmente;
- contornar ações sensíveis aplicáveis ao pedido local.

### 13.3 Ações sensíveis locais

Quando uma ação sensível for permitida sobre um pedido local, ela continuará exigindo:

- reautenticação local protegida;
- justificativa, quando aplicável;
- evento de segurança;
- preservação dos valores anteriores e posteriores.

### 13.4 Políticas sincronizadas

O Cliente deverá registrar qual versão das políticas e permissões foi utilizada na criação e alteração do pedido offline.

### 13.5 Alteração posterior de políticas

Mudanças feitas na Central durante a indisponibilidade não invalidarão silenciosamente o estado local já autorizado.

A incorporação deverá preservar o que foi legitimamente realizado com a autoridade disponível naquele momento, salvo corrupção, fraude técnica ou violação de invariantes permanentes.

---

## 14. Identificação dos pedidos offline

### 14.1 Código de origem

Cada usuário autorizado a gerar pedidos possuirá um código de origem exclusivo e permanente.

Exemplos:

```text
J
MR
A7
```

O formato concreto poderá variar, desde que seja não ambíguo.

### 14.2 Sequência local

Cada código de origem possuirá uma sequência crescente usada para formar o identificador visível.

Exemplo:

```text
Código de origem: J
Sequência: 324
Pedido visível: #J324
```

### 14.3 Ausência de colisão

A combinação entre código permanente e sequência local deverá impedir que duas origens produzam o mesmo identificador visível.

### 14.4 Persistência da sequência

A sequência local deverá ser gravada de forma durável antes de o identificador ser apresentado como reservado.

### 14.5 Lacunas permitidas

Falhas, cancelamentos ou reservas interrompidas poderão gerar lacunas na sequência.

A continuidade perfeita da numeração é menos importante que impedir duplicidade e reutilização.

### 14.6 Código não reutilizável

Um código que já tenha originado pedido nunca poderá ser atribuído a outra pessoa, mesmo se o usuário:

- sair da empresa;
- for desativado;
- mudar de perfil;
- perder permissão de vendas;
- tiver sua conta arquivada.

### 14.7 Identificador técnico

O identificador visível não substitui o identificador técnico estável definido na RFC-0005.

### 14.8 Preservação após sincronização

O identificador visível não deverá ser renumerado apenas porque o pedido foi incorporado à Central.

---

## 15. Persistência local

### 15.1 Durabilidade

Pedidos e eventos offline deverão ser persistidos localmente de forma durável.

### 15.2 Conteúdo mínimo

O armazenamento local deverá preservar, conforme aplicável:

- pedido;
- cliente local;
- itens;
- valores;
- pagamentos;
- descontos;
- fluxo instanciado;
- processos;
- etapas;
- datas;
- responsáveis;
- estados;
- referências;
- eventos;
- evidências;
- identidade do usuário;
- estação;
- sessão;
- versão de permissões e políticas;
- estado de sincronização;
- tentativas e falhas.

### 15.3 Integridade

A implementação deverá detectar corrupção, gravação incompleta e inconsistências locais antes de sincronizar.

### 15.4 Atomicidade conceitual

Alterações compostas deverão ser gravadas como unidade lógica ou possuir mecanismo de recuperação que impeça pedidos parcialmente incoerentes.

### 15.5 Segredos

Senhas, tokens e segredos não deverão ser gravados em texto legível.

### 15.6 Separação de cache e dados pendentes

Cache descartável e dados offline não sincronizados deverão possuir tratamento diferente.

Dados pendentes nunca poderão ser eliminados por uma simples limpeza de cache.

### 15.7 Recuperação após falha

Ao reiniciar o Cliente, o sistema deverá identificar pedidos e eventos pendentes e restaurar seu estado de sincronização.

---

## 16. Eventos offline

### 16.1 Registro obrigatório

Toda alteração relevante de um pedido local deverá produzir evento conforme a RFC-0006.

### 16.2 Origem

O evento deverá registrar:

- usuário;
- estação;
- sessão;
- origem offline;
- momento local;
- sequência local;
- entidade afetada;
- mudança realizada;
- política aplicada.

### 16.3 Ordem local

A estação deverá preservar uma ordem local estável dos eventos produzidos.

### 16.4 Correlação

Eventos de uma mesma operação composta deverão compartilhar correlação suficiente para incorporação coerente.

### 16.5 Repetição segura

O reenvio de um evento não poderá aplicar a mesma alteração duas vezes.

### 16.6 Imutabilidade

Eventos locais já registrados não deverão ser reescritos para ocultar o que ocorreu.

Correções deverão produzir novos eventos.

### 16.7 Incorporação

A Central deverá preservar a identidade e a origem offline dos eventos incorporados.

---

## 17. Fila local de sincronização

### 17.1 Finalidade

A fila local representa tudo o que ainda precisa ser reconhecido pela Central.

### 17.2 Estados conceituais

Cada item deverá possuir estado equivalente a:

- aguardando envio;
- preparando;
- enviando;
- recebido pela Central;
- incorporado;
- falha temporária;
- falha que exige atenção;
- recuperação administrativa.

### 17.3 Não descarte

Nenhum item poderá desaparecer da fila sem confirmação de incorporação ou procedimento administrativo auditado.

### 17.4 Tentativas

A fila deverá registrar:

- número de tentativas;
- último momento;
- resultado;
- motivo conhecido;
- próxima tentativa prevista.

### 17.5 Prioridade

A implementação poderá priorizar unidades completas de pedido e seus eventos causais, evitando enviar consequências dependentes antes da entidade principal.

### 17.6 Continuidade

Fechar ou reiniciar a aplicação não deverá apagar a fila.

---

## 18. Reconexão

### 18.1 Detecção automática

O Cliente deverá detectar o retorno funcional da Central sem depender de ação manual do usuário.

### 18.2 Aviso

A interface deverá informar que a Central foi restabelecida.

### 18.3 Início automático

A sincronização começará automaticamente.

O usuário não deverá precisar aprovar o simples envio de dados já produzidos legitimamente offline.

### 18.4 Continuidade de uso

Sempre que tecnicamente seguro, o usuário poderá continuar utilizando a aplicação enquanto a sincronização ocorre.

### 18.5 Ordem de retorno

O Cliente deverá, conceitualmente:

1. validar a conexão;
2. revalidar a sessão quando necessário;
3. consultar compatibilidade e estado da Central;
4. identificar pendências locais;
5. preparar unidades coerentes;
6. enviar dados e eventos;
7. receber confirmações;
8. atualizar o estado local;
9. informar o resultado.

### 18.6 Reconexão não é incorporação

Estar novamente conectado não significa que todos os dados locais já foram sincronizados.

A interface deverá distinguir esses estados.

---

## 19. Protocolo conceitual de sincronização

### 19.1 Unidade coerente

A sincronização deverá enviar uma representação completa e coerente do pedido local e seus eventos relacionados.

### 19.2 Identificação da origem

Cada pacote ou operação deverá indicar:

- instalação;
- estação;
- usuário;
- sessão;
- pedido;
- identificadores técnicos;
- identificador visível;
- sequência local;
- eventos;
- versão de esquema;
- versão de políticas utilizada.

### 19.3 Validação técnica

A Central poderá validar:

- integridade do pacote;
- identidade da instalação;
- identidade da estação;
- unicidade dos identificadores;
- ausência de duplicação;
- consistência estrutural;
- versão compatível;
- autenticidade da origem;
- presença de campos obrigatórios.

### 19.4 Ausência de reaprovação comercial

A Central não deverá exigir aprovação adicional apenas porque o pedido foi criado offline.

### 19.5 Preservação do estado

A incorporação deverá preservar exatamente o conteúdo autorizado produzido na estação.

### 19.6 Confirmação

O Cliente somente poderá marcar uma pendência como sincronizada após receber confirmação durável da Central.

### 19.7 Confirmação parcial

Uma unidade que exige consistência não deverá ser marcada como integralmente sincronizada se apenas parte dela tiver sido aceita.

A implementação deverá usar transação lógica, compensação ou estado explícito de incorporação parcial.

---

## 20. Preservação integral do estado local

### 20.1 Regra

A sincronização deverá incorporar o pedido como ele foi deixado pelo usuário.

### 20.2 Conteúdo preservado

Deverão ser preservados, conforme aplicável:

- cliente;
- contatos;
- itens;
- quantidades;
- valores;
- descontos;
- pagamentos;
- prazos;
- fluxo instanciado;
- processos;
- etapas;
- responsáveis;
- estados finais;
- referências;
- eventos;
- evidências;
- autoria;
- origem offline;
- versões de regras utilizadas.

### 20.3 Não normalização destrutiva

A Central não poderá substituir silenciosamente o fluxo, recalcular decisões autorizadas para outro resultado ou apagar etapas apenas porque o modelo global mudou durante a indisponibilidade.

### 20.4 Regras permanentes

A preservação integral não autoriza incorporar conteúdo tecnicamente corrompido, duplicado, forjado ou incompatível com invariantes permanentes.

### 20.5 Divergência com cadastros globais

Quando um dado local possuir equivalente global atualizado, a Central deverá preservar a realidade histórica do pedido e relacioná-la corretamente, sem sobrescrever silenciosamente o conteúdo contratado.

### 20.6 Novo cliente local

Um cliente criado junto ao pedido offline poderá ser incorporado como nova entidade ou relacionado a uma entidade global comprovadamente equivalente, desde que:

- o pedido preserve os dados efetivamente utilizados;
- nenhuma associação ambígua seja feita silenciosamente;
- a operação seja auditável.

---

## 21. Idempotência e duplicação

### 21.1 Reenvio esperado

Falhas de rede poderão obrigar o Cliente a reenviar dados cuja confirmação não foi recebida.

### 21.2 Identidade estável

Pedidos, eventos e operações deverão possuir identidades estáveis para que a Central reconheça repetições.

### 21.3 Efeito único

Processar novamente o mesmo conteúdo não poderá:

- criar outro pedido;
- duplicar pagamentos;
- duplicar itens;
- concluir etapas novamente;
- gerar números diferentes;
- criar eventos equivalentes indevidos.

### 21.4 Confirmação recuperável

Se a Central já tiver incorporado o pedido, mas o Cliente não tiver recebido a confirmação, uma nova tentativa deverá retornar o estado já reconhecido.

### 21.5 Duplicidade aparente de cliente

A prevenção de duplicidade de clientes não deverá impedir a incorporação do pedido nem provocar perda de dados.

A consolidação poderá ocorrer por procedimento explícito posterior quando a equivalência não for segura.

---

## 22. Falhas de sincronização

### 22.1 Preservação obrigatória

Toda falha deverá manter os dados locais intactos.

### 22.2 Visibilidade

O usuário deverá ser informado quando houver falha que impeça a incorporação.

### 22.3 Diagnóstico

O sistema deverá apresentar motivo compreensível, como:

- Central indisponível novamente;
- sessão inválida;
- versão incompatível;
- pacote corrompido;
- identificador duplicado inesperado;
- dados obrigatórios ausentes;
- erro de persistência central;
- falha de autorização técnica;
- recuperação administrativa necessária.

### 22.4 Nova tentativa automática

Falhas temporárias deverão gerar novas tentativas automáticas conforme política.

### 22.5 Tentativa manual

O usuário deverá possuir ação para tentar novamente quando isso for seguro.

### 22.6 Falha persistente

Uma falha persistente deverá permanecer destacada e não poderá ser silenciada como se a sincronização tivesse terminado.

### 22.7 Proibição de recriação manual como solução padrão

O sistema não deverá orientar o usuário a digitar novamente o pedido na Central como solução comum, pois isso aumenta risco de duplicação e perda de autoria.

### 22.8 Suporte administrativo

Falhas que não possam ser resolvidas automaticamente deverão oferecer informações suficientes para recuperação por usuário autorizado.

---

## 23. Transição para o estado global

### 23.1 Momento da transição

O pedido deixa de ser local quando a Central confirma sua incorporação durável.

### 23.2 Efeitos

Após a sincronização:

- o pedido integra o estado global;
- usuários autorizados poderão visualizá-lo;
- usuários autorizados poderão editá-lo;
- bloqueios de edição normais passam a ser aplicáveis;
- regras centrais vigentes passam a orientar alterações futuras;
- eventos offline permanecem identificados como tais;
- a origem comercial permanece preservada.

### 23.3 Origem não é propriedade

O prefixo do pedido indica sua origem comercial, não exclusividade permanente do criador.

### 23.4 Limpeza local

Após confirmação segura, o Cliente poderá retirar o conteúdo da fila de pendências.

A implementação poderá manter cache ou histórico local, mas nunca deverá apagar a única cópia antes da confirmação central.

### 23.5 Notificação do resultado

O usuário deverá receber resultado claro, incluindo:

- quantidade sincronizada;
- pedidos incorporados;
- pendências restantes;
- falhas encontradas;
- ações disponíveis.

---

## 24. Logout e encerramento da aplicação

### 24.1 Logout bloqueado

O usuário não poderá encerrar normalmente a sessão enquanto existirem pedidos ou eventos locais ainda não sincronizados.

### 24.2 Finalidade

A regra preserva:

- autoria;
- vínculo com credenciais locais;
- responsabilidade sobre pendências;
- continuidade da fila;
- segurança da estação;
- recuperação compreensível.

### 24.3 Fechamento da janela

Quando houver pendências, fechar a janela não deverá apagar a sessão ou os dados.

A aplicação poderá:

- permanecer ativa em segundo plano;
- impedir encerramento completo;
- solicitar que o usuário aguarde a sincronização;
- permitir encerramento técnico preservando a sessão bloqueada para retomada, conforme implementação segura.

### 24.4 Desligamento do computador

O sistema não pode impedir queda de energia ou desligamento forçado.

Por isso, dados e fila deverão ser duráveis e recuperáveis na próxima inicialização.

### 24.5 Troca de usuário

Enquanto houver dados pendentes vinculados à identidade atual, a troca normal de usuário deverá permanecer bloqueada.

### 24.6 Sessão após reinício

Ao reabrir o Cliente, o sistema deverá restaurar a pendência vinculada à identidade e impedir que outra pessoa assuma silenciosamente sua autoria.

---

## 25. Recuperação administrativa excepcional

### 25.1 Finalidade

Um procedimento excepcional poderá ser necessário quando:

- o usuário não puder retornar;
- a conta tiver sido desativada;
- a estação precisar de manutenção;
- a credencial local estiver indisponível;
- houver corrupção parcial recuperável;
- a sincronização normal estiver tecnicamente bloqueada.

### 25.2 Não normalidade

A recuperação administrativa não será um atalho comum para contornar o bloqueio de logout ou trocar de usuário.

### 25.3 Proteções

O procedimento deverá exigir:

- administrador autorizado;
- reautenticação;
- justificativa;
- identificação da estação;
- identificação do usuário original;
- inventário dos dados pendentes;
- preservação de cópia de segurança;
- auditoria imutável;
- resultado explícito.

### 25.4 Autoria preservada

Recuperar ou sincronizar administrativamente um pedido não transfere sua autoria comercial ao administrador.

### 25.5 Transferência técnica

Quando for necessário mover os dados para outra estação ou ferramenta de recuperação, a origem técnica original deverá permanecer registrada.

### 25.6 Descarte excepcional

Descartar dados pendentes somente poderá ocorrer quando:

- houver confirmação de que são irrecuperáveis, inválidos ou duplicados;
- o impacto for explicado;
- existir autorização adequada;
- uma cópia ou evidência for preservada quando possível;
- o procedimento for auditado.

---

## 26. Concorrência e conflitos

### 26.1 Estratégia principal

A primeira versão evita conflitos de edição global proibindo alterações offline sobre registros já sincronizados.

### 26.2 Conflitos possíveis

Ainda poderão ocorrer conflitos como:

- cliente local semelhante a cliente global;
- código de origem configurado incorretamente;
- repetição de pacote;
- versão de esquema incompatível;
- mudança de permissão durante a indisponibilidade;
- política atual diferente da utilizada offline.

### 26.3 Tratamento

Conflitos não deverão ser resolvidos por escolha silenciosa de “última gravação vence”.

### 26.4 Estado legítimo offline

Mudanças globais ocorridas durante a indisponibilidade não deverão apagar o pedido local legitimamente produzido.

### 26.5 Conflito de identidade

Se a Central detectar colisão impossível de identificador técnico ou código de origem, a sincronização deverá parar de forma segura e exigir diagnóstico.

### 26.6 Sem mesclagem arbitrária

A IA não deverá decidir sozinha como mesclar registros conflitantes.

Ela poderá explicar o problema e preparar alternativas, mas a resolução persistente seguirá regras determinísticas e autorização humana.

---

## 27. Interação com eventos e auditoria

### 27.1 Origem offline

Todo evento incorporado deverá continuar identificado como originado offline.

### 27.2 Tempos distintos

A auditoria deverá preservar:

- momento local do fato;
- momento de registro na estação;
- momento de recebimento pela Central;
- momento de incorporação.

### 27.3 Sequência

A Central deverá preservar a ordem local original e estabelecer uma ordem de incorporação sem falsificar a cronologia.

### 27.4 Eventos da sincronização

Deverão existir eventos equivalentes a:

- modo offline iniciado;
- pedido local criado;
- login offline realizado;
- reconexão detectada;
- sincronização iniciada;
- pacote recebido;
- pedido incorporado;
- sincronização concluída;
- sincronização falhou;
- recuperação administrativa executada.

### 27.5 Imutabilidade

A incorporação não deverá reescrever eventos locais como se tivessem sido produzidos online.

---

## 28. Segurança

### 28.1 Dados locais protegidos

Pedidos, pagamentos, clientes, credenciais e eventos locais deverão ser protegidos contra acesso não autorizado.

### 28.2 Menor privilégio

Somente o Cliente e os componentes autorizados deverão acessar o armazenamento offline.

### 28.3 Identidade da estação

A Central deverá reconhecer a estação que envia o conteúdo e rejeitar origens não autorizadas.

### 28.4 Integridade

A implementação deverá utilizar mecanismos adequados para detectar alteração indevida dos pacotes e dados locais.

### 28.5 Segredos

Senhas, tokens e chaves não deverão constar em eventos, mensagens de erro ou pacotes de domínio em texto legível.

### 28.6 Dados de usuário desativado

A desativação de um usuário não autoriza apagar pedidos pendentes por ele criados.

A recuperação deverá preservar autoria e aplicar procedimento administrativo.

### 28.7 Ataques de repetição

A Central deverá impedir que pacotes capturados ou reenviados produzam duplicações ou alterações indevidas.

---

## 29. Experiência do usuário

### 29.1 Estado visível

O Cliente deverá exibir de forma persistente e compreensível quando estiver offline.

### 29.2 Linguagem

Mensagens deverão explicar consequências práticas, por exemplo:

> “A Central está indisponível. Você pode consultar dados já sincronizados e criar novos pedidos nesta estação. Pedidos existentes não podem ser alterados até a reconexão.”

### 29.3 Identificação de dados locais

Pedidos locais deverão possuir marcação visual clara enquanto não estiverem sincronizados.

### 29.4 Contagem de pendências

O usuário deverá conseguir visualizar quantos pedidos ou eventos aguardam incorporação.

### 29.5 Progresso

Durante a sincronização, a interface deverá mostrar progresso suficiente para indicar atividade real sem exigir detalhes técnicos excessivos.

### 29.6 Resultado acionável

Em caso de falha, a interface deverá oferecer ações como:

- tentar novamente;
- abrir detalhes;
- copiar diagnóstico;
- solicitar suporte administrativo.

### 29.7 Sem falsa conclusão

Um pedido local não deverá aparecer como globalmente disponível antes da confirmação da Central.

---

## 30. Fluxos arquiteturais principais

### 30.1 Queda da Central durante sessão ativa

```text
Cliente detecta indisponibilidade
        ↓
Preserva sessão e dados locais
        ↓
Exibe estado offline
        ↓
Bloqueia alterações do estado global
        ↓
Mantém consulta da visão sincronizada
        ↓
Permite novos pedidos locais
```

### 30.2 Criação de pedido offline

```text
Usuário inicia novo pedido
        ↓
Cliente valida permissões sincronizadas
        ↓
Reserva identificador técnico e sequência local
        ↓
Usuário informa dados do pedido
        ↓
Cliente aplica regras locais conhecidas
        ↓
Pedido e eventos são gravados duravelmente
        ↓
Interface confirma criação local
        ↓
Pedido entra na fila de sincronização
```

### 30.3 Reconexão e incorporação

```text
Cliente detecta retorno da Central
        ↓
Informa o usuário
        ↓
Revalida conexão e sessão
        ↓
Identifica pendências locais
        ↓
Envia unidade coerente com chave idempotente
        ↓
Central valida integridade e identidade
        ↓
Central incorpora pedido e eventos
        ↓
Central confirma durabilidade
        ↓
Cliente marca pedido como global
        ↓
Interface informa resultado
```

### 30.4 Falha de sincronização

```text
Envio ou incorporação falha
        ↓
Dados permanecem locais
        ↓
Fila registra tentativa e motivo
        ↓
Interface mantém pendência visível
        ↓
Sistema agenda nova tentativa
        ↓
Usuário pode tentar novamente
        ↓
Se persistir, recuperação administrativa
```

### 30.5 Tentativa de logout com pendências

```text
Usuário solicita logout
        ↓
Cliente verifica fila local
        ↓
Existem pedidos ou eventos pendentes?
        ├── Não → encerra sessão normalmente
        └── Sim → bloqueia logout
                  ↓
             explica o motivo
                  ↓
             tenta sincronizar quando possível
                  ↓
             oferece suporte administrativo excepcional
```

---

## 31. Observabilidade e diagnóstico

### 31.1 Indicadores mínimos

O sistema deverá permitir acompanhar:

- estado da Central por estação;
- duração do período offline;
- quantidade de pedidos locais;
- quantidade de eventos pendentes;
- tamanho da fila;
- idade da pendência mais antiga;
- tentativas realizadas;
- falhas por motivo;
- tempo de sincronização;
- pedidos incorporados;
- recuperações administrativas.

### 31.2 Logs técnicos

Logs deverão registrar detalhes suficientes para diagnóstico sem substituir os eventos de auditoria.

### 31.3 Diagnóstico exportável

Usuários autorizados deverão poder gerar um pacote de diagnóstico que não exponha senhas ou segredos.

### 31.4 Alertas

Falhas que ameacem perda de dados, corrupção ou bloqueio prolongado deverão produzir alertas técnicos e administrativos apropriados.

### 31.5 Saúde do armazenamento local

O Cliente deverá detectar falta de espaço, falha de gravação e corrupção antes que operações sejam apresentadas como concluídas.

---

## 32. Requisitos de qualidade

### 32.1 Durabilidade

Nenhum pedido offline confirmado ao usuário poderá depender apenas de memória volátil.

### 32.2 Não perda

Falhas de rede, reinicialização, repetição ou queda da Central não poderão apagar dados pendentes.

### 32.3 Não duplicação

Reenvios não poderão criar efeitos duplicados.

### 32.4 Clareza

O usuário deverá compreender quando está offline, o que pode fazer e o que ainda não foi sincronizado.

### 32.5 Segurança

Credenciais, permissões e dados locais deverão permanecer protegidos.

### 32.6 Consistência

Pedidos locais deverão manter coerência interna e ser incorporados como unidades completas.

### 32.7 Responsividade

A gravação local deverá ser suficientemente rápida para não comprometer o atendimento, sem sacrificar durabilidade.

### 32.8 Recuperabilidade

O sistema deverá retomar pendências após falhas e oferecer procedimento administrativo para casos excepcionais.

### 32.9 Auditabilidade

Toda operação relevante deverá preservar autoria, estação, momento, origem offline e resultado da sincronização.

### 32.10 Compatibilidade evolutiva

O protocolo e os dados deverão possuir versionamento suficiente para evolução controlada entre versões do Cliente e da Central.

---

## 33. Falhas previstas

### 33.1 Queda de energia durante gravação local

A implementação deverá detectar operações incompletas e restaurar o último estado consistente.

### 33.2 Queda durante envio

O conteúdo deverá permanecer pendente até confirmação central.

### 33.3 Central recebe, mas confirmação não retorna

Nova tentativa deverá reconhecer a operação já incorporada.

### 33.4 Cliente reinicia com pendências

A fila deverá ser restaurada automaticamente.

### 33.5 Usuário é desativado antes da sincronização

Os dados deverão permanecer recuperáveis e vinculados à autoria original. A incorporação deverá seguir procedimento administrativo seguro quando a autenticação normal não for mais possível.

### 33.6 Estação é danificada

A recuperação dependerá de cópia local disponível, backup ou procedimento técnico. A arquitetura não poderá prometer recuperar dados que nunca foram persistidos em meio durável.

### 33.7 Incompatibilidade de versão

A sincronização deverá parar de forma segura, preservar os dados e indicar atualização ou migração necessária.

### 33.8 Armazenamento sem espaço

O Cliente deverá impedir a confirmação de novas operações que não possam ser persistidas duravelmente.

### 33.9 Corrupção local

O sistema deverá isolar o conteúdo afetado, preservar evidências e impedir incorporação automática até diagnóstico.

### 33.10 Oscilação de rede

A sincronização deverá tolerar interrupções e retomar sem duplicar efeitos.

---

## 34. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | Continuidade do Mheibos como memória operacional ativa |
| RFC-0001 | Segurança, rastreabilidade, fonte da verdade e proteção da atenção humana |
| RFC-0002 | Processos, fluxos, estados e autoridade operacional aplicada aos pedidos locais |
| RFC-0003 | Central, Clientes, armazenamento local e topologia da implantação |
| RFC-0004 | Disponibilidade e limites da camada cognitiva durante falhas da Central |
| RFC-0005 | Identidade técnica, Pedido, Processo, Estação, Sessão e separação entre estado local e global |
| RFC-0006 | Eventos offline, ordenação, idempotência, incorporação e auditoria |
| RFC-0007 | Identidade, permissões sincronizadas, autenticação offline e recuperação administrativa |
| RFC-0009 | Apresentação visual do modo offline, alertas e intervenções |
| RFC-0012 | Notificação de pendências prolongadas e escalonamento de falhas |
| RFC-0013 | Regras comerciais, financeiras, pagamentos e descontos dos pedidos offline |
| RFC-0014 | Referências de arquivos e comportamento de integrações durante indisponibilidade |

Esta RFC define o comportamento de continuidade e sincronização. Os RFCs relacionados definem o significado dos dados, a autorização, os eventos e a experiência visual utilizados por esse comportamento.

---

## 35. Consequências da decisão

### 35.1 Benefícios

- continuidade de novas vendas durante quedas da Máquina Principal;
- menor dependência de disponibilidade contínua da infraestrutura local;
- prevenção de perda de pedidos produzidos offline;
- ausência de colisão na identificação visível;
- simplicidade maior que uma replicação completa;
- redução de conflitos entre estações;
- preservação da autoridade previamente concedida;
- sincronização automática e rastreável;
- evolução futura possível sem transformar cache em fonte da verdade.

### 35.2 Custos e limitações

- pedidos globais existentes não podem ser alterados offline;
- dados exibidos offline podem estar desatualizados;
- pedidos locais ficam invisíveis às outras estações;
- troca de usuário fica limitada;
- logout pode permanecer bloqueado;
- cada Cliente precisa de armazenamento local confiável;
- sincronização exige idempotência, versionamento e recuperação;
- falhas persistentes demandam ferramentas administrativas.

### 35.3 Riscos

- apresentar cache como dado atual;
- permitir edição global offline por conveniência;
- perder dados ao limpar cache;
- duplicar pedidos por reenvio;
- renumerar pedidos após sincronização;
- reutilizar códigos de origem;
- aceitar pacotes corrompidos;
- ocultar falhas de sincronização;
- permitir logout e troca de usuário com pendências;
- atribuir pedidos recuperados ao administrador;
- misturar confirmação de conexão com confirmação de incorporação;
- transformar recuperação excepcional em fluxo comum.

---

## 36. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. o estado offline for explicitamente indicado ao usuário;
2. dados globais existentes permanecerem somente para consulta offline;
3. alterações de pedidos e processos globais forem bloqueadas sem a Central;
4. novos pedidos puderem ser criados e persistidos localmente;
5. pedidos offline permanecerem exclusivos da estação de origem;
6. outras estações não visualizarem pedidos locais antes da sincronização;
7. o usuário puder registrar integralmente o pedido local dentro de suas permissões sincronizadas;
8. cada pedido possuir identificador técnico estável;
9. o identificador visível combinar código de origem e sequência local;
10. códigos de origem utilizados nunca forem reutilizados;
11. o estado local for gravado duravelmente antes da confirmação visual;
12. eventos offline preservarem usuário, estação, sessão, sequência e origem;
13. a reconexão for detectada automaticamente;
14. a sincronização começar automaticamente e permanecer visível;
15. reenvios forem idempotentes;
16. a Central preservar integralmente o estado autorizado produzido offline;
17. pedidos incorporados não exigirem aprovação adicional apenas por sua origem offline;
18. pedidos sincronizados passarem a obedecer às regras globais normais;
19. falhas não descartarem dados locais;
20. falhas permanecerem visíveis com motivo e possibilidade de nova tentativa;
21. a última identidade validada puder continuar ou autenticar-se offline na estação autorizada;
22. a troca de usuário exigir a Central;
23. o logout normal ser bloqueado com pendências;
24. recuperações administrativas exigirem reautenticação, justificativa e auditoria;
25. a autoria original permanecer preservada em toda recuperação e incorporação.

---

## 37. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em revisões posteriores:

- banco local definitivo;
- formato físico da fila;
- protocolo de transporte;
- serialização dos pacotes;
- tamanho máximo de lote;
- política exata de retentativas;
- tempo de detecção de queda e reconexão;
- criptografia concreta do armazenamento local;
- mecanismo de assinatura ou verificação de integridade;
- estratégia de backup das estações;
- interface administrativa de recuperação;
- política de expiração da autenticação offline;
- sincronização de arquivos externos;
- uso offline de recursos cognitivos;
- tratamento de múltiplas identidades offline na fase futura;
- edição offline de registros globais em versões posteriores;
- sincronização em arquitetura de nuvem.

Essas decisões não poderão reduzir as garantias de durabilidade, autoria, não duplicação, isolamento e visibilidade estabelecidas nesta RFC.

---

## 38. Declaração normativa

Quando a Central estiver indisponível, o Cliente Mheibos deverá entrar em modo offline restrito e visível.

Nesse modo, o usuário poderá consultar a última visão sincronizada e criar novos pedidos locais, mas não poderá alterar pedidos, processos ou outros registros já pertencentes ao estado global.

Cada pedido offline permanecerá exclusivo da estação de origem até sua incorporação pela Central. Dentro do escopo permitido, o usuário manterá as permissões previamente sincronizadas e poderá registrar integralmente a realidade comercial e operacional do novo pedido.

Os identificadores visíveis serão formados por código permanente de origem e sequência local. Códigos já utilizados nunca serão reutilizados.

Quando a Central retornar, o Cliente iniciará automaticamente uma sincronização visível. A Central preservará o estado autorizado produzido offline, impedirá duplicações e transformará o pedido em registro global após confirmação durável.

Falhas de sincronização nunca poderão apagar ou ocultar dados pendentes. O logout e a troca normal de usuário permanecerão bloqueados enquanto existirem pedidos ou eventos locais não sincronizados, salvo recuperação administrativa excepcional, protegida e auditada.

---

## 39. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-041 — modo offline restrito | 6, 9 e 10 |
| INV-042 — pedidos exclusivos da estação | 11 |
| INV-043 — autoridade preservada offline | 9, 12 e 13 |
| INV-044 — identificador por origem e sequência | 14 |
| INV-045 — códigos não reutilizados | 14.6 |
| INV-046 — sincronização automática e visível | 18, 29 e 30.3 |
| INV-047 — falhas permanecem locais e visíveis | 17 e 22 |
| INV-048 — preservação integral do estado local | 19 e 20 |
| INV-049 — pedido torna-se global após sincronizar | 23 |
| INV-050 — login offline da última identidade validada | 12 |
| INV-051 — logout bloqueado com pendências | 24 e 25 |
