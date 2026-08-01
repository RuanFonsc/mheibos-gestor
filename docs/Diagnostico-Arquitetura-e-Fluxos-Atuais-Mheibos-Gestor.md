# MHEIBOS INTELLIGENT OPERATING SYSTEM

# Diagnóstico da Arquitetura e dos Fluxos Atuais do Mheibos Gestor

**Status:** Documento de Diagnóstico  
**Versão:** 1.0  
**Data:** 31/07/2026  
**Objetivo:** Registrar o estado real do sistema existente antes da implementação da nova arquitetura definida pelos RFCs.

---

# 1. Finalidade

Este documento **não é um RFC**.

Seu objetivo é documentar, de forma técnica e honesta, como o Mheibos Gestor funciona atualmente, servindo como base para:

- comparação entre a arquitetura atual e a arquitetura futura;
- planejamento da migração;
- identificação de débitos técnicos;
- identificação de regras existentes que precisam ser preservadas;
- identificação de funcionalidades que deverão ser substituídas;
- auditoria da evolução do projeto.

Nenhuma decisão arquitetural deste documento possui caráter normativo.

Os documentos normativos do projeto continuam sendo os RFCs oficiais.

---

# 2. Situação Geral

O sistema atual é um software desktop baseado em:

- Django 5
- Templates Server Side
- PostgreSQL (ou SQLite por configuração)
- Electron como launcher desktop

A arquitetura atual cresceu de forma incremental durante vários anos.

Como consequência, existem diversas regras de negócio implementadas diretamente em Views, Services e Forms, sem uma separação clara entre:

- domínio;
- aplicação;
- interface;
- persistência.

Apesar disso, o sistema já resolve uma parte importante da operação da empresa.

---

# 3. Componentes atuais

O sistema é composto principalmente pelos módulos:

- Clientes
- Pedidos
- Catálogo
- Financeiro
- Vendas
- Aprendizado
- Migração
- Electron

O módulo de Pedidos concentra a maior parte das regras operacionais.

---

# 4. Modelo operacional atual

Hoje praticamente toda a empresa gira em torno da entidade Pedido.

O Pedido acaba acumulando responsabilidades que pertencem a conceitos diferentes, como:

- orçamento;
- venda;
- produção;
- aprovação;
- financeiro;
- entrega.

Essa centralização simplificou o desenvolvimento inicial, porém tornou difícil representar corretamente o fluxo real da empresa.

---

# 5. Fluxos existentes

O levantamento identificou os seguintes fluxos reais implementados:

- cadastro de clientes;
- criação automática de clientes;
- criação de pedidos;
- edição de pedidos;
- controle de itens;
- upload de artes;
- pagamentos;
- produção;
- assistência de envio;
- entrega;
- financeiro;
- aprendizado.

Esses fluxos existem, porém muitos deles dependem apenas da troca de Status do Pedido.

---

# 6. Principais limitações

O diagnóstico identificou diversos problemas estruturais.

Entre eles:

- ausência de entidade Orçamento;
- ausência de entidade Fechamento;
- ausência de Processo independente;
- ausência de Etapas;
- ausência de máquina formal de estados;
- ausência de auditoria central;
- ausência de workflow engine;
- regras espalhadas entre diversos módulos;
- sincronização financeira dependente de chamadas manuais;
- duplicação de lógica de criação de pedidos;
- estados que podem ser ignorados;
- produção sem aprovação formal;
- entrega sem evidência;
- histórico parcial;
- múltiplas fontes de verdade para alguns dados.

---

# 7. Estado dos módulos

## Clientes

Funciona adequadamente para cadastro simples.

Problemas encontrados:

- deduplicação baseada apenas no nome;
- clientes criados automaticamente ficam invisíveis no CRM;
- ausência de identidade forte baseada em telefone ou documento.

## Pedidos

É o núcleo operacional do sistema.

Problemas encontrados:

- excesso de responsabilidades;
- múltiplos caminhos para alterar status;
- criação duplicada entre Gestor e Vendas;
- cálculo de valores dentro das Views;
- ausência de camada de domínio.

## Catálogo

Além do catálogo de produtos, concentra funcionalidades que não pertencem ao mesmo contexto.

## Financeiro

Já possui boa estrutura, porém depende de sincronização manual e possui duplicidades conceituais.

## Vendas

Duplica parte significativa da lógica existente no módulo de Pedidos.

## Aprendizado

Hoje funciona apenas como coleta de dados.

---

# 8. Máquinas de estado atuais

Existem máquinas de estado implícitas para:

- Pedido
- Pagamento
- Financeiro
- Cliente
- Aprendizado

As transições normalmente são feitas alterando diretamente um campo de Status.

---

# 9. Principais débitos técnicos

- lógica distribuída entre Views;
- regras espalhadas entre módulos;
- ausência de eventos;
- ausência de evidências;
- ausência de auditoria consistente;
- ausência de separação entre domínio e interface;
- duplicação de informações;
- forte acoplamento entre interface e regras de negócio.

---

# 10. Objetivo da nova arquitetura

A nova arquitetura pretende introduzir:

- Processos
- Fluxos
- Etapas
- Eventos
- Evidências
- Auditoria
- Estados independentes
- Interface Viva
- Missões
- Conhecimento estruturado
- Sincronização offline robusta

---

# 11. Estratégia de migração

A migração deverá ocorrer de forma incremental, preservando dados, compatibilidade e continuidade operacional.

---

# 12. Considerações finais

Este documento representa uma fotografia técnica do estado atual do Mheibos Gestor antes da adoção completa da nova arquitetura.
