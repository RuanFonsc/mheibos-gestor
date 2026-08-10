# ENG — Migração futura do Cliente para Tauri 2 + React + TypeScript

**Status:** FUTURA — não faz parte da fila ativa dos IMPs atuais  
**Fonte original:** `C:\Users\Ruan\Downloads\ENG-MIGRACAO-CLIENTE-TAURI2-REACT-TYPESCRIPT.md`  
**Central vigente:** Django  
**Cliente vigente:** Electron + templates Django  

## Regra de prioridade

Este ENG deve ser lido por qualquer agente que trabalhe no cliente desktop, mas **não autoriza iniciar a migração agora**. A prioridade atual continua sendo concluir IMP-010, IMP-011, IMP-012 e IMP-013 conforme suas fontes normativas.

A migração Tauri somente poderá entrar na execução depois que os contratos funcionais e de API necessários estiverem estabilizados e a fila ativa dos IMPs autorizar uma fatia de migração.

## Decisão arquitetural preservada

- Django permanece como autoridade global, domínio, casos de uso, autorização, eventos, auditoria, sincronização e persistência central.
- React/TypeScript será apenas a interface e a lógica visual do Cliente.
- Tauri/Rust será apenas a camada desktop/local restrita.
- SQLite local, filesystem e comandos do sistema operacional permanecem limitados às responsabilidades locais autorizadas.
- IA não será requisito para o cliente funcionar.
- React, Tauri e cache local não podem se tornar uma segunda fonte de verdade.

## Escopo futuro

Quando autorizada, a migração será incremental e reversível:

1. inventário do Electron e dos templates atuais;
2. formalização dos contratos Central–Cliente;
3. shell Tauri/React sem remover Electron;
4. migração por fatias verticais;
5. testes de equivalência, segurança, offline e auditoria;
6. remoção do Electron somente após todos os critérios de desativação serem aprovados.

Não fazer reescrita em bloco, não mover regras de negócio para React/Rust e não remover o cliente atual antes da equivalência funcional comprovada.

## Relação com os IMPs

Esta migração é uma trilha posterior de infraestrutura do Cliente. Ela não substitui nem reordena os IMPs de domínio:

- não bloqueia IMP-010;
- não bloqueia IMP-011;
- não bloqueia IMP-012;
- não bloqueia IMP-013;
- deve reutilizar as regras e contratos já validados nesses IMPs.

O Dashboard do IMP-012 deve ser concluído no cliente vigente antes de ser migrado para React, salvo decisão posterior expressa no plano de implementação.

## Critério para iniciar

A migração só entra na fila ativa quando houver:

- contratos de API estáveis;
- autenticação e autorização documentadas;
- modelo offline validado;
- fluxos de arquivos oficiais conhecidos;
- critérios visuais definidos;
- fatia inicial pequena e reversível;
- Quality Gates específicos aprovados.

O documento original completo permanece como referência de execução futura. Este registro é o ponto oficial de descoberta para impedir que um agente confunda a diretriz de migração com uma autorização para interromper a implementação atual.
