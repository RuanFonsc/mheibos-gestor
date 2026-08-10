# Mapa de Dependências da Série ENG

**Data:** 01/08/2026

```mermaid
flowchart TD
  R["Manifesto, Princípios, RFCs e Inventário"] --> E0["ENG-0000 Programa"]
  E0 --> E1["ENG-0001 Manifesto de Engenharia"]
  E0 --> E2["ENG-0002 Constituição dos Agentes"]
  E1 --> E2
  E2 --> E3["ENG-0003 Skill Oficial"]
  E0 --> E3
  E3 --> E4["ENG-0004 Development Protocol"]
  R --> E5["ENG-0005 Architecture Guide"]
  D["Diagnóstico Atual"] --> E6["ENG-0006 Implementation Guide"]
  R --> E6
  E4 --> E6
  E5 --> E6
  D --> E7["ENG-0007 Migration Strategy"]
  R --> E7
  E6 --> E7
  E0 --> E8["ENG-0008 Architectural Checklist"]
  E1 --> E8
  E2 --> E8
  E3 --> E8
  E4 --> E8
  E5 --> E8
  E6 --> E8
  E7 --> E8
  E4 --> E9["ENG-0009 Code Review Guide"]
  E8 --> E9
  R --> E10["ENG-0010 Glossário Oficial"]
  E0 --> E10
  E1 --> E10
  E2 --> E10
  E3 --> E10
  E4 --> E10
  E5 --> E10
  E6 --> E10
  E7 --> E10
  E8 --> E10
  E9 --> E10
```

## Dependências normativas externas

- ENG-0005 depende de RFCs e Inventário.
- ENG-0006 depende de RFCs e Diagnóstico.
- ENG-0007 depende de Diagnóstico e RFCs.
- ENG-0010 depende de todas as RFCs existentes.

## Dependências bloqueadas ou incompletas

- RFC-0015 está aprovada e RFC-0016 está recebida como Draft 0.1 em `docs/RFC-0016-Governanca-da-IA-Autonomia-e-Autoridade-Humana.md`; ambas permanecem fontes com escopo próprio e não tornam a IA obrigatória.
- RFC-0002 e RFC-0003 a RFC-0011/RFC-0013 aguardam aprovação explícita conforme seus próprios metadados.
- A numeração da RFC-0012 foi corrigida; seu conteúdo normativo detalhado ainda precisa ser elaborado.
- O baseline executa Ruff e mypy por `tools/quality.ps1`.
- A descoberta padrão do Django encontra e executa quatro testes de caracterização do domínio de pedidos.

Essas lacunas propagam `COMPLETED_WITH_GAPS`, sem invalidar as responsabilidades procedurais dos ENGs.
