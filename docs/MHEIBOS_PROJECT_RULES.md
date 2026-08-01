# Regras do Projeto Mheibos

## Objetivo

Este documento define as regras operacionais que o ChatGPT deve seguir durante o desenvolvimento do projeto Mheibos.

Enquanto estivermos trabalhando neste projeto, estas regras devem ser consideradas antes das demais preferências de colaboração, respeitando sempre as limitações e políticas da plataforma.

---

## Regra 001 — Documentação oficial

Todo arquivo Markdown (`.md`) criado para o projeto deve passar a integrar a documentação oficial e as fontes de referência do Mheibos.

### Aplicação

- Todo novo documento deve ser considerado nas análises futuras do projeto.
- O conteúdo poderá ser utilizado como referência conceitual, técnica ou arquitetural.
- Um novo documento não deve contradizer documentos anteriores sem revisão explícita.
- Quando um novo documento alterar conceitos existentes, os documentos afetados devem ser identificados e atualizados.
- Sempre que um arquivo `.md` for criado, ele deve ser entregue como arquivo real, e não apenas exibido como texto na conversa.
- Quando a plataforma não permitir inserir automaticamente o arquivo na base de fontes pesquisáveis, essa limitação deve ser informada claramente ao usuário.

**Status:** Ativa  
**Versão:** 1.1

---

## Regra 002 — IA obrigatória, implementada por último

A IA é parte obrigatória da arquitetura final do Mheibos e suas funções previstas devem existir no desenho, nos contratos, nos dados e nos fluxos do sistema. A implementação e instalação do modelo de IA, local ou via API, ocorrerá somente na última fase, depois da fundação determinística.

### Aplicação

- Nenhum processo operacional pode parar, bloquear, ser adiado ou degradado porque a IA ainda não foi instalada ou está desligada.
- A ausência de IA não pode travar outras fases do desenvolvimento.
- As fases anteriores devem preparar contratos e pontos de extensão das funções cognitivas, sem acoplar o produto a um provedor.
- Enquanto a IA estiver desligada, a função deve usar execução determinística, permitir decisão humana ou omitir somente a assistência cognitiva opcional.
- Se uma lacuna lógica for realmente incontornável e não houver solução normativa, determinística ou humana sem inventar regra, interromper somente a parte afetada, registrar fontes e alternativas como `DECISAO_HUMANA_NECESSARIA` e perguntar ao responsável humano como proceder.
- A lacuna não autoriza instalar antecipadamente uma IA, inventar regra de negócio ou bloquear partes independentes.

**Status:** Ativa  
**Versão:** 1.0

---

## Manutenção das regras

Este é o arquivo oficial e único das regras de colaboração do projeto.

Quando uma nova regra for definida:

1. Ela deverá ser adicionada neste mesmo arquivo.
2. A numeração deverá seguir a sequência existente.
3. A versão do documento deverá ser atualizada.
4. A data de atualização deverá ser registrada.
5. O arquivo atualizado deverá substituir a versão anterior nas fontes do projeto.

---

**Última atualização:** 1º de agosto de 2026
