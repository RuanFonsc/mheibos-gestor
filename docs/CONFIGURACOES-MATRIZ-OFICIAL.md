# Matriz Oficial de Configurações do Mheibos

**Status:** aprovada para implementação incremental  
**Data:** 10/08/2026  
**Escopo:** organização da janela Configurações; não altera regras normativas das RFCs.

## 1. Regras de escopo

- Preferência individual pertence ao usuário e não altera regra de negócio.
- Configuração empresarial é persistente, auditável e somente pode ser alterada por autoridade autorizada.
- Cadastro e manutenção de usuários pertencem exclusivamente à página **Usuários**, nunca ao Perfil.
- A IA pode estar desligada; nenhuma configuração normal depende dela.
- Itens ainda não definidos normativamente aparecem como estado informativo ou pendente, sem valores inventados.
- A arte oficial só é criada ou vinculada pela interface do Mheibos. Nome, extensão, estrutura Ano/Mês/Dia e forma de exibição do caminho são decisões do sistema.

## 2. Hierarquia oficial

### 2.1 Perfil do usuário

**Editável pelo próprio usuário:** nome de exibição, foto, senha, programa/formato padrão de arte oficial (CorelDRAW, Illustrator, Photoshop, Inkscape, GIMP, Affinity Designer, Affinity Photo e PDF), tema, zoom, densidade, nível inicial de detalhes, dicas não críticas, redução de movimento, intensidade de animação, layouts pessoais e preferências pessoais de notificações/Assistência de Impressão.

**Somente leitura:** papel, categoria, canal padrão, estação, estado online/offline, permissões efetivas, estado da IA e memórias/preferências aprendidas quando disponíveis.

### 2.2 Perfil da Empresa

**Editável por administrador:** identidade e contatos, logo, raiz compartilhada das artes, retenção de cópias locais, modelo e campos da Ordem de Serviço, categorias de serviço, prazos e alertas por categoria, políticas comerciais aprovadas, destinos de backup e regras de arquivamento quando os contratos estiverem implementados.

**Somente leitura/pendente:** validação da pasta compartilhada, estado da Central, estado da sincronização e parâmetros ainda não detalhados pela RFC-0012.

### 2.3 Aparência

Área exclusiva para opções visuais permitidas: tema, zoom, densidade, redução de movimento, intensidade de animação, nível de detalhes, contraste/legibilidade e layouts pessoais. Nenhuma opção pode esconder informação obrigatória ou substituir autorização.

### 2.4 Operação e Alertas

Preferências individuais de frequência, duração, posição e categorias acompanhadas; políticas empresariais de prazos, criticidade, responsáveis, alertas e escalonamento determinístico. Os valores temporais da RFC-0012 permanecem `DECISAO_HUMANA_NECESSARIA` até sua aprovação.

### 2.5 Segurança

Perfil do usuário permite alterar a própria senha. Administradores autorizados poderão configurar política de ações sensíveis, justificativa, reautenticação, bloqueios e tentativas quando os parâmetros de implementação forem definidos. Permissões efetivas e sessão são informativas.

### 2.6 Offline e Sincronização

Estado da Central, estação, última sincronização, fila local, operações pendentes e bloqueio de logout são informativos. Destino e retenção locais só poderão ser configurados dentro dos limites da RFC-0008.

### 2.7 Dashboard e Analytics

Preferências pessoais de indicadores, ordem, filtros, nível de detalhes e layout. Metas e indicadores globais permanecem configurações empresariais sujeitas à permissão. Premissas de simulação não viram preferência automaticamente.

### 2.8 IA e Autonomia

Enquanto o Modelo de Decisões Autônomas da IA não estiver aprovado, esta área exibe apenas estado da IA, Gateway, modelo e funções disponíveis. Categorias de autonomia, teto, janelas, limites computacionais e operação desacompanhada ficam documentados como futuros e não são editáveis.

## 3. Fora da janela Configurações

- Cadastro, edição, ativação, desativação e categorias de usuários: página **Usuários**.
- Nome, extensão, diretório Ano/Mês/Dia e vínculo da arte oficial: fluxo próprio de criação/vinculação.
- Regras de produção, conclusão de arte, bloqueios, autorizações gerenciais, auditoria e invariantes de segurança.

## 4. Diretriz visual da página

A tela deve usar navegação por áreas, grupos recolhíveis, formulários curtos, indicação explícita de editável/somente leitura/pendente, ações próximas ao grupo alterado e layout responsivo em 100% e 125% de zoom. Não usar cards gigantes nem misturar preferência pessoal com política empresarial.

## 5. Fontes

RFC-0003, RFC-0005, RFC-0007, RFC-0008, RFC-0009, RFC-0012, RFC-0013, RFC-0014, RFC-0015, RFC-0016, `UI-STANDARDS-MHEIBOS.md`, `VISUAL-QUALITY-GATE-MHEIBOS.md` e `IMPLEMENTATION-DECISIONS.md`.
