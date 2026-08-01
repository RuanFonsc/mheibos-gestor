# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0003 — Arquitetura Técnica da Plataforma

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-014 a INV-023

---

## 1. Resumo

Esta RFC define a arquitetura técnica da primeira versão do Mheibos.

O Mheibos será uma plataforma desktop distribuída, instalada na rede local da empresa e composta por uma **Central**, executada na Máquina Principal, e por **Clientes Mheibos**, executados nas estações de trabalho.

A Central será a autoridade global da instalação. Os Clientes fornecerão a experiência operacional dos usuários, manterão autonomia local limitada e se comunicarão com a Central para acessar o estado compartilhado, autenticação, regras e serviços comuns.

A primeira versão será implantada e testada localmente na empresa piloto. Arquitetura em nuvem, múltiplas empresas e aplicações especializadas futuras não fazem parte desta versão, embora a plataforma deva evitar dependências que impeçam essa evolução.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- onde cada parte do Mheibos será executada;
- como a Máquina Principal e as estações se relacionam;
- quais são os componentes técnicos permanentes da plataforma;
- quais responsabilidades pertencem à Central e aos Clientes;
- como a aplicação principal será organizada;
- quais fronteiras deverão impedir acoplamentos indevidos;
- como a arquitetura inicial poderá evoluir sem ser reescrita.

Esta RFC não especifica o comportamento interno detalhado de eventos, dados, permissões, sincronização, IA, interface viva, missões ou integrações. Esses temas pertencem aos RFCs indicados na seção de fronteiras.

---

## 3. Decisões fundamentais

A arquitetura técnica da primeira versão adota as seguintes decisões:

1. O Mheibos será uma aplicação desktop instalada localmente.
2. A implantação será distribuída entre uma Central e múltiplos Clientes.
3. A Central será executada na Máquina Principal e será a autoridade global.
4. A Máquina Principal também poderá funcionar como estação administrativa.
5. Os Clientes terão autonomia local limitada, sem autoridade para criar regras globais.
6. A indisponibilidade temporária da Máquina Principal será uma condição prevista.
7. O Mheibos Gestor será uma aplicação integrada, com módulos visíveis e utilizáveis sem interação obrigatória com a IA.
8. Aplicações especializadas futuras deverão obedecer à mesma Central.
9. O modelo de IA inicial será único, pequeno, local e substituível.
10. A evolução para nuvem e múltiplas empresas será posterior e exigirá revisão arquitetural própria.

---

## 4. Escopo da primeira versão

### 4.1 Incluído

A primeira versão compreende:

- uma implantação dentro de uma única empresa;
- uma Máquina Principal na rede local;
- uma Central do Mheibos executada nessa máquina;
- um Cliente Mheibos instalado na Máquina Principal;
- Clientes Mheibos instalados nas demais estações autorizadas;
- comunicação entre Clientes e Central pela rede local;
- persistência central do estado compartilhado;
- persistência local mínima necessária a cada Cliente;
- serviços centrais de autenticação, regras, sincronização e coordenação;
- uma fronteira cognitiva opcional e substituível, mantida desligada na implantação atual;
- uma aplicação principal integrada denominada Mheibos Gestor.

### 4.2 Fora do escopo

Não fazem parte desta RFC:

- implantação em nuvem;
- arquitetura multitenant;
- hospedagem de várias empresas na mesma Central;
- aplicativo web como experiência principal;
- aplicativo móvel;
- Mheibos Vendas;
- Mheibos Produção;
- conselho de múltiplos modelos de IA;
- escolha definitiva do modelo de linguagem;
- definição do esquema completo do banco de dados;
- protocolo detalhado de sincronização offline;
- regras detalhadas de autenticação e autorização;
- implementação detalhada de eventos e auditoria;
- comportamento cognitivo da IA;
- especificação visual da interface.

A exclusão desses temas não significa rejeição. Significa apenas que possuem RFCs próprios ou pertencem a fases posteriores.

---

## 5. Visão geral da arquitetura

```text
┌──────────────────────────────────────────────────────────────┐
│                     REDE LOCAL DA EMPRESA                    │
│                                                              │
│  ┌──────────────────── Máquina Principal ─────────────────┐  │
│  │                                                        │  │
│  │  ┌───────────────┐       ┌─────────────────────────┐  │  │
│  │  │ Mheibos Gestor│       │     Central Mheibos     │  │  │
│  │  │ Administrativo│◄─────►│                         │  │  │
│  │  └───────────────┘       │ API / Coordenação       │  │  │
│  │                          │ Estado Global            │  │  │
│  │                          │ Regras e Autorização     │  │  │
│  │                          │ Serviços Compartilhados  │  │  │
│  │                          │ Persistência Central     │  │  │
│  │                          │ Gateway de IA            │  │  │
│  │                          └────────────┬────────────┘  │  │
│  └──────────────────────────────────────┼───────────────┘  │
│                                         │                  │
│                         Rede local / protocolo interno      │
│                  ┌──────────────────────┼────────────────┐ │
│                  │                      │                │ │
│          ┌───────▼────────┐    ┌────────▼───────┐       │ │
│          │ Cliente Mheibos│    │ Cliente Mheibos│  ...  │ │
│          │ Estação A      │    │ Estação B      │       │ │
│          │ UI + cache     │    │ UI + cache     │       │ │
│          │ serviços locais│    │ serviços locais│       │ │
│          └────────────────┘    └────────────────┘       │ │
└──────────────────────────────────────────────────────────────┘
```

A Central concentra a autoridade e os serviços compartilhados. Os Clientes concentram a experiência do usuário e os recursos necessários para operar a estação.

---

## 6. Topologia de implantação

### 6.1 Máquina Principal

A Máquina Principal é o equipamento que hospeda a Central da instalação local.

Ela deverá executar, no mínimo:

- o processo principal da Central;
- a API ou protocolo interno de comunicação;
- a persistência central;
- os serviços compartilhados da instalação;
- o gateway de acesso ao modelo de IA;
- os mecanismos de inicialização, supervisão e diagnóstico dos serviços.

Ela também poderá executar o Mheibos Gestor como estação administrativa. Essa possibilidade facilita o acompanhamento da Central e reduz a necessidade de uma máquina exclusivamente dedicada na fase inicial.

A coexistência entre Central e estação administrativa não significa que os dois componentes sejam a mesma aplicação. Eles devem permanecer logicamente separados, com ciclos de vida, responsabilidades e interfaces próprias.

### 6.2 Estações de trabalho

Cada estação autorizada executará um Cliente Mheibos.

O Cliente deverá conter:

- a interface desktop;
- a sessão do usuário;
- os adaptadores de comunicação com a Central;
- o armazenamento local necessário;
- a fila local de operações permitidas;
- os serviços da estação;
- os mecanismos de integração com o sistema operacional;
- o acesso controlado aos recursos locais necessários ao trabalho.

### 6.3 Rede local

A comunicação entre Clientes e Central ocorrerá prioritariamente pela rede local da empresa.

A arquitetura não deverá pressupor disponibilidade permanente da internet para o funcionamento básico da primeira versão.

A descoberta da Central, o endereçamento, a criptografia do transporte, as portas, os certificados e os protocolos concretos serão decisões de implementação subordinadas aos requisitos de segurança e implantação.

---

## 7. Central Mheibos

### 7.1 Papel

A Central é a autoridade global da instalação.

Ela mantém a visão oficial e compartilhada do sistema e coordena todos os Clientes conectados.

### 7.2 Responsabilidades

Pertencem à Central:

- autenticar identidades quando disponível;
- fornecer permissões e políticas oficiais;
- consolidar o estado global;
- validar operações que dependam de autoridade central;
- coordenar bloqueios de edição;
- receber e distribuir atualizações;
- executar serviços compartilhados;
- manter o acesso à persistência central;
- disponibilizar o conhecimento organizacional;
- intermediar o acesso ao modelo de IA;
- registrar saúde, disponibilidade e falhas dos componentes centrais;
- expor contratos estáveis para Clientes e aplicações futuras.

### 7.3 Restrições

A Central não deverá:

- depender da interface administrativa para continuar executando;
- incorporar diretamente regras visuais específicas de uma tela;
- depender de um modelo de IA específico;
- permitir que um Cliente substitua silenciosamente uma regra oficial;
- misturar dados globais com estados temporários exclusivamente visuais de uma estação.

---

## 8. Cliente Mheibos

### 8.1 Papel

O Cliente é a aplicação utilizada pelo usuário em sua estação.

Ele apresenta o Mheibos Gestor, executa interações locais e mantém a continuidade operacional permitida quando a Central estiver temporariamente indisponível.

### 8.2 Responsabilidades

Pertencem ao Cliente:

- renderizar a interface desktop;
- aplicar a experiência correspondente ao usuário autenticado;
- enviar comandos e consultas à Central;
- manter cache e dados locais autorizados;
- preservar operações locais pendentes;
- detectar disponibilidade da Central;
- informar claramente o estado de conectividade;
- integrar-se ao Windows e aos aplicativos locais quando autorizado;
- executar adaptações temporárias da interface;
- apresentar notificações e intervenções;
- impedir que uma ausência de conexão seja confundida com operação global normal.

### 8.3 Autonomia limitada

O Cliente poderá tomar decisões locais somente dentro das regras previamente fornecidas pela Central e dos limites definidos para operação offline.

O Cliente não poderá:

- criar uma permissão global;
- alterar uma política oficial;
- declarar um estado global sem sincronização;
- acessar dados não autorizados;
- assumir que sua cópia local é mais recente que a Central;
- transformar uma preferência visual local em regra da empresa.

---

## 9. Mheibos Gestor

### 9.1 Aplicação integrada

O Mheibos Gestor será o ambiente principal de trabalho da primeira versão.

Pedidos, clientes, processos, dashboards, notificações, assistência da IA e demais funções atuais serão acessíveis dentro da mesma aplicação.

Essa integração deverá reduzir trocas desnecessárias de contexto sem transformar o programa em um bloco monolítico impossível de evoluir.

### 9.2 Organização modular interna

Embora a experiência seja integrada, o código deverá ser organizado em módulos internos com contratos explícitos.

Um módulo de interface não deverá acessar diretamente o armazenamento central nem incorporar regras de negócio que pertencem ao núcleo da plataforma.

A separação mínima deverá considerar:

- apresentação;
- casos de uso da aplicação;
- domínio e regras;
- infraestrutura;
- comunicação com a Central;
- integração com recursos locais;
- IA e orquestração de interface por adaptadores.

### 9.3 Navegação principal

Os módulos visíveis continuarão sendo a forma principal e confiável de navegação.

O usuário deverá conseguir operar o Gestor sem conversar com a IA.

A IA poderá acelerar, orientar e reorganizar a experiência, mas não será uma dependência obrigatória para localizar ou executar as funções normais do sistema.

---

## 10. Componentes lógicos da plataforma

A arquitetura deverá possuir componentes lógicos equivalentes aos seguintes. Os nomes concretos no código poderão variar, mas suas responsabilidades não deverão ser misturadas sem justificativa formal.

### 10.1 Host da Central

Responsável por inicializar, supervisionar e encerrar ordenadamente os serviços centrais.

### 10.2 API ou Barramento de Comunicação

Contrato interno usado por Clientes e futuras aplicações para consultar e comandar a Central.

Deverá esconder detalhes de persistência e impedir acesso direto dos Clientes ao banco central.

### 10.3 Núcleo da Aplicação

Coordena casos de uso e aplica as decisões do domínio por meio dos motores e serviços adequados.

### 10.4 Persistência Central

Mantém o estado compartilhado e os registros oficiais da instalação.

O banco e seu modelo detalhado pertencem à RFC-0005.

### 10.5 Armazenamento Local do Cliente

Mantém configurações, cache, credenciais offline protegidas e operações locais permitidas.

Seu comportamento detalhado pertence à RFC-0008.

### 10.6 Motor de Regras

Executa validações determinísticas e não depende do modelo de IA para decidir permissões, restrições ou transições oficiais.

As regras conceituais surgem do RFC-0002; seus eventos e auditoria pertencem ao RFC-0006.

### 10.7 Serviço de Identidade e Autorização

Fornece identidade, perfil, permissões e escopos ao restante da plataforma.

Sua especificação pertence à RFC-0007.

### 10.8 Serviço de Sincronização

Coordena a incorporação de operações locais e a atualização dos Clientes.

Sua especificação pertence à RFC-0008.

### 10.9 Gateway de IA

É a única fronteira autorizada entre a plataforma e o modelo de linguagem.

Ele deverá:

- esconder o fornecedor e o formato específico do modelo;
- permitir substituição do modelo;
- controlar contexto e recursos enviados;
- aplicar limites de execução;
- devolver resultados estruturados ao Mheibos;
- impedir que o modelo acesse diretamente o banco ou a interface.

### 10.10 Orquestrador de Interface

Traduz comandos estruturados e autorizados em ações visuais no Cliente.

Sua especificação funcional pertence à RFC-0009.

### 10.11 Adaptadores de Integração

Encapsulam acesso ao Windows, arquivos, programas externos, WhatsApp, webhooks e futuras integrações.

Sua especificação pertence à RFC-0014.

### 10.12 Observabilidade e Diagnóstico

Registra saúde, falhas, disponibilidade, consumo de recursos e estado dos serviços, sem substituir a auditoria de negócio.

---

## 11. Fluxos arquiteturais principais

### 11.1 Operação online comum

```text
Usuário
  ↓
Cliente Mheibos
  ↓ comando estruturado
API da Central
  ↓
Núcleo da Aplicação
  ↓
Motor de Regras / Serviços de Domínio
  ↓
Persistência Central
  ↓ resultado
Central
  ↓
Cliente atualiza a interface
```

A interface deverá responder de forma rápida. Processamentos secundários poderão ser desacoplados, desde que consistência, rastreabilidade e notificações sejam preservadas.

### 11.2 Consulta assistida pela IA

```text
Usuário ou estado operacional
  ↓
Mheibos
  ↓ seleção controlada de contexto
Gateway de IA
  ↓
Modelo local substituível
  ↓ resultado estruturado
Mheibos valida permissões e contexto
  ↓
Resposta, sugestão ou comando visual autorizado
```

O modelo não acessa diretamente o banco, não controla diretamente a interface e não se torna fonte oficial do estado.

### 11.3 Indisponibilidade da Central

```text
Cliente detecta perda da Central
  ↓
Ativa modo offline restrito
  ↓
Mantém consulta local permitida
  ↓
Aceita somente operações locais autorizadas
  ↓
Preserva operações pendentes
  ↓
Detecta retorno da Central
  ↓
Inicia sincronização automática e visível
```

As regras completas desse fluxo pertencem à RFC-0008.

---

## 12. Fronteiras obrigatórias

### 12.1 Cliente não acessa diretamente o banco central

Toda leitura ou alteração do estado global deverá passar por contratos da Central.

### 12.2 Interface não contém autoridade de negócio

Ocultar um botão não equivale a negar uma permissão. As regras oficiais deverão ser verificadas fora da camada visual.

### 12.3 IA não acessa diretamente recursos internos

O modelo deverá receber somente o contexto selecionado e devolver resultados que o Mheibos possa validar.

### 12.4 Modelo não armazena o conhecimento oficial

Conhecimento, memória, procedimentos e histórico deverão permanecer em componentes próprios da plataforma. Trocar o modelo não poderá apagar a inteligência acumulada.

### 12.5 Estado local não substitui estado global

Dados locais servem à continuidade controlada e à experiência da estação. O estado compartilhado oficial pertence à Central.

### 12.6 Aplicações futuras usam contratos públicos internos

Mheibos Vendas, Mheibos Produção e outros Clientes não deverão duplicar a Central nem acessar internamente seus bancos. Eles deverão consumir os mesmos contratos autorizados.

---

## 13. Modelo de IA na primeira versão

A arquitetura inicial deverá priorizar um único modelo de poucos parâmetros, executado localmente e compatível com a infraestrutura de pequenas e médias gráficas.

O modelo concreto não é definido nesta RFC.

A plataforma deverá tratá-lo como uma dependência substituível por meio do Gateway de IA.

A qualidade do Mheibos não deverá depender exclusivamente do tamanho do modelo. Ela deverá surgir da combinação entre:

- dados oficiais;
- contexto selecionado;
- regras determinísticas;
- memória externa ao modelo;
- ferramentas controladas;
- validação dos resultados;
- experiência integrada da interface.

Múltiplos modelos cooperativos poderão ser estudados futuramente, mas não serão requisito nem fundamento da primeira versão.

---

## 14. Disponibilidade e falhas previstas

### 14.1 Queda da Máquina Principal

A indisponibilidade temporária da Central é um evento esperado, especialmente em razão de quedas de energia.

O sistema deverá detectar essa condição, informar o usuário e aplicar o modo offline restrito, sem simular que a instalação permanece globalmente sincronizada.

### 14.2 Queda de um Cliente

A falha de uma estação não deverá interromper a Central nem os demais Clientes.

Operações locais não sincronizadas deverão ser preservadas conforme a RFC-0008.

### 14.3 Falha do modelo de IA

A indisponibilidade da IA não deverá impedir o uso normal dos módulos essenciais do Gestor.

Funções determinísticas, consultas, pedidos, processos e demais operações autorizadas deverão continuar disponíveis, ainda que recursos cognitivos e sugestões fiquem temporariamente indisponíveis.

### 14.4 Falha de integração externa

Uma integração indisponível não deverá derrubar o Gestor inteiro. O adaptador deverá isolar a falha, preservar dados pendentes e apresentar estado compreensível ao usuário.

### 14.5 Reinicialização ordenada

Central e Clientes deverão conseguir recuperar seu estado operacional após encerramento inesperado, preservando consistência e identificando operações incompletas.

---

## 15. Requisitos de qualidade arquitetural

### 15.1 Acessibilidade econômica

A primeira versão deverá funcionar em infraestrutura compatível com pequenas e médias empresas, evitando dependências obrigatórias de nuvem, múltiplas GPUs ou conjuntos de modelos caros.

### 15.2 Substituibilidade

Banco, modelo de IA, mecanismo de transporte e integrações externas deverão ser encapsulados por interfaces, reduzindo o impacto de futuras trocas.

### 15.3 Modularidade

Componentes deverão possuir responsabilidades claras e comunicação explícita. A aplicação integrada não poderá resultar em acoplamento indiscriminado.

### 15.4 Continuidade controlada

Falhas parciais deverão degradar capacidades específicas, e não derrubar automaticamente toda a plataforma.

### 15.5 Segurança por camadas

Permissões deverão ser verificadas na Central e nos casos de uso, não apenas na interface. Dados locais e credenciais deverão ser protegidos.

### 15.6 Observabilidade

Falhas técnicas deverão ser diagnosticáveis por registros, indicadores de saúde e mensagens de erro acionáveis.

### 15.7 Experiência responsiva

A distribuição entre Central e Clientes não poderá transformar interações comuns em operações perceptivelmente lentas na rede local.

---

## 16. Evolução futura

### 16.1 Nuvem

A migração para nuvem deverá substituir a topologia de implantação sem destruir os contratos lógicos entre Central e Clientes.

Ela exigirá decisões específicas sobre:

- multitenancy;
- isolamento entre empresas;
- disponibilidade contínua;
- segurança externa;
- conectividade pela internet;
- atualizações remotas;
- custos e escalabilidade;
- localização e governança de dados.

Essas decisões não serão antecipadas nesta RFC.

### 16.2 Aplicações especializadas

Mheibos Vendas, Mheibos Produção e outras aplicações poderão tornar-se Clientes especializados da mesma Central.

Elas deverão compartilhar:

- identidades;
- permissões;
- processos;
- estados;
- eventos;
- conhecimento;
- contratos de comunicação.

### 16.3 Modelos maiores ou múltiplos

Clientes com infraestrutura superior poderão futuramente utilizar modelos maiores ou serviços especializados, desde que o Gateway de IA preserve os mesmos contratos e limites.

---

## 17. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0004 | Papel, raciocínio, proatividade e limites cognitivos da IA |
| RFC-0005 | Entidades, relacionamentos, estados e persistência |
| RFC-0006 | Eventos, evidências, auditoria e processamento desacoplado |
| RFC-0007 | Identidade, perfis, permissões, ações sensíveis e bloqueios |
| RFC-0008 | Operação offline, armazenamento local e sincronização |
| RFC-0009 | Orquestração da interface, personalização e intervenções |
| RFC-0010 | Missões, workspaces e Teamwork |
| RFC-0011 | Conhecimento, memória e aprendizado |
| RFC-0012 | Pendências, lembretes, scheduler e escalonamento |
| RFC-0013 | Pedidos, metas, pagamentos e regras financeiras |
| RFC-0014 | Arquivos, WhatsApp, webhooks e integrações |
| RFC-0015 | Dashboard, analytics e simulações |
| RFC-0016 | Governança e segurança da IA |

Nenhuma dessas especificações deverá ser incorporada integralmente à RFC-0003. Esta RFC fornece somente a plataforma na qual elas serão implementadas.

---

## 18. Consequências da decisão

### 18.1 Benefícios

- funcionamento local sem dependência obrigatória de nuvem;
- custo inicial menor;
- autoridade central clara;
- experiência integrada para os usuários;
- continuidade limitada durante falhas da Central;
- possibilidade de trocar o modelo de IA;
- caminho de evolução para aplicações especializadas;
- redução de acoplamento entre interface, regras, dados e IA.

### 18.2 Custos e limitações

- a Máquina Principal torna-se um ponto central de disponibilidade;
- a operação offline exige armazenamento e sincronização locais;
- a implantação local exige instalação, atualização e diagnóstico em várias máquinas;
- a coexistência de Central e estação administrativa precisa de isolamento de recursos;
- a evolução para nuvem exigirá nova especificação e trabalho de migração;
- contratos internos precisam ser estáveis desde cedo para evitar dependências diretas.

### 18.3 Riscos

- transformar a Central em um processo monolítico;
- permitir acesso direto dos Clientes ao banco;
- espalhar regras de negócio pela interface;
- acoplar o Mheibos a um único modelo de IA;
- tratar cache local como fonte da verdade;
- tentar implementar prematuramente a arquitetura futura em nuvem;
- permitir que integrações externas derrubem a aplicação principal.

---

## 19. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. existir separação executável ou lógica clara entre Central e Cliente;
2. a Central for a autoridade do estado global;
3. Clientes não acessarem diretamente a persistência central;
4. a Máquina Principal puder executar a Central sem depender da interface administrativa aberta;
5. o Gestor continuar utilizável sem interação obrigatória com a IA;
6. a indisponibilidade da IA não impedir operações essenciais determinísticas;
7. nenhuma operação essencial exigir IA e qualquer provedor futuro for acessado por camada substituível;
8. operações locais forem explicitamente limitadas quando a Central estiver indisponível;
9. futuras aplicações puderem consumir contratos da Central sem duplicar sua autoridade;
10. a implantação inicial não exigir serviços em nuvem para a operação básica;
11. responsabilidades pertencentes a outros RFCs não forem implementadas de forma contraditória;
12. falhas de um Cliente ou integração não derrubarem automaticamente toda a instalação.

---

## 20. Decisões adiadas

As seguintes decisões deverão ser tomadas em documentos posteriores ou na fase de implementação:

- linguagem e framework definitivos de cada serviço;
- banco de dados definitivo;
- protocolo de comunicação definitivo;
- formato dos contratos internos;
- empacotamento e atualização dos Clientes;
- estratégia de backup e restauração;
- criptografia e gerenciamento de segredos;
- modelo de linguagem inicial;
- requisitos mínimos de hardware;
- monitoramento técnico e interface de administração da Central;
- mecanismo de descoberta da Máquina Principal na rede.

Essas escolhas deverão respeitar as fronteiras e requisitos definidos nesta RFC.

---

## 21. Declaração normativa

A primeira versão do Mheibos será uma plataforma desktop distribuída e local, formada por uma Central executada na Máquina Principal e por Clientes instalados nas estações de trabalho.

A Central será a autoridade global. Os Clientes fornecerão a experiência operacional e autonomia local limitada. O Mheibos Gestor permanecerá utilizável por seus módulos, independentemente de interação direta com a IA. O modelo de IA será local, único na primeira versão e substituível por arquitetura.

A evolução para nuvem, múltiplas empresas, aplicações especializadas e múltiplos modelos será posterior e não deverá ampliar prematuramente o escopo da primeira implementação.

---

## 22. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-014 — versão inicial desktop e local | 4, 6 e 21 |
| INV-015 — Central e Clientes | 5, 6, 7 e 8 |
| INV-016 — Central como autoridade global | 7 e 12 |
| INV-017 — Máquina Principal também administrativa | 6.1 |
| INV-018 — indisponibilidade prevista | 11.3 e 14.1 |
| INV-019 — nuvem posterior | 4.2 e 16.1 |
| INV-020 — Gestor integrado | 9.1 |
| INV-021 — módulos como navegação principal | 9.3 |
| INV-022 — aplicações futuras subordinadas à Central | 12.6 e 16.2 |
| INV-023 — fundação opera com IA desligada | 10.9 e 13 |
