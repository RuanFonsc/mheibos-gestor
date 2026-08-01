# ENG-0005 — Architecture Guide

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** orientar a interpretação conjunta, o roteamento e as fronteiras das RFCs do Mheibos.  
**Dependências:** RFCs e Inventário Oficial.

---

## 1. Como interpretar

Começar pelo Manifesto e Princípios, localizar a RFC proprietária no Inventário e consultar RFCs relacionadas apenas nas fronteiras necessárias. Não compor arquitetura por soma indiscriminada de trechos.

Cada decisão possui um proprietário. Uma RFC relacionada pode impor contrato ou invariante, mas não assume a regra especializada.

## 2. Mapa de propriedade

| Fonte | Propriedade |
|---|---|
| RFC-0000 | propósito, memória operacional, atenção |
| RFC-0001 | princípios permanentes |
| RFC-0002 | modelo operacional conceitual |
| RFC-0003 | plataforma, Central, Clientes e fronteiras técnicas |
| RFC-0004 | arquitetura cognitiva e limites da IA |
| RFC-0005 | representação de dados e invariantes estruturais |
| RFC-0006 | eventos, evidências, auditoria e histórico |
| RFC-0007 | identidade, perfis, permissões e segurança |
| RFC-0008 | offline e sincronização |
| RFC-0009 | Interface Viva e intervenções |
| RFC-0010 | Missões e Teamwork |
| RFC-0011 | conhecimento, memória e aprendizado |
| RFC-0012 | Pendências, Lembretes e Escalonamento; reservada, aguardando elaboração |
| RFC-0013 | comercial, financeiro, metas e pedidos |
| RFC-0014 | arquivos, WhatsApp e integrações |
| RFC-0015 | prevista para analytics/simulação; ausente |
| RFC-0016 | prevista para governança/segurança da IA; ausente |

## 3. Plataforma

RFC-0003 define primeira versão desktop e local:

- Central na Máquina Principal como autoridade global;
- múltiplos Clientes Mheibos com autonomia local limitada;
- Cliente não acessa banco central diretamente;
- Gestor como aplicação principal integrada;
- contratos estáveis para aplicações especializadas futuras;
- Gateway de IA substituível;
- falha da IA ou integração não derruba funções essenciais.

Nuvem, multitenancy, aplicativo móvel e múltiplos modelos são evolução futura, não escopo inicial implícito.

## 4. Domínio e dados

RFC-0002 fornece Processo, Objetivo, Fluxo, Estado e Evidência. RFC-0005 estrutura:

- identidades técnicas estáveis;
- Pedido distinto de Processo;
- Modelo de Fluxo distinto de Fluxo Instanciado;
- Etapa com estado próprio;
- autoria, responsabilidade e conclusão separadas;
- estados comercial, operacional, financeiro e entrega independentes;
- pagamentos preservados;
- configuração organizacional distinta de preferência;
- estado global distinto de local/temporário;
- exclusão lógica como padrão.

Decisão física de banco, índices ou normalização não pode alterar essas invariantes.

## 5. Eventos e auditoria

RFC-0006 distingue Evento, Evidência, Auditoria, Comando, Notificação e Log Técnico.

Mudanças relevantes produzem eventos com identidade, origem, alvo, momento, mudança, contexto e resultado. Ação mediada pela IA distingue sugestão, autorização humana, validação e operação oficial.

Auditoria é imutável por correção aditiva; exclusão não destrói passado. Offline preserva origem, sequência e idempotência. Event sourcing não é imposto.

## 6. Identidade e segurança

RFC-0007 mantém identidade Mheibos independente do Windows, um perfil principal por usuário e exceções explícitas. Autorização considera ação, recurso, registro, propriedade, responsabilidade, contexto e alcance.

Ocultar interface não autoriza nem nega. Ações sensíveis exigem proteção, motivo e auditoria conforme política. IA e identidades técnicas não recebem privilégios ocultos.

## 7. Offline

RFC-0008 define offline restrito, visível e recuperável:

- regras previamente autorizadas;
- credencial protegida;
- operações locais preservadas;
- IDs e origem estáveis;
- reenvio idempotente;
- conflitos explícitos;
- incorporação pela Central;
- nenhuma ampliação de privilégio;
- nenhuma sincronização geral simplificada.

## 8. Interface

RFC-0009 mantém navegação normal utilizável sem chat. Interface Viva adapta temporariamente apresentação por comandos estruturados e autorizados.

Intervenção usa a menor interrupção eficaz, proporcional a gravidade, urgência e confiança. Deve explicar mudança e restauração. Cor, brilho ou animação não são o único canal crítico. Adaptação temporária não vira preferência persistente silenciosamente.

## 9. IA, conhecimento e memória

RFC-0004 define um único Mheibos cognitivo, contextual e subordinado aos dados oficiais. Sugestão precede imposição. Recomendações relevantes são explicáveis. Investigação ampla opcional pede consentimento.

RFC-0011 mantém conhecimento fora do modelo, em camadas com autoridade, proveniência, vigência e permissão. Memória curta não é automaticamente promovida a longa. Ensinamento começa pendente; IA avalia, humano autorizado aprova.

## 10. Operação colaborativa

RFC-0010 define Missão como workspace persistente com objetivo, plano, tarefas, participantes, dependências, progresso, conversas, notas e decisões.

Teamwork depende de aceite ou autoridade formal. IA não impõe colaboração, transfere responsabilidade ou julga pessoas. Missão referencia processos; não os duplica.

## 11. Comercial, financeiro e integrações

RFC-0013 preserva autoria comercial, pagamentos, saldo e estados independentes. Cancelamentos são auditáveis; entrega com saldo exige autorização e cria pendência conforme regra.

RFC-0014 mantém arquivos físicos fora do banco de uso diário, armazenando referências e contexto. Excluir vínculo não apaga arquivo. WhatsApp de cliente comercial pode receber assistência controlada; fornecedor terceirizado permanece em registro humano explícito conforme regra oficial.

## 12. Matriz de leitura por mudança

| Mudança | Proprietária | Relacionadas mínimas |
|---|---|---|
| Pedido/Processo/Etapa | 0005 | 0002, 0006, 0007, 0013 |
| permissão | 0007 | 0005, 0006 |
| evento/auditoria | 0006 | RFC da entidade, 0007 |
| offline | 0008 | 0003, 0005, 0006, 0007 |
| interface/intervenção | 0009 | RFC da regra, 0004, 0007 |
| IA | 0004 | 0007, 0011 e RFC da operação |
| conhecimento | 0011 | 0004, 0006, 0007 |
| missão | 0010 | 0005, 0006, 0007 |
| financeiro | 0013 | 0005, 0006, 0007 |
| arquivos/WhatsApp | 0014 | 0003, 0006, 0007 |

## 13. Resolução de divergências

1. Confirmar que as fontes tratam da mesma decisão e escopo.
2. Aplicar hierarquia e propriedade.
3. Distinguir norma de diagnóstico.
4. Verificar versão e status.
5. Se duas fontes normativas permanecerem incompatíveis, registrar conflito.
6. Não alterar código nem documento afetado até decisão.

## 14. Decisões adiadas

Se uma RFC declarar decisão adiada, implementação pode escolher detalhe técnico somente quando:

- a escolha não cria regra de produto;
- respeita invariantes;
- é reversível ou registrada em ADR;
- possui testes;
- não fecha opção arquitetural sem decisão formal.

## 15. Lacunas

- GAP-ENG-0000-001: RFC-0015/0016 ausentes.
- GAP-ENG-0000-002: drafts não formalmente aprovados.
- GAP-ENG-0000-003: RFC-0012 reservada e ainda não elaborada.
- GAP-ENG-0005-001: Inventário prevê RFC-0012 está corretamente reservada para Pendências, mas suas políticas detalhadas ainda aguardam elaboração.

## 16. Relatório de validação

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
| Testes | APROVADO — roteamento e referências verificáveis |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
