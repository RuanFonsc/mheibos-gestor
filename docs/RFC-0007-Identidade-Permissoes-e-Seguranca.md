# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0007 — Identidade, Permissões e Segurança

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-030 a INV-040

---

## 1. Resumo

Esta RFC define como o Mheibos identifica usuários, autentica acessos, atribui perfis, calcula permissões, limita ações, protege operações sensíveis e coordena edições concorrentes.

Cada pessoa utilizará credenciais próprias do Mheibos, independentes da conta do Windows. A identidade autenticada será validada pela Central e determinará o perfil, as permissões efetivas, os escopos de acesso, as responsabilidades disponíveis e a experiência apresentada pela interface.

Cada usuário possuirá exatamente um perfil principal. Perfis fornecerão permissões padrão, enquanto necessidades particulares serão atendidas por exceções individuais explícitas, restritivas ou concessivas, sempre auditadas.

A autorização não será implementada apenas por ocultação de telas ou botões. Toda operação relevante deverá ser validada na camada central e nos casos de uso responsáveis pela persistência. A interface poderá antecipar essas limitações, mas nunca será a única barreira de segurança.

Ações classificadas como sensíveis exigirão reautenticação com a senha do usuário que as executa. Usuários comuns autorizados deverão informar justificativa textual obrigatória. Administradores autorizados poderão executar sem justificativa obrigatória, mas nunca sem reautenticação e auditoria.

Registros sensíveis utilizarão bloqueio temporário de edição. Enquanto um usuário estiver editando, os demais poderão consultar o registro, mas não alterá-lo. Todo bloqueio deverá possuir mecanismos de liberação automática e administrativa para impedir abandono indefinido.

A IA herdará integralmente os limites do usuário autenticado. Ela não possuirá privilégios próprios, não poderá contornar permissões e não poderá revelar, preparar ou executar ações fora do escopo autorizado daquela sessão.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- como o Mheibos identifica uma pessoa;
- como funciona a autenticação própria do sistema;
- como perfis e exceções individuais formam as permissões efetivas;
- por que cada usuário possui apenas um perfil principal;
- como permissões consideram ação, dado, propriedade, contexto e alcance;
- onde a autorização deve ser aplicada;
- como usuários comuns, gerentes e administradores acessam dados e indicadores;
- o que caracteriza uma ação sensível;
- quando a senha deve ser solicitada novamente;
- quando uma justificativa é obrigatória;
- como a política de ações sensíveis pode ser configurada;
- como o sistema evita alterações simultâneas incompatíveis;
- como bloqueios de edição são adquiridos, renovados e liberados;
- como a IA permanece subordinada à identidade e às permissões humanas;
- quais registros de segurança devem ser auditados.

Esta RFC não define o protocolo criptográfico definitivo, o algoritmo de hash de senha, o banco de dados, a interface visual de administração, a política completa de operação offline ou a tecnologia concreta de controle de sessão. Essas escolhas pertencem à implementação ou a RFCs relacionados, mas deverão respeitar as regras aqui estabelecidas.

---

## 3. Decisões fundamentais

A arquitetura de identidade, permissões e segurança adota as seguintes decisões:

1. A autenticação será própria do Mheibos e independente da conta do Windows.
2. Cada usuário possuirá credenciais individuais.
3. A Central será a autoridade da identidade, dos perfis, das permissões e das políticas oficiais.
4. Cada usuário possuirá exatamente um perfil principal.
5. Perfis fornecerão permissões padrão.
6. Exceções individuais poderão conceder ou restringir capacidades específicas.
7. Toda exceção individual será explícita, justificável e auditada.
8. Permissões serão avaliadas por ação, recurso, propriedade, contexto e alcance.
9. Ocultar elementos da interface não será considerado controle de acesso suficiente.
10. A autorização será aplicada nos casos de uso e na camada central antes da persistência.
11. Usuários comuns acessarão seus próprios indicadores por padrão.
12. Visão global dependerá de permissão própria, normalmente associada à gestão ou administração.
13. Toda ação sensível exigirá reautenticação com a senha do executor.
14. Usuários comuns autorizados deverão justificar ações sensíveis.
15. Administradores autorizados poderão dispensar justificativa textual, mas nunca reautenticação ou auditoria.
16. A política de ações sensíveis será configurável por administradores autorizados.
17. Edição concorrente de registros sensíveis utilizará bloqueio temporário exclusivo para escrita.
18. Leitura permanecerá disponível aos demais usuários enquanto houver bloqueio.
19. Todo bloqueio terá expiração e mecanismos seguros de liberação.
20. A IA herdará exatamente os limites do usuário autenticado.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- identidade do usuário;
- credenciais próprias do Mheibos;
- autenticação online;
- sessões autenticadas;
- perfil principal;
- permissões padrão;
- exceções individuais;
- cálculo de permissões efetivas;
- escopos de acesso;
- propriedade e autoria como fatores de autorização;
- acesso a indicadores próprios e globais;
- negação central de operações;
- reautenticação;
- ações sensíveis;
- justificativas obrigatórias;
- configuração da política de sensibilidade;
- bloqueio temporário de edição;
- expiração e liberação de bloqueios;
- herança de permissões pela IA;
- auditoria das decisões de segurança.

### 4.2 Fora do escopo

Não são definidos aqui:

- algoritmo definitivo de hash de senha;
- autenticação multifator;
- recuperação definitiva de senha;
- integração com diretórios externos;
- autenticação biométrica;
- Single Sign-On;
- protocolo de transporte;
- certificados e gerenciamento de segredos;
- política legal de retenção de credenciais;
- interface visual definitiva para perfis e permissões;
- catálogo final de todas as permissões;
- catálogo final de ações sensíveis;
- autenticação offline detalhada;
- regras de sincronização de permissões;
- segurança física da Máquina Principal;
- políticas completas de backup e resposta a incidentes.

Esses temas poderão ser adicionados futuramente, desde que não contradigam as decisões desta RFC.

---

## 5. Conceitos fundamentais

### 5.1 Identidade

Identidade é o registro persistente que representa uma pessoa reconhecida pelo Mheibos.

Ela não se confunde com:

- nome de exibição;
- conta do Windows;
- estação utilizada;
- sessão atual;
- perfil;
- função temporária em um processo.

A identidade deverá possuir identificador técnico estável e continuar referenciável mesmo após desativação do usuário.

### 5.2 Credencial

Credencial é o meio pelo qual o usuário prova sua identidade ao Mheibos.

Na primeira versão, a credencial principal será formada por identificador de acesso e senha própria do sistema.

A senha nunca deverá ser armazenada ou registrada em texto legível.

### 5.3 Perfil

Perfil é a função organizacional principal do usuário dentro do Mheibos.

Exemplos iniciais:

- Administrador;
- Gerente;
- Designer/Vendedor;
- Produção;
- Financeiro.

Os nomes poderão evoluir, mas o conceito permanecerá: cada usuário possui exatamente um perfil principal que fornece seu conjunto padrão de permissões.

### 5.4 Permissão

Permissão é uma capacidade autorizada sobre um recurso em determinado contexto.

Uma permissão não deverá ser reduzida a um único valor como “pode acessar módulo”. Ela poderá depender de:

- ação solicitada;
- tipo de entidade;
- registro específico;
- propriedade ou autoria;
- responsabilidade atual;
- estado da entidade;
- módulo ou contexto de origem;
- alcance individual, de equipe ou global;
- condição adicional de segurança.

### 5.5 Exceção individual

Exceção individual é uma alteração explícita das permissões padrão do perfil para um usuário específico.

Ela poderá:

- conceder capacidade adicional;
- restringir capacidade existente;
- limitar o alcance;
- impor condição adicional;
- possuir vigência temporária ou permanente.

Exceções não criam um segundo perfil.

### 5.6 Sessão

Sessão é o período autenticado em que uma identidade utiliza o Mheibos em uma estação.

A sessão deverá preservar, no mínimo:

- usuário;
- estação;
- início;
- última atividade relevante;
- contexto online ou offline;
- permissões efetivas carregadas;
- estado de encerramento;
- reautenticações realizadas para ações sensíveis.

### 5.7 Ação sensível

Ação sensível é uma operação que, por seu impacto comercial, financeiro, administrativo, operacional ou de segurança, exige confirmação adicional de identidade e auditoria reforçada.

### 5.8 Bloqueio de edição

Bloqueio de edição é uma reserva temporária de escrita sobre um registro sensível.

Ele não transfere propriedade da entidade. Apenas impede que duas pessoas alterem simultaneamente o mesmo registro de forma incompatível.

---

## 6. Autenticação própria do Mheibos

### 6.1 Independência do Windows

O Mheibos não utilizará a conta do Windows como identidade oficial do usuário.

Uma pessoa poderá acessar o sistema em estações diferentes utilizando suas próprias credenciais, respeitados os limites definidos para operação online e offline.

### 6.2 Autoridade da Central

Quando disponível, a Central deverá:

- validar a identidade;
- verificar o estado do usuário;
- validar a credencial;
- fornecer o perfil vigente;
- calcular ou disponibilizar permissões efetivas;
- registrar a sessão;
- informar restrições aplicáveis;
- negar acesso de usuários bloqueados ou desativados.

### 6.3 Estado do usuário

O registro do usuário deverá permitir estados equivalentes a:

- ativo;
- bloqueado temporariamente;
- senha expirada, caso a política futura adote esse conceito;
- desativado;
- aguardando ativação;
- recuperação administrativa.

Esses estados não deverão apagar o histórico da identidade.

### 6.4 Falha de autenticação

Tentativas recusadas deverão produzir registros de segurança suficientes para diagnóstico e proteção, sem registrar a senha informada.

A política concreta de limite de tentativas, atraso progressivo e bloqueio temporário será decidida na implementação.

### 6.5 Encerramento de sessão

A sessão deverá ser encerrada por:

- logout autorizado;
- encerramento da aplicação;
- expiração definida pela política;
- desativação ou bloqueio do usuário;
- intervenção administrativa autorizada;
- falha de segurança que exija revogação.

Restrições específicas relacionadas a dados offline pendentes pertencem à RFC-0008.

---

## 7. Um perfil principal por usuário

### 7.1 Regra

Cada usuário possuirá exatamente um perfil principal ativo.

Não será permitido acumular simultaneamente, por exemplo, os perfis “Designer/Vendedor” e “Financeiro” como duas identidades funcionais independentes.

### 7.2 Justificativa

A regra reduz:

- combinações imprevisíveis de permissões;
- conflitos de responsabilidade;
- dificuldade de auditoria;
- ambiguidade na interface;
- aumento descontrolado de privilégios;
- complexidade para explicar por que determinada ação foi autorizada.

### 7.3 Necessidades híbridas

Quando uma pessoa precisar de uma capacidade que não pertence ao seu perfil principal, o sistema deverá utilizar uma exceção individual explícita.

Exemplo:

> Um Designer/Vendedor autorizado a consultar uma categoria específica de relatório financeiro recebe uma concessão individual limitada, sem adquirir o perfil Financeiro.

### 7.4 Mudança de perfil

Trocar o perfil principal de um usuário será uma operação administrativa relevante.

A alteração deverá registrar:

- perfil anterior;
- novo perfil;
- autor da mudança;
- momento;
- justificativa, quando exigida pela política;
- impacto nas exceções existentes;
- vigência.

A mudança não poderá reescrever retroativamente as permissões utilizadas em eventos passados.

---

## 8. Perfis padrão

### 8.1 Finalidade

Perfis fornecem uma base previsível de acesso para pessoas que exercem funções semelhantes.

### 8.2 Perfis iniciais conceituais

A primeira versão poderá utilizar, entre outros, os seguintes perfis:

#### Administrador

Responsável por configurações amplas, usuários, perfis, políticas, exceções, segurança e manutenção autorizada da instalação.

#### Gerente

Responsável por supervisão operacional, indicadores globais autorizados, acompanhamento de equipe e decisões gerenciais.

#### Designer/Vendedor

Responsável por atendimento, criação ou edição de pedidos permitidos, acompanhamento de suas próprias vendas, metas, crescimento e relatórios individuais.

#### Produção

Responsável pela execução de etapas e processos produtivos dentro do escopo atribuído.

#### Financeiro

Responsável por pagamentos, saldos, cobranças, pendências e relatórios financeiros autorizados.

### 8.3 Perfis não são telas

Um perfil não deverá ser definido apenas pela lista de telas visíveis.

Ele deverá representar capacidades de negócio e escopos de acesso.

### 8.4 Evolução dos perfis

A empresa poderá ajustar nomes e permissões padrão, desde que:

- cada usuário continue com um único perfil principal;
- mudanças sejam auditadas;
- permissões críticas permaneçam protegidas;
- versões anteriores possam ser identificadas quando necessário.

---

## 9. Modelo de autorização

### 9.1 Regra geral

A autorização deverá considerar a combinação entre:

```text
Usuário autenticado
       +
Perfil principal
       +
Exceções individuais
       +
Ação solicitada
       +
Tipo de recurso
       +
Registro específico
       +
Propriedade ou responsabilidade
       +
Contexto e estado
       +
Alcance autorizado
       +
Condições de segurança
       =
Permissão efetiva
```

### 9.2 Dimensão da ação

Exemplos de ações diferentes:

- visualizar;
- criar;
- editar;
- concluir;
- cancelar;
- excluir do uso normal;
- exportar;
- aprovar;
- transferir;
- autorizar exceção;
- administrar política.

Permissão para visualizar não implica permissão para editar.

### 9.3 Dimensão do recurso

A autorização poderá variar por:

- Pedido;
- Processo;
- Etapa;
- Cliente;
- Pagamento;
- Pendência;
- Missão;
- Relatório;
- Usuário;
- Perfil;
- Política;
- Auditoria;
- Integração.

### 9.4 Dimensão da propriedade

O acesso poderá considerar relações como:

- criado pelo próprio usuário;
- vendido pelo próprio usuário;
- atribuído ao usuário;
- pertencente à equipe supervisionada;
- pertencente à organização inteira;
- sem relação direta, mas autorizado por função.

### 9.5 Dimensão do contexto

Uma ação poderá ser permitida somente em determinado estado ou fluxo.

Exemplo:

> Um usuário pode editar um pedido ainda não confirmado, mas precisa de autorização superior para alterar determinadas condições após o início da produção.

### 9.6 Dimensão do alcance

Os alcances conceituais poderão incluir:

- próprio;
- atribuído;
- equipe;
- setor;
- global;
- registro específico;
- conjunto temporário explicitamente delegado.

### 9.7 Negação explícita

Uma restrição individual deverá prevalecer sobre uma concessão padrão do perfil quando ambas se aplicarem ao mesmo contexto.

A ordem exata de resolução deverá ser implementada de modo determinístico e documentado.

---

## 10. Permissões efetivas

### 10.1 Composição

Permissões efetivas são o resultado calculado da combinação entre perfil, exceções, escopos e contexto.

### 10.2 Concessões individuais

Uma concessão deverá ser:

- específica;
- limitada ao necessário;
- associada a um autor administrativo;
- auditada;
- revisável;
- revogável;
- preferencialmente dotada de vigência quando temporária.

### 10.3 Restrições individuais

Uma restrição poderá remover ou limitar uma capacidade normalmente fornecida pelo perfil.

Exemplo:

> Um usuário mantém o perfil Designer/Vendedor, mas perde temporariamente a capacidade de aplicar descontos acima de determinado limite.

### 10.4 Proibição de privilégio implícito

A existência de acesso anterior, conhecimento de um endereço interno ou visibilidade de uma tela não concede permissão.

Toda operação deverá ser reavaliada no momento de execução.

### 10.5 Mudança durante a sessão

Quando permissões forem alteradas durante uma sessão ativa, a Central deverá possuir mecanismo para:

- invalidar ou atualizar o contexto de autorização;
- impedir uso indefinido de privilégios revogados;
- preservar operações já confirmadas;
- registrar a mudança.

O mecanismo concreto será definido na implementação.

---

## 11. Aplicação da autorização por camadas

### 11.1 Interface

A interface deverá:

- esconder ou desabilitar ações indisponíveis;
- explicar restrições quando apropriado;
- evitar induzir o usuário a operações impossíveis;
- adaptar módulos e comandos ao perfil.

Essa camada melhora a experiência, mas não constitui a autoridade final.

### 11.2 Cliente

O Cliente poderá realizar validações preventivas com base nas permissões conhecidas, mas não poderá conceder a si próprio uma capacidade negada pela Central.

### 11.3 Central

A Central deverá validar toda operação que altere o estado global.

A validação deverá ocorrer antes da persistência e antes do evento oficial de conclusão.

### 11.4 Casos de uso e domínio

Regras de autorização específicas do negócio deverão existir nos casos de uso e componentes responsáveis pela operação.

Exemplo:

> A permissão genérica de editar pedidos não substitui a regra específica que exige autorização superior para entregar um pedido com saldo em aberto.

### 11.5 Persistência

A arquitetura deverá impedir que um Cliente contorne a autorização por acesso direto ao banco.

Clientes não acessarão diretamente a persistência central, conforme RFC-0003.

### 11.6 Integrações

Webhooks, WhatsApp, ferramentas administrativas e futuras aplicações especializadas também deverão operar por identidades técnicas e permissões definidas, sem canais paralelos de autoridade.

---

## 12. Acesso a dados e indicadores

### 12.1 Regra padrão para usuários comuns

Usuários comuns acessarão por padrão os indicadores relacionados ao próprio trabalho.

Um Designer/Vendedor poderá consultar, conforme autorização:

- seus pedidos;
- suas vendas;
- suas metas;
- seu crescimento;
- seus relatórios individuais;
- processos e pendências sob sua responsabilidade.

### 12.2 Ausência de visão automática sobre terceiros

Acesso aos próprios indicadores não concede acesso automático:

- aos resultados de outros usuários;
- aos valores globais da empresa;
- aos relatórios gerenciais;
- a dados financeiros fora de seu escopo;
- a comparações individuais não autorizadas.

### 12.3 Visão gerencial

Gerentes poderão possuir acesso à equipe, ao setor ou à operação global conforme seu escopo.

### 12.4 Visão administrativa

Administradores poderão possuir visão ampla para administração e segurança, sem que isso elimine auditoria, reautenticação ou proteção de dados sensíveis.

### 12.5 Menor exposição

Mesmo quando um usuário possuir uma função ampla, a interface e a IA deverão apresentar apenas os dados necessários ao objetivo atual sempre que isso reduzir exposição sem prejudicar a operação.

---

## 13. Ações sensíveis

### 13.1 Definição

Ação sensível é toda operação que exige uma confirmação adicional por causa de seu impacto ou irreversibilidade operacional.

### 13.2 Exemplos conceituais

A lista inicial poderá incluir ações equivalentes a:

- cancelar pedido;
- excluir registro do uso normal;
- alterar pagamento;
- estornar valor;
- alterar autoria comercial;
- entregar pedido com saldo em aberto;
- modificar perfil;
- conceder ou retirar permissão;
- criar exceção individual;
- liberar bloqueio mantido por outro usuário;
- alterar política de segurança;
- restaurar backup;
- executar recuperação administrativa;
- exportar auditoria sensível;
- desativar usuário;
- modificar critérios oficiais de metas.

Esta lista é exemplificativa. A política concreta será configurável.

### 13.3 Classificação configurável

Administradores autorizados poderão:

- incluir uma ação na lista de sensibilidade;
- retirar uma ação da lista;
- definir quais perfis podem executá-la;
- exigir justificativa para categorias adicionais;
- limitar o alcance;
- estabelecer vigência.

Toda alteração da política será auditada.

### 13.4 Limites da configuração

A configurabilidade não autoriza eliminar proteções permanentes estabelecidas pelos princípios do projeto.

Determinadas ações poderão permanecer obrigatoriamente sensíveis por decisão futura normativa.

---

## 14. Reautenticação

### 14.1 Obrigatoriedade

Toda ação sensível deverá exigir a senha do usuário que a executa, mesmo que a sessão já esteja autenticada.

### 14.2 Finalidade

A reautenticação busca confirmar:

- presença consciente do executor;
- continuidade da identidade;
- intenção de realizar a ação;
- redução do risco de uso indevido de sessão aberta.

### 14.3 Executor real

A senha informada deverá pertencer ao usuário autenticado que assumirá autoria pela ação.

Não deverá ser permitido que um usuário comum peça a senha de outra pessoa para executar a ação dentro de sua própria sessão como se fosse o titular.

Fluxos formais de aprovação superior, quando existirem, deverão registrar separadamente solicitante e aprovador.

### 14.4 Validade limitada

Uma reautenticação deverá possuir validade curta e vinculada ao contexto da ação.

Ela não deverá transformar-se em liberação ampla e indefinida de operações sensíveis.

Os tempos concretos serão definidos na implementação.

### 14.5 Falha

Falhas de reautenticação deverão impedir a ação e produzir registro de segurança apropriado.

---

## 15. Justificativa de ações sensíveis

### 15.1 Usuários comuns

Usuários comuns autorizados deverão informar uma justificativa textual antes de concluir uma ação sensível.

### 15.2 Conteúdo

A justificativa deverá:

- ser explicitamente vinculada à ação;
- ser preservada na auditoria;
- estar disponível aos usuários autorizados;
- possuir conteúdo mínimo suficiente para explicar a decisão.

A implementação poderá rejeitar justificativas vazias ou evidentemente inválidas.

### 15.3 Administradores

Administradores autorizados poderão executar ações sensíveis sem justificativa textual obrigatória, quando a política permitir.

Isso não elimina:

- reautenticação;
- evento de segurança;
- autoria;
- valores anteriores e posteriores;
- auditoria imutável.

### 15.4 Política mais restritiva

A empresa poderá exigir justificativa também para administradores em ações específicas.

A dispensa normativa significa apenas que a justificativa não é obrigatória por padrão para toda ação administrativa.

---

## 16. Fluxo de ação sensível

```text
Usuário solicita operação
        ↓
Sistema verifica permissão inicial
        ↓
Sistema identifica ação sensível
        ↓
Interface explica impacto
        ↓
Sistema solicita senha do executor
        ↓
Usuário comum informa justificativa obrigatória
        ↓
Central revalida identidade, permissão, estado e bloqueio
        ↓
Operação é executada
        ↓
Evento registra ação, autoria, motivo e resultado
        ↓
Auditoria preserva valores anteriores e posteriores
```

Nenhuma etapa visual substitui a validação central.

---

## 17. Política configurável de segurança

### 17.1 Conteúdo da política

A política de ações sensíveis deverá poder representar:

- ação classificada;
- recurso afetado;
- perfis autorizados;
- escopo permitido;
- exigência de justificativa;
- necessidade de aprovação adicional, se futuramente adotada;
- vigência;
- versão;
- autor da configuração.

### 17.2 Lista padrão

O Mheibos deverá fornecer uma lista inicial de ações sensíveis coerente com os riscos da plataforma.

### 17.3 Alterações

Somente administradores autorizados poderão alterar a política.

### 17.4 Auditoria

Toda mudança deverá gerar evento contendo:

- regra anterior;
- regra nova;
- autor;
- momento;
- escopo;
- vigência;
- justificativa, quando exigida.

### 17.5 Aplicação histórica

Alterar a política não deverá reescrever retroativamente as regras utilizadas em ações anteriores.

A auditoria deverá permitir identificar qual política estava vigente no momento da operação.

---

## 18. Edição concorrente

### 18.1 Problema

Dois usuários alterando simultaneamente o mesmo registro sensível podem produzir:

- sobrescrita silenciosa;
- perda de dados;
- decisões incompatíveis;
- histórico confuso;
- erros financeiros ou operacionais.

### 18.2 Decisão

Ao entrar no modo de edição de um registro sensível, o usuário deverá adquirir um bloqueio temporário exclusivo de escrita.

### 18.3 Leitura compartilhada

Enquanto o bloqueio estiver ativo:

- outros usuários poderão visualizar o registro;
- a interface indicará que o registro está em edição;
- deverá ser exibido quem mantém o bloqueio, quando autorizado;
- ações de escrita conflitantes serão impedidas.

### 18.4 Escopo do bloqueio

O bloqueio deverá ser aplicado no menor escopo seguro.

Conforme o domínio, poderá incidir sobre:

- pedido completo;
- pagamento;
- etapa;
- política;
- usuário;
- conjunto transacional específico.

A granularidade concreta será definida por caso de uso, evitando tanto conflitos quanto bloqueios amplos desnecessários.

### 18.5 Aquisição central

Quando a Central estiver disponível, ela será a autoridade para conceder ou negar o bloqueio.

### 18.6 Bloqueio não é permissão

Adquirir bloqueio não concede capacidade de editar.

O usuário deverá possuir permissão antes e durante a confirmação da alteração.

---

## 19. Ciclo de vida dos bloqueios

### 19.1 Aquisição

O bloqueio deverá registrar:

- entidade ou escopo bloqueado;
- usuário;
- estação;
- sessão;
- início;
- última renovação;
- expiração prevista;
- finalidade ou modo de edição.

### 19.2 Renovação

Enquanto houver atividade válida de edição, o Cliente poderá renovar o bloqueio por meio de mecanismo de presença ou lease temporário.

### 19.3 Liberação normal

O bloqueio deverá ser liberado ao:

- salvar;
- cancelar;
- fechar a tela de edição;
- sair do modo de edição;
- encerrar a sessão;
- desconectar de forma reconhecida.

### 19.4 Expiração por inatividade

Bloqueios deverão expirar após período de inatividade suficiente para indicar abandono.

O tempo concreto deverá equilibrar:

- proteção contra perda de trabalho;
- continuidade dos demais usuários;
- realidade das tarefas demoradas.

### 19.5 Queda da estação

Se a estação falhar ou perder conexão, o bloqueio não poderá permanecer indefinidamente.

A Central deverá liberá-lo após expiração segura.

### 19.6 Liberação administrativa

Administrador autorizado poderá liberar um bloqueio quando necessário.

Essa ação será sensível e deverá exigir:

- reautenticação;
- auditoria;
- identificação do bloqueio liberado;
- preservação do usuário e estação anteriores;
- aviso ao usuário afetado quando possível.

### 19.7 Alteração após expiração

Um Cliente que perder o bloqueio não poderá salvar silenciosamente sobre uma versão mais recente.

Ele deverá receber erro compreensível e, quando possível, preservar o rascunho para revisão manual.

---

## 20. IA subordinada à identidade

### 20.1 Regra geral

A IA não possui um perfil próprio superior aos usuários.

Ela atua dentro da sessão e do contexto autorizado da pessoa que interage com o Mheibos.

### 20.2 Limites de consulta

A IA somente poderá consultar ou receber dados compatíveis com:

- identidade do usuário;
- permissões efetivas;
- escopo do objetivo atual;
- necessidade operacional.

### 20.3 Limites de resposta

A IA não poderá revelar ao usuário informações que ele não poderia consultar pelos módulos normais do sistema.

### 20.4 Limites de sugestão

A IA não deverá sugerir uma ação como disponível quando o usuário não possui permissão para executá-la.

Ela poderá explicar que determinada ação exige outro perfil ou autoridade, sem revelar dados indevidos.

### 20.5 Limites de execução

Quando a IA preparar uma ação:

- o usuário deverá possuir a permissão correspondente;
- ações sensíveis continuarão exigindo reautenticação;
- justificativas continuarão obrigatórias quando aplicáveis;
- bloqueios continuarão necessários;
- a Central validará a operação;
- a auditoria distinguirá sugestão, autorização humana e execução determinística.

### 20.6 Ausência de privilégio oculto

O fato de o Mheibos possuir conhecimento global na instalação não autoriza a IA a expor ou utilizar esse conhecimento fora do escopo permitido.

### 20.7 Proatividade

Intervenções proativas também deverão respeitar as permissões do destinatário.

Um usuário comum não deverá receber em um alerta dados globais que não poderia consultar diretamente.

---

## 21. Segurança de sessões

### 21.1 Vínculo

Cada sessão deverá estar vinculada a um usuário e uma estação.

### 21.2 Permissões carregadas

A sessão deverá possuir referência ao conjunto de permissões efetivas ou à versão utilizada, permitindo auditoria e atualização controlada.

### 21.3 Inatividade

A política poderá bloquear ou encerrar sessões após inatividade, especialmente em estações compartilhadas.

### 21.4 Troca de usuário

A troca de usuário exigirá encerramento ou suspensão segura da sessão anterior.

Não deverá ocorrer simples substituição visual da identidade mantendo o mesmo contexto de autorização.

### 21.5 Revogação

A Central deverá poder revogar sessões quando:

- o usuário for desativado;
- a senha for redefinida por segurança;
- houver alteração crítica de permissão;
- houver suspeita de comprometimento;
- um administrador autorizado encerrar a sessão.

### 21.6 Dados pendentes

Operações locais pendentes e regras de logout offline pertencem à RFC-0008 e deverão preservar autoria e segurança.

---

## 22. Negação de acesso

### 22.1 Comportamento

Quando uma operação for negada, o sistema deverá:

- não executar alteração parcial;
- informar o usuário de forma compreensível;
- evitar revelar detalhes sensíveis;
- registrar tentativa quando relevante;
- indicar a autoridade necessária quando isso for seguro e útil.

### 22.2 Motivos conceituais

A negação poderá ocorrer por:

- ausência de permissão;
- escopo insuficiente;
- estado incompatível;
- registro bloqueado;
- usuário desativado;
- sessão inválida;
- falha de reautenticação;
- justificativa ausente;
- política atualizada;
- conflito de versão;
- indisponibilidade da Central para operação que exige autoridade global.

### 22.3 Não exposição

Mensagens de erro não deverão revelar:

- senhas;
- tokens;
- regras internas desnecessárias;
- existência de dados altamente sensíveis fora do escopo;
- informações pessoais de outros usuários sem autorização.

---

## 23. Auditoria de identidade e segurança

### 23.1 Eventos obrigatórios

Deverão ser auditados, conforme aplicável:

- criação de usuário;
- ativação e desativação;
- login aceito;
- login recusado relevante;
- logout;
- revogação de sessão;
- mudança de perfil;
- concessão de permissão;
- retirada de permissão;
- exceção individual;
- alteração de política sensível;
- ação sensível executada;
- ação sensível recusada;
- reautenticação aceita ou recusada;
- bloqueio adquirido;
- bloqueio liberado;
- bloqueio expirado;
- liberação administrativa;
- tentativa de acesso negada relevante;
- execução de ação mediada pela IA.

### 23.2 Conteúdo

Os registros deverão preservar:

- usuário;
- estação;
- sessão;
- ação;
- recurso;
- escopo;
- permissão utilizada;
- resultado;
- política vigente;
- reautenticação;
- justificativa, quando aplicável;
- valores anteriores e posteriores;
- origem online ou offline quando pertinente.

### 23.3 Imutabilidade

A auditoria seguirá a RFC-0006 e não poderá ser reescrita silenciosamente por administradores.

---

## 24. Fluxos arquiteturais principais

### 24.1 Login online

```text
Usuário informa credenciais
        ↓
Cliente envia solicitação protegida
        ↓
Central localiza identidade
        ↓
Central valida credencial e estado do usuário
        ↓
Central carrega perfil e exceções
        ↓
Permissões efetivas são calculadas
        ↓
Sessão é criada
        ↓
Evento de autenticação é registrado
        ↓
Cliente recebe contexto autorizado
```

### 24.2 Operação comum autorizada

```text
Usuário solicita ação
        ↓
Interface verifica disponibilidade aparente
        ↓
Cliente envia comando à Central
        ↓
Central valida sessão, permissão, escopo e estado
        ↓
Caso de uso executa a operação
        ↓
Evento oficial é registrado
        ↓
Cliente atualiza a interface
```

### 24.3 Ação mediada pela IA

```text
IA identifica ou recebe solicitação
        ↓
Mheibos seleciona contexto permitido
        ↓
IA prepara sugestão
        ↓
Usuário confirma
        ↓
Central valida permissão do usuário
        ↓
Se sensível, exige senha e justificativa aplicável
        ↓
Operação determinística é executada
        ↓
Auditoria distingue sugestão, autorização e resultado
```

### 24.4 Edição com bloqueio

```text
Usuário entra no modo de edição
        ↓
Central valida permissão
        ↓
Central tenta adquirir bloqueio
        ↓
Bloqueio concedido ao usuário e sessão
        ↓
Demais usuários permanecem em leitura
        ↓
Usuário salva ou cancela
        ↓
Central valida novamente e persiste
        ↓
Bloqueio é liberado
```

---

## 25. Relação com operação offline

### 25.1 Fronteira

A autenticação offline, a identidade validada por estação, as permissões sincronizadas e a troca de usuário sem Central pertencem à RFC-0008.

### 25.2 Princípios que permanecem válidos

Mesmo offline:

- a identidade deverá ser própria do Mheibos;
- permissões deverão derivar da última autoridade central válida;
- a IA não poderá ultrapassar o usuário;
- ações locais permitidas deverão preservar autoria;
- eventos indicarão origem offline;
- nenhuma estação poderá criar novas permissões globais.

### 25.3 Restrições

A ausência da Central poderá impedir operações que dependam de:

- revalidação de política atual;
- bloqueio global;
- acesso a dados globais atualizados;
- ação sensível com autoridade central;
- troca para usuário não previamente autorizado naquela estação.

As regras detalhadas serão normatizadas no RFC-0008.

---

## 26. Requisitos de segurança

### 26.1 Menor privilégio

Usuários e componentes deverão receber somente as capacidades necessárias às suas responsabilidades.

### 26.2 Negação por padrão

Na ausência de concessão aplicável, a operação deverá ser negada.

### 26.3 Defesa em profundidade

A segurança deverá existir em múltiplas camadas:

- interface;
- Cliente;
- comunicação;
- Central;
- casos de uso;
- persistência;
- auditoria.

### 26.4 Credenciais protegidas

Senhas e segredos não deverão ser armazenados em texto legível nem enviados a componentes que não precisem validá-los.

### 26.5 Sessões revogáveis

A Central deverá conseguir revogar sessões e impedir uso continuado de acesso removido.

### 26.6 Explicabilidade

O sistema deverá ser capaz de explicar por que uma operação foi permitida ou negada em termos compreensíveis e auditáveis, sem expor detalhes inseguros.

### 26.7 Consistência

A mesma operação, com o mesmo usuário, recurso, estado e política, deverá produzir a mesma decisão de autorização.

### 26.8 Disponibilidade proporcional

Mecanismos de segurança não deverão tornar operações comuns perceptivelmente lentas, mas ações de maior risco poderão exigir etapas adicionais conscientes.

---

## 27. Falhas e situações previstas

### 27.1 Central indisponível

O Cliente deverá aplicar somente capacidades offline explicitamente permitidas, sem simular autoridade global.

### 27.2 Permissão alterada durante edição

Antes de salvar, a Central deverá validar novamente a autorização.

Perder permissão durante a edição impedirá a persistência, ainda que o usuário tenha adquirido o bloqueio anteriormente.

### 27.3 Bloqueio expirado

O Cliente deverá impedir salvamento silencioso e informar que a edição perdeu a reserva.

### 27.4 Sessão revogada

A operação deverá ser recusada e o usuário deverá autenticar-se novamente.

### 27.5 Política alterada

Uma ação iniciada sob política antiga deverá ser revalidada antes da execução se ainda não tiver sido confirmada.

### 27.6 Falha de auditoria

Uma ação sensível não deverá ser apresentada como concluída se o evento obrigatório não puder ser preservado de forma durável.

### 27.7 Falha da IA

A indisponibilidade cognitiva não altera permissões e não impede operações determinísticas autorizadas.

---

## 28. Requisitos de qualidade

### 28.1 Clareza

Usuários deverão compreender suas capacidades e limitações sem precisar conhecer a arquitetura interna.

### 28.2 Previsibilidade

Perfis e exceções deverão produzir resultados consistentes.

### 28.3 Auditabilidade

Toda mudança de acesso ou segurança deverá possuir autoria e histórico.

### 28.4 Granularidade adequada

Permissões não deverão ser tão amplas que exponham dados desnecessários, nem tão fragmentadas que tornem a administração inviável.

### 28.5 Administração segura

Ferramentas administrativas deverão estar sujeitas às mesmas regras de reautenticação, auditoria e menor privilégio.

### 28.6 Recuperação

Falhas de estação, sessão ou bloqueio não deverão causar perda silenciosa de dados nem manter reservas indefinidas.

### 28.7 Desempenho

A verificação de permissões deverá ser rápida o suficiente para não comprometer a responsividade da rede local.

---

## 29. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | propósito e autoridade humana no Mheibos |
| RFC-0001 | segurança, fonte da verdade, explicabilidade e limites permanentes |
| RFC-0002 | responsabilidades, processos, estados e ações operacionais |
| RFC-0003 | Central, Clientes, contratos e fronteiras técnicas |
| RFC-0004 | identidade cognitiva e limites da IA |
| RFC-0005 | Usuário, Perfil, Sessão, Estação e representação estrutural das permissões |
| RFC-0006 | eventos, ações sensíveis, mudanças de perfil, políticas e auditoria imutável |
| RFC-0008 | autenticação offline, permissões sincronizadas e troca de usuário |
| RFC-0009 | adaptação visual conforme perfil e apresentação de bloqueios ou confirmações |
| RFC-0010 | autoridade e participação em Missões e Teamwork |
| RFC-0011 | acesso a conhecimento e memória conforme escopo |
| RFC-0012 | destinatários, responsáveis e visibilidade de pendências |
| RFC-0013 | autorizações financeiras, metas, cobranças e entrega com saldo |
| RFC-0014 | identidades técnicas de integrações e acesso a arquivos e WhatsApp |
| RFC-0015 | acesso a dashboards, indicadores e simulações |
| RFC-0016 | governança, aprovação e segurança da IA |

Esta RFC define quem pode fazer o quê, em qual contexto e com quais proteções. Os demais RFCs definem o significado das operações, dos dados e das intervenções.

---

## 30. Consequências da decisão

### 30.1 Benefícios

- identidade independente das estações e do Windows;
- auditoria clara por pessoa;
- permissões previsíveis por função;
- flexibilidade por exceções individuais sem múltiplos perfis;
- menor exposição de dados;
- proteção de ações críticas;
- redução de uso indevido de sessões abertas;
- prevenção de sobrescritas concorrentes;
- IA incapaz de contornar a segurança;
- base compatível com futuras aplicações especializadas.

### 30.2 Custos

- necessidade de serviço central de identidade;
- administração de perfis e exceções;
- maior complexidade de autorização contextual;
- implementação de reautenticação;
- mecanismos de bloqueio e expiração;
- auditoria de mudanças de segurança;
- necessidade de atualizar sessões após mudanças de permissão;
- tratamento de falhas e conflitos de edição.

### 30.3 Riscos

- transformar perfis em listas excessivamente amplas;
- conceder muitas exceções individuais e perder previsibilidade;
- confiar apenas na interface para negar ações;
- manter permissões antigas em sessões ativas;
- permitir ações sensíveis sem senha;
- aceitar justificativas vazias ou inúteis;
- deixar administradores fora da auditoria;
- manter bloqueios abandonados;
- permitir salvamento após perda do bloqueio;
- expor dados globais pela IA a usuários sem autorização;
- confundir posse do bloqueio com permissão de editar;
- criar mensagens de erro que revelem informações sensíveis.

---

## 31. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. cada usuário possuir credenciais próprias do Mheibos;
2. a conta do Windows não for utilizada como identidade oficial;
3. a Central for a autoridade de autenticação e autorização quando disponível;
4. cada usuário possuir exatamente um perfil principal;
5. necessidades adicionais forem representadas por exceções individuais auditadas;
6. permissões considerarem ação, recurso, propriedade, contexto e alcance;
7. negar ou ocultar um botão não for a única barreira de segurança;
8. operações globais forem validadas pela Central antes da persistência;
9. usuários comuns acessarem seus próprios indicadores por padrão, sem visão automática sobre terceiros;
10. ações sensíveis exigirem reautenticação com a senha do executor;
11. usuários comuns autorizados informarem justificativa textual em ações sensíveis;
12. administradores não puderem dispensar reautenticação ou auditoria;
13. a política de ações sensíveis puder ser alterada apenas por administradores autorizados;
14. mudanças nessa política produzirem auditoria imutável;
15. registros sensíveis utilizarem bloqueio temporário de escrita quando houver risco de concorrência;
16. demais usuários continuarem com leitura durante o bloqueio, quando autorizados;
17. bloqueios forem liberados ao salvar, cancelar, fechar, desconectar, encerrar sessão ou expirar;
18. liberação administrativa de bloqueio exigir autorização e auditoria;
19. a IA somente acessar, sugerir e executar capacidades compatíveis com o usuário atual;
20. nenhuma ação mediada pela IA contornar senha, justificativa, bloqueio ou validação central;
21. mudanças de perfil, permissões, exceções e sessões forem auditadas;
22. credenciais e segredos não forem gravados em texto legível;
23. permissões revogadas não permanecerem utilizáveis indefinidamente em sessões antigas;
24. falha da IA não alterar a autoridade nem as regras determinísticas.

---

## 32. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em documentos posteriores:

- formato definitivo do nome de usuário;
- política de complexidade de senha;
- algoritmo de hash e parâmetros;
- recuperação e redefinição de senha;
- autenticação multifator;
- duração padrão das sessões;
- duração da validade de reautenticação;
- número de tentativas antes de bloqueio;
- tempo de expiração dos bloqueios de edição;
- granularidade final de cada bloqueio;
- catálogo completo de permissões;
- catálogo inicial completo de ações sensíveis;
- interface de administração de perfis;
- fluxo de aprovação superior;
- delegações temporárias;
- vigência automática de exceções;
- alertas de acessos anormais;
- integração futura com identidade corporativa;
- política de autenticação para aplicações especializadas;
- mecanismo técnico de invalidação de sessão;
- armazenamento seguro de credenciais offline.

Essas escolhas deverão respeitar as decisões, fronteiras e critérios desta RFC.

---

## 33. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-030 — autenticação própria do Mheibos | 6 |
| INV-031 — exatamente um perfil por usuário | 7 |
| INV-032 — permissões por função e escopo | 9, 10 e 11 |
| INV-033 — perfis padrão e exceções individuais | 8 e 10 |
| INV-034 — indicadores próprios por padrão | 12 |
| INV-035 — ações sensíveis exigem reautenticação | 13, 14 e 16 |
| INV-036 — usuários comuns justificam ações sensíveis | 15 e 16 |
| INV-037 — política configurável de ações sensíveis | 13.3 e 17 |
| INV-038 — bloqueio temporário de edição | 18 |
| INV-039 — liberação e expiração de bloqueios | 19 |
| INV-040 — IA herda os limites do usuário | 20 |

---

## 34. Declaração normativa

Todo acesso humano ao Mheibos será realizado por identidade e credenciais próprias do sistema, independentes da conta do Windows. A Central será a autoridade de autenticação, perfis, permissões e políticas oficiais.

Cada usuário possuirá exatamente um perfil principal. Perfis fornecerão permissões padrão, e necessidades particulares serão atendidas por exceções individuais explícitas, limitadas e auditadas. A autorização considerará ação, recurso, propriedade, responsabilidade, contexto e alcance. Nenhuma operação será considerada protegida apenas porque uma tela ou botão foi ocultado.

Usuários comuns acessarão por padrão seus próprios indicadores e dados operacionais autorizados. Visões de equipe ou globais dependerão de permissão específica.

Toda ação classificada como sensível exigirá reautenticação com a senha do usuário que a executa. Usuários comuns autorizados deverão registrar justificativa textual. Administradores autorizados poderão dispensar a justificativa quando a política permitir, mas nunca a reautenticação ou a auditoria.

A política de ações sensíveis será configurável por administradores autorizados e toda alteração será auditada. Registros sensíveis utilizarão bloqueios temporários de escrita, preservando leitura para os demais usuários autorizados. Bloqueios serão liberados por conclusão, cancelamento, encerramento, desconexão, expiração ou intervenção administrativa auditada.

A Inteligência Artificial não possuirá privilégios próprios ou ocultos. Ela herdará os limites do usuário autenticado e não poderá consultar, revelar, sugerir ou executar ações fora do escopo permitido. Toda ação mediada pela IA continuará sujeita às mesmas permissões, reautenticação, justificativa, bloqueio, validação central e auditoria aplicáveis a uma ação humana direta.
