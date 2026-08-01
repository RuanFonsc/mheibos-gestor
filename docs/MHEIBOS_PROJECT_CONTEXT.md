# Contexto do Projeto Mheibos (Fonte para IA)

Este documento resume decisões arquiteturais já tomadas e deve ser utilizado como contexto base em novas conversas.

## Visão

O Mheibos não é um ERP tradicional.

É um Sistema Operacional Empresarial que acompanha a operação da empresa através de Processos Operacionais.

## Ideias Fundamentais

- O usuário trabalha; o Mheibos observa.
- O sistema deve depender de evidências e não de atualização manual de status.
- A IA nunca é a fonte oficial da verdade.
- O Motor de Regras é determinístico.
- A IA interpreta, explica e sugere.

## Conceitos Principais

- Processo Operacional
- Objetivo
- Fluxo
- Estado Operacional
- Evidência Operacional
- Observação Passiva
- Motor de Evidências
- Motor de Regras
- Intervenção Operacional
- Memória Operacional

## Decisões importantes

- A empresa é modelada por processos, não por módulos.
- Desktop Agent observa programas, arquivos e servidor.
- Arquivos fazem parte do contexto operacional.
- Validações técnicas devem ser determinísticas.
- A arquitetura será dividida em RFCs independentes.

## RFCs previstas

- RFC-0000 Manifesto
- RFC-0001 Princípios Fundamentais
- RFC-0002 Modelo Operacional
- RFC-0003 Arquitetura Técnica
- RFC-0004 Arquitetura Cognitiva
- RFC-0005 Modelo de Dados

## Observação

Este documento é apenas um resumo para acelerar o entendimento do projeto. As RFCs são sempre a fonte oficial das decisões arquiteturais.
