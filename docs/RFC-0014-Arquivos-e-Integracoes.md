# RFC-0014 --- Arquivos e Integrações

**Status:** Aprovado

## Objetivo

Definir a política oficial do Mheibos para gerenciamento de arquivos e
integrações externas, estabelecendo claramente quais arquivos pertencem
ao domínio do sistema e quais permanecem sob responsabilidade do sistema
operacional e dos softwares especializados.

## Princípios Fundamentais

-   O Mheibos **não é um gerenciador de arquivos**.
-   O banco de dados nunca armazenará arquivos binários de uso diário.
-   O sistema administra apenas os **vínculos, metadados e integridade
    operacional**.
-   O armazenamento físico permanece no computador, servidor local ou
    destinos configurados pela empresa.

## Arquivos Oficiais de Arte

-   Ao iniciar a etapa de arte, o Mheibos cria automaticamente o arquivo
    no programa escolhido pelo usuário.
-   O usuário pode definir um programa padrão em suas preferências ou
    escolher a cada criação.
-   O arquivo é criado vazio, utilizando as configurações padrão do
    software gráfico.
-   O nome oficial é gerado automaticamente.
-   A estrutura de diretórios é organizada por Ano/Mês/Dia.

Exemplo:

    Artes/
    └── 2026/
        └── 08 - Agosto/
            └── 15/
                └── #340 - Caneca Porcelana - Dia dos Pais.cdr

## Integridade dos Arquivos

-   O nome e a localização oficial fazem parte da identidade do arquivo.
-   Após o primeiro salvamento, o nome não pode ser alterado.
-   Alterações manuais de nome ou localização geram erro crítico.
-   O usuário pode acrescentar sufixos apenas durante a criação,
    preservando a estrutura oficial.

## Múltiplos Arquivos

-   Um pedido pode possuir diversos arquivos oficiais.
-   O usuário pode criá-los pelo Mheibos ou manualmente e vinculá-los
    depois.
-   Arquivos criados fora do fluxo só passam a existir para o sistema
    quando forem vinculados explicitamente.

## Monitoramento

O Mheibos monitora:

-   existência;
-   nome;
-   localização;
-   propriedades técnicas disponíveis;
-   dimensões;
-   proporção;
-   resolução, quando possível.

Discrepâncias geram alertas com explicação do problema e exigem
confirmação consciente do usuário ("Eu entendi"), registrando auditoria.

## Arte de Referência

A imagem utilizada na Ordem de Produção:

-   é anexada manualmente (Ctrl+V, arrastar e soltar ou explorador);
-   serve apenas como referência visual;
-   não é sincronizada automaticamente com a arte oficial.

## Arquivos Anexados

O Mheibos não interpreta arquivos anexados ao pedido.

Ele não:

-   descriptografa;
-   solicita senhas;
-   analisa conteúdo.

Os anexos permanecem em lista única e podem ser adicionados por:

-   Ctrl+V;
-   Drag & Drop;
-   Explorador de Arquivos.

Duplicidades são detectadas e o usuário decide se deseja manter ambas.

Excluir um anexo remove apenas o vínculo, nunca o arquivo físico.

## Pesquisa

As artes podem ser localizadas por:

-   número do pedido;
-   cliente;
-   telefone;
-   produto;
-   tema;
-   descrição;
-   nome do arquivo;
-   metadados.

O campo **Tema** pertence ao pedido.

Após o início da etapa de arte ou o primeiro pagamento, o tema torna-se
imutável.

## Backups

O sistema permite configurar:

-   Google Drive;
-   OneDrive;
-   NAS;
-   Servidores;
-   outros provedores.

O backup contempla apenas os arquivos oficiais de arte vinculados aos
pedidos.

## Revisão Anual

Os vínculos físicos não são permanentes.

O administrador realiza uma Revisão Anual, podendo:

-   encerrar vínculos;
-   arquivar períodos;
-   manter anos ativos;
-   executar backup previamente.

Após o encerramento permanecem:

-   histórico;
-   auditoria;
-   metadados;
-   nome do arquivo;
-   informações técnicas.

## PDFs

Documentos como Ordens de Produção e relatórios são regenerados sob
demanda a partir do banco de dados, não sendo armazenados
permanentemente como regra.

## Cancelamento

Cancelar um pedido não altera os arquivos de arte.

Eles permanecem preservados para histórico e reaproveitamento.

## Filosofia Final

O Mheibos administra apenas os arquivos que fazem parte do fluxo
operacional.

Todo o restante continua sendo responsabilidade do Windows, do sistema
de arquivos e dos softwares especializados.

Essa separação mantém o sistema leve, previsível, auditável e escalável.
