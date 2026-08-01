# ENG-0001 — Manifesto de Engenharia do Mheibos

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** declarar a filosofia permanente da prática de engenharia do Mheibos.  
**Dependência:** ENG-0000.

---

## 1. Engenharia a serviço da atenção

O Mheibos existe para assumir a responsabilidade de lembrar, acompanhar e tornar visível o que exige decisão. Sua engenharia deve servir ao mesmo propósito.

Código, arquitetura, testes e documentação não são fins isolados. São meios para construir uma memória operacional confiável, preservar a atenção humana e permitir que pessoas se concentrem no trabalho que exige julgamento.

Uma mudança tecnicamente sofisticada que aumenta ambiguidade, dependência de memória ou fragilidade operacional não é boa engenharia para o Mheibos.

## 2. A realidade antes da interface

O sistema representa a operação real. Telas, módulos e aplicativos são projeções dessa realidade, não suas autoridades.

Pedido não substitui Processo. Processo não substitui Etapa. Estado não substitui Evento. Evento não substitui Evidência. Um status genérico não comprime dimensões comerciais, operacionais, financeiras e de entrega.

Engenharia começa pela entidade, pelo objetivo, pelo fluxo, pela responsabilidade e pelos critérios de conclusão. A interface vem depois, como meio de interação compreensível e autorizado.

## 3. A norma antes do legado

RFCs definem o que deve existir. Código e diagnóstico revelam o que existe. O trabalho de engenharia transforma um no outro com migração consciente.

O legado contém valor, dados e conhecimento operacional. Ele deve ser compreendido e preservado quando legítimo, mas não copiado como arquitetura futura. Compatibilidade é uma ponte com plano de remoção, não uma moradia permanente.

## 4. Determinismo antes da cognição

Permissão, autenticação, transição obrigatória, cálculo oficial, integridade e persistência pertencem a mecanismos determinísticos.

A IA pode interpretar contexto, explicar fatos, sugerir alternativas, planejar e acompanhar. Ela não cria verdade, não concede autoridade e não substitui regra ausente. Toda saída cognitiva relevante deve poder ser validada, explicada e recusada.

Falha da IA não pode impedir operações determinísticas essenciais.

## 5. Domínio antes da apresentação

Toda capacidade operacional deve nascer em regras e casos de uso explícitos. A sequência preferencial é:

1. identificar entidade e invariante;
2. aplicar autorização e regra determinística;
3. persistir com integridade;
4. produzir evento e auditoria;
5. expor contrato estável;
6. apresentar na interface.

Ocultar botão não nega permissão. JavaScript, template, formulário ou view não se tornam autoridade por conveniência.

## 6. Histórico antes da conveniência

O Mheibos é memória operacional. Apagar silenciosamente contradiz seu produto.

Alterações relevantes preservam autoria, origem, momento, contexto e consequência. Cancelamento, desativação, arquivamento e substituição são estados diferentes. Exclusão física é excepcional e subordinada a política, autorização e rastreabilidade.

Estado atual e histórico são representações distintas e complementares.

## 7. Fatias verificáveis antes de grandes reescritas

A evolução ocorre em incrementos pequenos, coerentes e testáveis. Cada fatia deve:

- possuir objetivo e classificação;
- manter integridade dos dados;
- produzir comportamento observável;
- incluir testes proporcionais ao risco;
- permitir diagnóstico e recuperação;
- atualizar documentação;
- declarar o que ainda não foi resolvido.

Reescritas amplas exigem justificativa arquitetural e plano de migração. Abstração especulativa não substitui necessidade real.

## 8. Contratos antes do acoplamento

A Central mantém autoridade global. Clientes Mheibos, interfaces especializadas e integrações usam contratos explícitos.

Nenhum Cliente acessa diretamente o banco central. Nenhum modelo acessa diretamente banco ou widgets. Nenhuma integração externa derruba o sistema inteiro. Fronteiras entre Domínio, Aplicação, Infraestrutura e Interface devem ser visíveis no código e nos testes.

## 9. Evidência antes da suposição

Estados e intervenções importantes devem derivar de fatos verificáveis, eventos e regras. Hipótese deve ser identificada como hipótese. Recomendação deve apresentar fundamentos, incerteza e impacto.

Quando uma fonte faltar ou divergir, a engenharia registra a lacuna. Terminar rápido nunca justifica transformar inferência em arquitetura.

## 10. Segurança antes da facilidade

Autoridade é validada antes da persistência. Identidades são próprias, permissões respeitam ação, recurso, registro, responsabilidade e contexto. Ações sensíveis recebem proteção e auditoria proporcionais.

A IA herda permissões do usuário. Offline não amplia privilégios. Cache local não se torna verdade global.

## 11. Continuidade antes do cenário ideal

Falhas são parte do sistema:

- Central temporariamente indisponível;
- Cliente interrompido;
- integração externa falhando;
- IA indisponível;
- evento secundário não processado;
- operação offline reenviada.

Engenharia prevê idempotência, recuperação, visibilidade, compensação e limites claros. Falha secundária não apaga o fato principal.

## 12. Clareza antes do volume

Documentação possui responsabilidade exclusiva. Um documento deve responder claramente às perguntas que lhe pertencem e referenciar o proprietário das demais.

Código legível, nomes não ambíguos, testes próximos às regras e relatórios verificáveis valem mais que volume. “Cliente”, “status” e “arquivo” devem ser qualificados quando puderem representar conceitos distintos.

## 13. Dignidade antes da otimização

O Mheibos auxilia pessoas e processos; não humilha, rotula ou diagnostica indivíduos. Métricas existem para coordenação e melhoria, não exposição depreciativa.

Intervenções usam a menor interrupção eficaz. Recomendações preservam decisão humana. Colaboração depende de aceite ou autoridade formal.

## 14. Aprendizado governado

Conhecimento permanece fora do modelo de linguagem, com origem, escopo, vigência e validação. Prática emergente não se torna regra por repetição ou conveniência.

O sistema aprende com acertos, erros e improvisações sem promover automaticamente observação a conhecimento oficial. Trocar o modelo não apaga a memória da empresa.

## 15. O compromisso do engenheiro

Quem altera o Mheibos compromete-se a:

- localizar a fonte normativa antes de editar;
- distinguir presente e futuro;
- planejar antes de implementar;
- preservar dados e história;
- testar riscos relevantes;
- revisar segurança, eventos e auditoria;
- registrar conflitos e lacunas;
- parar quando faltar decisão;
- entregar evidências verificáveis.

## 16. Lacunas herdadas

Este Manifesto não resolve as lacunas GAP-ENG-0000-001, GAP-ENG-0000-002 e GAP-ENG-0000-003. Temas dependentes das RFC-0015/RFC-0016, de aprovação dos drafts ou do roteamento da RFC-0012 permanecem sujeitos a decisão humana.

## 17. Relatório de validação

| Gate | Resultado | Evidência |
|---|---|---|
| Fonte Normativa | APROVADO COM LACUNAS | RFC-0000, RFC-0001 e ENG-0000 |
| Arquitetura | APROVADO | somente princípios já normativos |
| Domínio | APROVADO | domínio precede interface |
| Dados | APROVADO | preservação e histórico declarados |
| Eventos/Auditoria | APROVADO | rastreabilidade é princípio |
| Segurança | APROVADO | autoridade determinística |
| IA | APROVADO | cognição subordinada à verdade |
| UX | APROVADO | atenção e dignidade preservadas |
| Código | NÃO APLICÁVEL | documento filosófico |
| Testes | APROVADO | referências, estrutura e dependência verificadas |
| Documentação | APROVADO | responsabilidade exclusiva explícita |
| Revisão Final | APROVADO COM LACUNAS | lacunas herdadas preservadas |

**Resultado:** `COMPLETED_WITH_GAPS`.

## 18. Declaração final

O melhor resultado de engenharia não é o maior código nem o documento mais extenso. É uma evolução que representa corretamente a realidade, reduz carga cognitiva, preserva autoridade humana, protege a memória operacional e pode ser verificada.

Enquanto as pessoas constroem o trabalho, a engenharia do Mheibos constrói a confiança que permite ao sistema lembrar.
