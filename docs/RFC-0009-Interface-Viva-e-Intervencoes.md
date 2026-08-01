# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0009 — Interface Viva e Intervenções

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-052 a INV-064

---

## 1. Resumo

Esta RFC define a **Interface Viva** do Mheibos: a forma pela qual a aplicação desktop pode adaptar temporariamente sua apresentação, conduzir a atenção do usuário, oferecer assistência contextual, destacar riscos e organizar ambientes focados de trabalho sem substituir a interface normal, alterar silenciosamente dados persistentes ou ultrapassar permissões.

A interface do Mheibos não será apenas uma superfície passiva de telas e formulários. Ela será também um meio controlado de comunicação entre o sistema e o usuário. Por meio de uma API interna, componentes autorizados poderão abrir e fechar janelas, navegar entre módulos, selecionar abas, focar campos, rolar listas, aplicar filtros, destacar elementos e montar contextos temporários de trabalho.

A IA não controlará diretamente componentes visuais nem executará código arbitrário na interface. Ela produzirá intenções estruturadas, que serão validadas pelo Mheibos e traduzidas pelo **Orquestrador de Interface** em ações previamente permitidas.

Adaptações temporárias poderão ocorrer automaticamente quando não alterarem dados, regras, permissões ou decisões persistentes. Alterações reais deverão começar como sugestão, explicar o impacto e depender da confirmação correspondente.

As intervenções possuirão níveis de criticidade. O padrão será uma comunicação flutuante não bloqueante. Situações relevantes poderão oferecer ações rápidas. Situações críticas poderão exigir reconhecimento ou uma ação mínima antes de liberar a apresentação crítica, com tratamento diferente para usuários comuns e administradores.

A personalização será individual. Usuários com o mesmo perfil poderão receber organização, filtros, atalhos e assistência diferentes, sem que isso modifique regras de negócio, autoridade ou acesso.

Objetivos declarados poderão gerar uma interface focada denominada **Missão**. A missão reunirá temporariamente módulos, listas, bloqueios e ações relevantes, poderá ser pausada e retomada e não substituirá a navegação normal do Mheibos.

Erros recorrentes deverão acionar assistência progressiva, preferencialmente antes que se tornem hábito. O sistema poderá iniciar treinamento guiado e adaptar a forma de apoio aos padrões de atenção do usuário, sem diagnosticar, rotular ou expor características pessoais.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- como a IA e outros componentes autorizados podem influenciar a interface;
- quais ações visuais a interface deverá expor por API interna;
- como impedir que o modelo de linguagem controle diretamente a aplicação;
- quais adaptações podem ocorrer automaticamente;
- quais mudanças exigem sugestão e confirmação;
- como diferenciar comentário, alerta, intervenção relevante e situação crítica;
- quando uma intervenção pode bloquear parcialmente a continuidade visual;
- como usuários comuns e administradores tratam situações críticas;
- como a interface pode ser personalizada individualmente;
- como objetivos geram ambientes temporários de trabalho;
- como missões podem ser pausadas e retomadas;
- como erros recorrentes acionam ajuda progressiva;
- como a assistência se adapta ao padrão de atenção sem criar diagnósticos;
- como tutoriais devem apresentar conteúdo de forma progressiva;
- como preservar acessibilidade, previsibilidade, controle humano e desempenho.

Esta RFC não define o layout visual definitivo, o design system, a biblioteca gráfica, os componentes PyQt6 concretos, o modelo de linguagem, o armazenamento completo das missões, as regras de criação de tarefas, o scheduler de notificações ou a governança da IA. Esses temas pertencem à implementação ou a RFCs especializados.

---

## 3. Decisões fundamentais

A arquitetura de Interface Viva e Intervenções adota as seguintes decisões:

1. A interface exporá uma API interna de ações visuais controladas.
2. A IA não manipulará diretamente widgets, janelas ou código da interface.
3. Toda intenção cognitiva será convertida em comando estruturado, validado e autorizado antes da execução visual.
4. A interface poderá abrir e fechar janelas, navegar, selecionar abas, focar campos, rolar listas, aplicar filtros e destacar elementos.
5. A interface será um meio legítimo de comunicação do Mheibos com o usuário.
6. Destaques visuais poderão incluir pulsação, brilho, foco, escurecimento do restante da tela e indicação do próximo passo.
7. Alterações persistentes começarão como sugestão e dependerão da confirmação aplicável.
8. Adaptações temporárias que não alterem dados reais poderão ocorrer localmente e de forma automática.
9. Intervenções possuirão níveis de criticidade e intensidade proporcional.
10. O padrão será um comentário flutuante não bloqueante.
11. Intervenções relevantes poderão apresentar ações rápidas.
12. Situações críticas poderão exigir reconhecimento ou uma ação mínima.
13. Usuários comuns somente removerão uma apresentação crítica depois de uma ação mínima válida.
14. Administradores poderão restaurar a interface crítica após reconhecimento, sem apagar a situação subjacente.
15. A personalização será individual e não modificará regras de negócio nem permissões.
16. Um objetivo poderá gerar uma interface focada temporária denominada Missão.
17. A missão não substituirá a interface normal e poderá ser pausada e retomada.
18. Erros recorrentes acionarão assistência progressiva, por padrão a partir da terceira ocorrência configurável.
19. A assistência deverá ser educada, gentil, preventiva e orientada à solução.
20. O sistema poderá adaptar o apoio ao padrão individual de atenção, sem diagnosticar, rotular ou expor condições pessoais.
21. Tutoriais apresentarão primeiro o caminho oficial essencial e revelarão conteúdo complementar progressivamente.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- Interface Viva;
- Orquestrador de Interface;
- API interna de ações visuais;
- catálogo conceitual de comandos de interface;
- validação e autorização de comandos;
- destaques e condução visual;
- adaptações temporárias;
- sugestões de alterações persistentes;
- níveis de intervenção;
- reconhecimento e ação mínima;
- comportamento de situações críticas;
- personalização individual;
- interface focada por objetivo;
- pausa e retomada de missões;
- assistência a erros recorrentes;
- treinamento guiado;
- divulgação progressiva de tutoriais;
- acessibilidade e redução de sobrecarga;
- registro técnico e auditoria das intervenções relevantes;
- recuperação segura da interface.

### 4.2 Fora do escopo

Não são definidos aqui:

- identidade visual definitiva;
- tipografia, cores, ícones e espaçamentos finais;
- biblioteca concreta de componentes;
- framework definitivo da interface;
- persistência completa de Missões e Teamwork;
- regras de tarefas e colaboração;
- scheduler de lembretes;
- canais externos de notificação;
- comportamento cognitivo completo da IA;
- algoritmo de detecção de erros recorrentes;
- modelo definitivo de personalização;
- telemetria comportamental detalhada;
- política legal de dados pessoais;
- acessibilidade normativa específica de uma plataforma;
- integração visual definitiva com WhatsApp;
- telas finais de cada módulo.

---

## 5. Conceitos fundamentais

### 5.1 Interface Viva

Interface Viva é a capacidade do Cliente Mheibos de adaptar temporariamente sua apresentação e conduzir a atenção do usuário com base em contexto, objetivo, risco, assistência ou intervenção autorizada.

Ela não significa que a interface possa alterar-se de forma imprevisível ou arbitrária. Toda adaptação deverá respeitar contratos, limites, reversibilidade e clareza.

### 5.2 Orquestrador de Interface

O Orquestrador de Interface é o componente do Cliente responsável por receber comandos estruturados e traduzi-los em ações visuais seguras.

Ele deverá impedir que a IA, integrações ou módulos externos manipulem diretamente widgets internos.

### 5.3 Comando de interface

Comando de interface é uma intenção estruturada equivalente a:

- abrir uma tela;
- fechar uma janela não crítica;
- selecionar uma aba;
- focar um campo;
- rolar até um elemento;
- aplicar um filtro temporário;
- destacar uma linha;
- escurecer áreas não relacionadas;
- apresentar uma intervenção;
- montar ou restaurar uma visão focada.

Um comando de interface não é, por si só, uma autorização para alterar dados persistentes.

### 5.4 Adaptação temporária

Adaptação temporária é uma mudança local na apresentação que não altera a realidade oficial da operação.

Exemplos:

- reorganizar uma lista;
- abrir uma tela relevante;
- aplicar um filtro;
- destacar pedidos em risco;
- esconder temporariamente informações sem relação com o objetivo atual;
- montar uma visão de missão.

### 5.5 Alteração persistente

Alteração persistente modifica dados, configurações, estados, responsáveis, mensagens, políticas, tarefas, decisões ou qualquer outra informação oficial.

Ela não poderá ser disfarçada como adaptação visual.

### 5.6 Intervenção

Intervenção é uma comunicação ativa do Mheibos que busca produzir reconhecimento, decisão ou ação do usuário diante de uma situação relevante.

### 5.7 Reconhecimento

Reconhecimento é a confirmação de que o usuário percebeu e compreendeu minimamente a situação apresentada.

Reconhecer não significa resolver, concordar ou assumir culpa.

### 5.8 Ação mínima

Ação mínima é uma resposta operacional válida suficiente para retirar uma apresentação crítica do primeiro plano.

Exemplos:

- iniciar um plano;
- justificar conscientemente;
- pedir ajuda;
- encaminhar a uma autoridade;
- assumir uma pendência;
- definir um próximo passo;
- resolver a situação.

### 5.9 Missão

Missão é uma interface focada e temporária criada em torno de um objetivo operacional.

Sua persistência, tarefas, participantes e colaboração pertencem à RFC-0010. Nesta RFC, Missão representa a experiência visual focada e sua continuidade.

### 5.10 Assistência progressiva

Assistência progressiva é o aumento gradual da ajuda oferecida conforme um erro, dificuldade ou padrão de falha se repete.

---

## 6. Princípios da Interface Viva

### 6.1 A interface normal permanece soberana

O usuário deverá continuar capaz de acessar os módulos e funções normais sem depender de comandos da IA.

A Interface Viva acelera, orienta e reorganiza; ela não elimina a navegabilidade convencional.

### 6.2 A interface não é fonte de autoridade

Ocultar, desabilitar ou destacar um elemento não substitui validações de permissão, regras de negócio ou persistência central.

### 6.3 Mudança visual deve ser compreensível

O usuário deverá entender:

- o que mudou;
- por que mudou;
- se a mudança é temporária;
- como restaurar a visão normal;
- qual ação está sendo solicitada;
- se dados reais serão alterados.

### 6.4 Intensidade proporcional

A intensidade visual deverá corresponder à criticidade, urgência, impacto e confiança da situação.

### 6.5 Menor interrupção eficaz

O Mheibos deverá utilizar a forma menos intrusiva capaz de alcançar o objetivo da intervenção.

### 6.6 Reversibilidade

Adaptações temporárias deverão ser reversíveis e não poderão destruir a configuração anterior necessária à continuidade.

### 6.7 Controle humano

A Interface Viva não poderá induzir o usuário a acreditar que uma sugestão já foi executada ou que uma decisão foi tomada em seu nome.

### 6.8 Acessibilidade

Informações importantes não poderão depender exclusivamente de cor, brilho, animação ou som.

---

## 7. Arquitetura de controle da interface

### 7.1 Fluxo geral

```text
Estado operacional ou solicitação do usuário
                    ↓
          Camada cognitiva ou módulo
                    ↓
        Intenção estruturada de interface
                    ↓
      Validação de identidade e permissão
                    ↓
      Política de intervenção e criticidade
                    ↓
          Orquestrador de Interface
                    ↓
       Componente visual autorizado
                    ↓
          Interface apresentada ao usuário
```

### 7.2 Ausência de controle direto pelo modelo

O modelo de linguagem não deverá:

- localizar widgets por reflexão livre;
- executar código na interface;
- acessar objetos gráficos internos;
- simular cliques arbitrários;
- preencher campos sem contrato;
- enviar mensagens sem autorização;
- persistir dados por comandos visuais;
- esconder avisos obrigatórios;
- bloquear a aplicação fora das políticas definidas.

### 7.3 Intenções estruturadas

Uma intenção deverá conter, conforme aplicável:

- tipo de ação;
- alvo lógico;
- contexto;
- motivo;
- criticidade;
- duração;
- comportamento de restauração;
- ações rápidas oferecidas;
- necessidade de confirmação;
- fallback quando o alvo não estiver disponível.

### 7.4 Validação

Antes da execução, o Mheibos deverá verificar:

- se o comando existe no catálogo permitido;
- se o alvo pertence à tela atual ou pode ser aberto;
- se o usuário pode acessar o conteúdo;
- se o comando conflita com uma ação sensível;
- se há uma intervenção crítica já ativa;
- se a mudança é temporária ou persistente;
- se existe alternativa acessível;
- se o comando continua relevante ao estado atual.

### 7.5 Resultado estruturado

O Orquestrador deverá devolver resultado equivalente a:

- executado;
- executado parcialmente;
- alvo indisponível;
- negado por permissão;
- negado por estado;
- substituído por alternativa segura;
- cancelado por mudança de contexto;
- falha técnica.

---

## 8. API interna de ações visuais

### 8.1 Navegação

A API deverá permitir ações equivalentes a:

- abrir módulo;
- abrir registro;
- fechar janela autorizada;
- retornar à visão anterior;
- selecionar aba;
- abrir painel lateral;
- alternar contexto permitido.

### 8.2 Foco e localização

A API deverá permitir:

- focar campo;
- rolar até elemento;
- selecionar linha;
- expandir seção;
- apontar próximo passo;
- revelar componente recolhido.

### 8.3 Filtros e organização

A API deverá permitir:

- aplicar filtro temporário;
- ordenar lista;
- agrupar registros;
- ocultar temporariamente itens não relacionados;
- restaurar filtros anteriores;
- montar visão resumida.

### 8.4 Destaques

A API deverá permitir:

- contorno;
- brilho;
- pulsação controlada;
- marcador visual;
- escurecimento do restante da tela;
- legenda explicativa;
- seta ou condução visual equivalente.

### 8.5 Intervenções

A API deverá permitir:

- comentário flutuante;
- alerta contextual;
- painel com ações rápidas;
- solicitação de reconhecimento;
- apresentação crítica;
- início de tour guiado;
- preparação de uma missão.

### 8.6 Restrições

A API interna não deverá expor comandos genéricos equivalentes a “execute qualquer código”, “clique em qualquer coordenada” ou “edite qualquer propriedade visual”.

---

## 9. A interface como meio de comunicação

### 9.1 Comunicação contextual

A intervenção deverá aparecer próxima ao elemento, registro ou decisão relacionada sempre que isso reduzir ambiguidade.

### 9.2 Condução visual

O Mheibos poderá conduzir o usuário por uma sequência de passos, desde que:

- o objetivo esteja declarado;
- a sequência seja compreensível;
- o usuário possa interromper quando permitido;
- ações persistentes continuem sujeitas às confirmações normais;
- o foco não esconda informação crítica contrária à recomendação.

### 9.3 Escurecimento do restante da tela

O escurecimento poderá ser usado para concentrar atenção, mas deverá:

- preservar legibilidade do alvo;
- manter saída acessível quando permitida;
- não simular bloqueio crítico em situação comum;
- não impedir acesso a recursos de segurança;
- respeitar preferências de acessibilidade.

### 9.4 Animações

Animações deverão ser limitadas, interrompíveis quando possível e substituíveis por indicadores estáticos para usuários que reduzam movimento.

### 9.5 Linguagem

A comunicação deverá ser:

- objetiva;
- respeitosa;
- gentil;
- orientada à ação;
- proporcional ao risco;
- livre de humilhação, acusação ou julgamento pessoal.

---

## 10. Fronteira entre adaptação temporária e alteração persistente

### 10.1 Regra fundamental

A aparência temporária poderá mudar automaticamente. A realidade persistente não.

### 10.2 Adaptações temporárias permitidas

Poderão ocorrer sem confirmação, quando autorizadas pela política:

- abrir uma tela;
- selecionar uma aba;
- aplicar um filtro temporário;
- ordenar uma lista;
- destacar registros;
- montar uma visão focada;
- apresentar ajuda;
- conduzir um tutorial;
- restaurar uma visão previamente conhecida.

### 10.3 Alterações persistentes protegidas

Exigem fluxo próprio de sugestão, confirmação e autorização:

- alterar dados;
- mudar estado;
- mudar responsável;
- enviar mensagem;
- criar tarefa oficial;
- alterar prazo;
- editar configuração;
- aplicar regra;
- concluir processo;
- registrar pagamento;
- modificar permissão;
- salvar preferência com impacto permanente quando não solicitada.

### 10.4 Conteúdo mínimo da sugestão

Antes da confirmação, a interface deverá apresentar, conforme aplicável:

- o que será alterado;
- o motivo;
- o registro afetado;
- valor anterior e novo valor;
- impacto esperado;
- riscos;
- necessidade de reautenticação;
- possibilidade de desfazer;
- ações de confirmar, editar ou cancelar.

### 10.5 Proibição de confirmação enganosa

O sistema não poderá utilizar botões, contagem regressiva, foco automático ou linguagem que faça uma alteração persistente parecer inevitável.

---

## 11. Níveis de intervenção

A política deverá suportar níveis equivalentes aos seguintes.

### 11.1 Nível 0 — Informação passiva

Utilizado para contexto complementar sem urgência.

Exemplos:

- etiqueta;
- indicador discreto;
- informação lateral;
- estado disponível para consulta.

Não bloqueia e não exige resposta.

### 11.2 Nível 1 — Comentário flutuante

É o padrão das intervenções do Mheibos.

Características:

- não bloqueante;
- curto;
- contextual;
- dispensável;
- sem reorganização intensa da tela;
- pode oferecer “ver detalhes”.

### 11.3 Nível 2 — Intervenção com ações rápidas

Utilizado quando existe risco ou oportunidade relevante e uma resposta simples pode resolver ou encaminhar.

Poderá oferecer:

- iniciar;
- adiar conscientemente;
- abrir registro;
- pedir ajuda;
- atribuir;
- revisar;
- ver impacto.

### 11.4 Nível 3 — Reconhecimento obrigatório

Utilizado quando a situação não deve permanecer invisível.

O usuário deverá reconhecer que percebeu o problema antes de restaurar integralmente a visão.

Reconhecimento não significa concordância nem resolução.

### 11.5 Nível 4 — Ação mínima obrigatória

Utilizado em situação crítica para usuários comuns.

A apresentação crítica somente será retirada depois de uma ação mínima válida.

### 11.6 Configurabilidade

Limites, exemplos e critérios poderão ser configurados por política, mas a implementação não poderá transformar qualquer recomendação comum em bloqueio crítico apenas para aumentar obediência.

---

## 12. Classificação de criticidade

### 12.1 Fatores

A criticidade deverá considerar, no mínimo:

- impacto operacional;
- urgência;
- risco financeiro;
- risco ao cliente;
- risco de segurança;
- quantidade de processos afetados;
- reversibilidade;
- prazo disponível;
- confiança da detecção;
- existência de responsável capaz de agir;
- repetição da situação.

### 12.2 Separação entre gravidade e confiança

Uma hipótese de alto impacto, mas baixa confiança, não deverá ser apresentada como fato crítico confirmado.

A interface poderá alertar sobre a incerteza e solicitar verificação.

### 12.3 Atualização

A criticidade deverá ser reavaliada quando o estado mudar.

Uma intervenção não poderá permanecer crítica depois que o risco tiver sido resolvido, invalidado ou reduzido.

### 12.4 Explicação

Intervenções relevantes ou críticas deverão permitir acesso aos fundamentos da classificação.

---

## 13. Situações normais e restauração da visão

### 13.1 Reconhecimento suficiente

Quando uma adaptação temporária for causada por situação normal, qualquer usuário autorizado poderá restaurar a visão original depois de reconhecer o aviso.

### 13.2 Formas de reconhecimento

O reconhecimento poderá ocorrer por ação equivalente a:

- “Entendi”;
- “Voltar à visão normal”;
- “Ver depois”;
- “Manter esta organização”;
- abertura consciente dos detalhes.

### 13.3 Estado subjacente

Restaurar a visão não apaga o evento, risco, pendência ou recomendação que originou a intervenção.

### 13.4 Reapresentação

A situação poderá reaparecer quando:

- houver mudança material;
- o prazo se aproximar;
- a criticidade aumentar;
- o usuário tiver solicitado lembrete;
- a política de pendência determinar novo contato.

A frequência pertence à RFC-0012.

---

## 14. Situações críticas

### 14.1 Usuários comuns

Um usuário comum não poderá remover a apresentação crítica apenas fechando a caixa, mudando de tela ou reiniciando a aplicação.

Ele deverá executar uma ação mínima válida, como:

- iniciar um plano;
- registrar justificativa;
- pedir ajuda;
- encaminhar a um gerente;
- assumir uma tarefa;
- definir prazo autorizado;
- resolver a situação.

### 14.2 Administradores

Administradores poderão restaurar a interface após reconhecimento, desde que possuam permissão correspondente.

Essa possibilidade não deverá:

- apagar a situação;
- encerrar automaticamente a pendência;
- remover a responsabilidade de terceiros;
- excluir o histórico;
- impedir reapresentação futura por mudança material.

### 14.3 Ausência de punição visual

A apresentação crítica deverá orientar para uma decisão ou próximo passo. Ela não poderá ser usada como punição, constrangimento ou exposição pública.

### 14.4 Segurança e emergência

A intervenção crítica não poderá bloquear:

- saída segura da aplicação;
- acesso a ajuda;
- recursos de acessibilidade;
- ações necessárias à segurança física;
- recuperação técnica autorizada.

### 14.5 Auditoria

Ações mínimas, reconhecimentos administrativos e restaurações críticas deverão produzir registros compatíveis com a RFC-0006 quando tiverem relevância operacional ou de segurança.

---

## 15. Ações rápidas

### 15.1 Finalidade

Ações rápidas reduzem a distância entre percepção e resposta.

### 15.2 Requisitos

Uma ação rápida deverá:

- ter resultado claro;
- respeitar permissões;
- informar quando altera dados;
- exigir confirmação quando persistente;
- exigir reautenticação quando sensível;
- usar o estado atual antes da execução;
- produzir evento quando houver alteração relevante.

### 15.3 Preparação não é execução

A interface poderá preencher uma proposta, abrir o registro correto ou preparar uma mensagem, mas não deverá executar silenciosamente uma alteração persistente.

### 15.4 Estado desatualizado

Se o objeto mudar entre a apresentação e o clique, a ação deverá ser revalidada e, quando necessário, reapresentada com o novo impacto.

---

## 16. Personalização individual

### 16.1 Regra

A Interface Viva poderá adaptar organização, filtros, atalhos, densidade de informação e forma de assistência para cada usuário.

### 16.2 Mesmo perfil, experiências diferentes

Dois usuários com o mesmo perfil poderão receber:

- ordem diferente de atalhos;
- filtros iniciais diferentes;
- lembretes em momentos diferentes;
- maior ou menor detalhamento;
- formas distintas de tutorial;
- destaque antecipado de riscos compatíveis com seus padrões de trabalho.

### 16.3 Limites

A personalização não poderá:

- conceder permissão;
- retirar obrigação formal;
- alterar regra de negócio;
- ocultar permanentemente informação obrigatória;
- modificar dados globais;
- criar tratamento discriminatório injustificável;
- expor padrões individuais a outros usuários sem autorização.

### 16.4 Preferências explícitas

O usuário deverá poder definir ou revisar preferências equivalentes a:

- densidade de informação;
- redução de movimento;
- intensidade de animação;
- frequência de dicas não críticas;
- nível inicial de detalhe;
- manutenção ou restauração de determinados layouts pessoais.

### 16.5 Preferências aprendidas

Preferências inferidas deverão ser tratadas como adaptações revisáveis, não como verdade permanente sobre a pessoa.

---

## 17. Padrões de atenção e assistência antecipada

### 17.1 Finalidade

O Mheibos poderá perceber que determinado usuário frequentemente deixa de notar um tipo de aviso, esquece um passo ou encontra dificuldade recorrente em uma parte da interface.

### 17.2 Uso permitido

O sistema poderá utilizar esse padrão para:

- antecipar lembrete;
- reposicionar informação;
- destacar o próximo passo;
- reduzir quantidade de elementos simultâneos;
- iniciar tutorial;
- oferecer checklist;
- confirmar compreensão.

### 17.3 Proibições

O sistema não deverá:

- diagnosticar condição médica ou psicológica;
- criar rótulo de distraído, incapaz ou improdutivo;
- expor o padrão a colegas;
- usar o padrão para humilhar;
- transformá-lo automaticamente em avaliação de desempenho;
- inferir atributo sensível sem base e finalidade legítima.

### 17.4 Linguagem interna e externa

A interface deverá comunicar a necessidade operacional, e não uma interpretação pessoal.

Exemplo adequado:

> “Este passo costuma ficar pendente. Quer que eu o destaque antes de concluir?”

Exemplo inadequado:

> “Você sempre esquece porque é desatento.”

### 17.5 Revisão

Adaptações baseadas em padrão de atenção deverão poder ser desativadas, ajustadas ou esquecidas conforme governança aplicável.

---

## 18. Interface focada por objetivo

### 18.1 Criação

Quando o usuário declarar um objetivo, o Mheibos poderá montar uma visão temporária que reúna:

- módulos relevantes;
- listas filtradas;
- pedidos relacionados;
- processos bloqueados;
- tarefas;
- prazos;
- indicadores;
- ações recomendadas;
- conversas e notas autorizadas.

### 18.2 Natureza

A interface focada é uma forma de organização, não um novo sistema nem uma substituição da navegação normal.

### 18.3 Origem

Uma missão poderá ser:

- criada pelo usuário;
- sugerida pela IA e aceita;
- atribuída por autoridade conforme RFC-0010.

### 18.4 Conteúdo e permissões

A missão somente poderá reunir informações que o usuário ou participante possa acessar.

### 18.5 Alterações

Montar a visão não altera automaticamente:

- responsáveis;
- prazos;
- estados;
- prioridades oficiais;
- tarefas persistentes;
- permissões.

### 18.6 Saída

O usuário poderá sair da missão para utilizar a interface comum, observadas as regras de missões atribuídas e situações críticas.

---

## 19. Pausa e retomada de missões

### 19.1 Pausa

Pausar uma missão deverá preservar, conforme aplicável:

- objetivo;
- progresso;
- filtros;
- registros selecionados;
- posição de navegação relevante;
- tarefas e bloqueios;
- notas;
- próximos passos;
- contexto necessário à retomada.

### 19.2 Trabalho comum

Durante a pausa, o usuário poderá executar trabalho normal sem perder a missão.

### 19.3 Retomada

Ao retomar, o Mheibos deverá:

- revalidar permissões;
- atualizar estados alterados;
- indicar mudanças relevantes ocorridas durante a pausa;
- restaurar o contexto compatível;
- não reaplicar cegamente filtros ou comandos inválidos.

### 19.4 Missão desatualizada

Se o objetivo tiver sido resolvido, cancelado ou tornado impossível, a interface deverá informar a mudança e oferecer encerramento ou revisão.

### 19.5 Persistência

A persistência conceitual da missão pertence ao RFC-0010 e ao modelo de dados da RFC-0005.

---

## 20. Erros recorrentes e assistência progressiva

### 20.1 Detecção

O Mheibos poderá detectar repetição de erro relevante por eventos, validações, correções ou padrões operacionais comprováveis.

### 20.2 Gatilho inicial

Por padrão, a terceira ocorrência configurável deverá ser suficiente para iniciar assistência progressiva, salvo quando:

- o risco exigir intervenção na primeira ocorrência;
- o erro for irrelevante;
- a repetição ainda não estiver suficientemente confirmada;
- a política do processo definir outro limite.

### 20.3 Progressão conceitual

A assistência poderá evoluir por níveis equivalentes a:

1. dica discreta;
2. explicação contextual;
3. destaque do passo correto;
4. confirmação antes de prosseguir;
5. checklist;
6. tutorial guiado;
7. sugestão de treinamento ou pedido de ajuda.

### 20.4 Objetivo

O objetivo é prevenir repetição e apoiar aprendizagem, não punir.

### 20.5 Reinício ou redução

A intensidade deverá diminuir quando o usuário demonstrar domínio ou quando o padrão deixar de ocorrer.

### 20.6 Exposição

A assistência individual não deverá ser exibida publicamente a colegas.

Informações gerenciais, quando autorizadas, deverão priorizar o impacto no processo e a necessidade de apoio.

---

## 21. Treinamento guiado

### 21.1 Início

Um treinamento poderá ser:

- solicitado pelo usuário;
- sugerido após erro recorrente;
- recomendado pela IA;
- atribuído conforme política organizacional futura.

### 21.2 Caminho oficial essencial

O treinamento deverá apresentar primeiro:

- objetivo do procedimento;
- passo atual;
- ação necessária;
- critério de conclusão;
- alerta essencial de segurança ou qualidade.

### 21.3 Tour guiado

O tour poderá:

- abrir a tela correta;
- destacar o componente;
- explicar a ação;
- aguardar o usuário;
- validar o resultado;
- avançar ao próximo passo.

### 21.4 Simulação e operação real

A interface deverá diferenciar claramente treinamento simulado de operação real.

Ações persistentes reais continuarão sujeitas a permissões e confirmações.

### 21.5 Interrupção e retomada

O treinamento deverá poder ser pausado e retomado quando isso não comprometer uma operação sensível em andamento.

---

## 22. Divulgação progressiva

### 22.1 Regra

O Mheibos deverá mostrar primeiro o conteúdo essencial para executar corretamente o procedimento.

### 22.2 Conteúdo complementar

Uma ação equivalente a **“Ver mais”** poderá revelar:

- explicação aprofundada;
- alternativas autorizadas;
- exceções;
- motivos da regra;
- atalhos;
- exploração do módulo;
- perguntas frequentes;
- histórico ou exemplos.

### 22.3 Prevenção de sobrecarga

O tutorial não deverá apresentar todas as possibilidades antes que o usuário compreenda o caminho básico.

### 22.4 Não ocultação de informação crítica

Divulgação progressiva não poderá esconder riscos, restrições ou requisitos obrigatórios necessários à decisão atual.

---

## 23. Notificações flutuantes e coexistência visual

### 23.1 Padrão visual

Intervenções comuns serão apresentadas principalmente por comentários ou pop-ups flutuantes contextualizados.

### 23.2 Empilhamento

A interface deverá evitar sobreposição descontrolada de múltiplas intervenções.

Ela poderá:

- agregar mensagens relacionadas;
- priorizar criticidade;
- adiar dicas não urgentes;
- apresentar uma fila consultável;
- manter somente uma intervenção focal por vez.

### 23.3 Não subnotificação

Uma falha visual não poderá apagar a obrigação de comunicação criada por um evento relevante.

### 23.4 Não supernotificação

O Mheibos deverá evitar repetição excessiva, animações contínuas e pop-ups que interrompam o trabalho sem benefício proporcional.

A política temporal e de escalonamento pertence à RFC-0012.

---

## 24. Concorrência entre intervenções

### 24.1 Prioridade

Quando múltiplas intervenções competirem, a ordem deverá considerar:

- segurança;
- criticidade;
- prazo;
- impacto;
- contexto atual;
- possibilidade de agregação;
- dependência entre ações.

### 24.2 Intervenção crítica ativa

Uma intervenção comum não deverá cobrir ou substituir uma apresentação crítica ativa.

### 24.3 Missão ativa

Intervenções relacionadas à missão poderão ser incorporadas ao contexto focado. Intervenções externas críticas poderão interromper ou suspender temporariamente a missão.

### 24.4 Mudança de contexto

Comandos de interface pendentes deverão ser cancelados ou revalidados quando o usuário mudar de tela, sessão, missão ou registro.

---

## 25. Acessibilidade e ergonomia

### 25.1 Múltiplos sinais

Criticidade e estado deverão ser comunicados por combinação de texto, ícone, posição, contraste e, quando útil, animação.

### 25.2 Redução de movimento

O usuário deverá poder reduzir ou eliminar pulsação, brilho e transições não essenciais.

### 25.3 Navegação por teclado

Intervenções, ações rápidas, reconhecimento e saída deverão ser utilizáveis por teclado quando a plataforma permitir.

### 25.4 Leitura assistiva

Textos, alvos e estados deverão possuir descrições compatíveis com tecnologias assistivas adotadas pela implementação.

### 25.5 Foco previsível

O Orquestrador não deverá mover o foco repetidamente enquanto o usuário digita ou executa ação delicada, salvo risco crítico que justifique interrupção.

### 25.6 Tempo suficiente

Intervenções que exigem leitura ou decisão não deverão desaparecer antes que o usuário tenha tempo razoável de compreendê-las.

---

## 26. Segurança e permissões

### 26.1 Herança da sessão

Toda ação visual deverá operar dentro da identidade e permissões do usuário atual.

### 26.2 Não revelação

A Interface Viva não poderá abrir, destacar, resumir ou pré-carregar conteúdo que o usuário não possa acessar normalmente.

### 26.3 Ações sensíveis

A preparação visual de uma ação sensível não elimina:

- reautenticação;
- justificativa;
- bloqueio de edição;
- validação central;
- auditoria.

### 26.4 Bloqueios de edição

A interface deverá informar quando um registro está bloqueado por outro usuário e não poderá apresentar ação rápida de edição como se estivesse disponível.

### 26.5 Modo offline

No modo offline, o Orquestrador somente poderá oferecer ações compatíveis com a RFC-0008.

Uma sugestão visual não poderá contornar a indisponibilidade da Central.

---

## 27. Registro, auditoria e privacidade

### 27.1 Ações temporárias comuns

Nem toda seleção de aba, rolagem ou destaque precisa gerar evento de negócio.

### 27.2 Intervenções relevantes

Deverão ser registradas quando necessário:

- intervenção crítica apresentada;
- reconhecimento;
- ação mínima escolhida;
- restauração administrativa;
- treinamento iniciado ou concluído;
- alteração persistente confirmada a partir de sugestão;
- falha do Orquestrador que impeça comunicação obrigatória.

### 27.3 Separação de logs

Logs técnicos do Orquestrador não substituem eventos de domínio ou auditoria.

### 27.4 Minimização

Dados de uso da interface deverão ser coletados somente na medida necessária à assistência, segurança, diagnóstico ou melhoria autorizada.

### 27.5 Padrões individuais

Registros de padrão de atenção ou dificuldade deverão possuir escopo restrito e governança compatível com os RFCs 0011 e 0016.

---

## 28. Falhas previstas e recuperação

### 28.1 Alvo inexistente

Se o elemento solicitado não existir na versão atual da tela, o Orquestrador deverá usar fallback seguro ou informar que não conseguiu concluir a ação visual.

### 28.2 Tela alterada

Se a interface mudar depois que o comando foi criado, o comando deverá ser revalidado.

### 28.3 Loop de navegação

O sistema deverá detectar sequências repetitivas ou contraditórias de comandos e interrompê-las.

### 28.4 Falha de animação

Uma falha de destaque não poderá impedir a apresentação textual da informação essencial.

### 28.5 Falha de restauração

O Cliente deverá manter forma segura de retornar à navegação normal, preservando a situação crítica quando aplicável.

### 28.6 Falha da IA

A indisponibilidade da IA não deverá impedir o uso normal dos módulos.

Intervenções determinísticas e avisos obrigatórios poderão continuar funcionando sem o modelo.

### 28.7 Reinicialização

Após reiniciar o Cliente, a aplicação deverá restaurar somente os estados visuais persistentes necessários, revalidando missão, criticidade, permissões e relevância.

---

## 29. Desempenho

### 29.1 Responsividade

Comandos comuns de navegação e destaque deverão ser executados sem atraso perceptível na estação.

### 29.2 Não bloqueio da thread visual

Análises cognitivas, recuperação de contexto e processamento secundário não deverão bloquear a interface.

### 29.3 Carregamento progressivo

Visões focadas poderão carregar informações progressivamente, desde que deixem claro o que ainda está sendo preparado.

### 29.4 Limites

A implementação deverá limitar:

- quantidade de elementos animados;
- número de filtros simultâneos;
- profundidade de tours;
- frequência de reorganizações automáticas;
- memória ocupada por estados de interface pausados.

---

## 30. Contratos com outros componentes

### 30.1 Arquitetura Técnica

O Orquestrador de Interface pertence ao Cliente Mheibos e consome contratos estáveis, conforme RFC-0003.

### 30.2 Arquitetura Cognitiva

A IA poderá propor intenções e intervenções, mas não executará diretamente comandos visuais, conforme RFC-0004.

### 30.3 Modelo de Dados

Preferências persistentes, missões, eventos e referências deverão utilizar entidades compatíveis com a RFC-0005.

### 30.4 Eventos e Auditoria

Intervenções relevantes, reconhecimentos e alterações persistentes deverão produzir eventos conforme RFC-0006.

### 30.5 Identidade e Segurança

Toda ação respeitará perfil, permissão, reautenticação e bloqueio conforme RFC-0007.

### 30.6 Operação Offline

A interface deverá refletir claramente as restrições da RFC-0008.

### 30.7 Missões e Teamwork

Objetivo, participantes, tarefas, chat, notas e regras de colaboração pertencem à RFC-0010.

### 30.8 Pendências e Escalonamento

Frequência, repetição, scheduler e escalonamento de intervenções pertencem à RFC-0012.

### 30.9 Governança da IA

Uso de padrões individuais, ensino e limites humanos pertencem também à RFC-0016.

---

## 31. Invariantes

Toda implementação deverá preservar as seguintes invariantes:

1. a IA nunca manipula diretamente widgets ou executa código da interface;
2. toda ação visual automatizada pertence a um catálogo controlado;
3. comandos são validados antes da execução;
4. a interface normal permanece utilizável sem interação obrigatória com a IA;
5. adaptação temporária não altera dados persistentes;
6. alteração persistente exige fluxo explícito de sugestão e confirmação;
7. uma ação visual não concede permissão;
8. a Interface Viva não revela dados fora do escopo do usuário;
9. intervenções possuem intensidade proporcional;
10. comentário flutuante não bloqueante é o padrão;
11. apresentação crítica não pode ser usada como punição;
12. usuários comuns precisam de ação mínima para retirar situação crítica;
13. administradores podem restaurar a interface após reconhecimento, sem apagar a situação;
14. restauração visual não encerra silenciosamente pendência ou risco;
15. personalização não modifica regras ou permissões;
16. uma missão não substitui a interface normal;
17. pausa de missão preserva contexto necessário à retomada;
18. retomada revalida estado e permissões;
19. assistência progressiva deve ser preventiva e respeitosa;
20. padrões individuais não podem produzir diagnóstico ou exposição indevida;
21. tutoriais mostram primeiro o caminho essencial;
22. informação crítica não pode depender somente de cor ou animação;
23. falha visual não pode apagar comunicação obrigatória;
24. falha da IA não pode inutilizar a aplicação normal;
25. intervenções relevantes permanecem rastreáveis quando exigido.

---

## 32. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. existir um Orquestrador de Interface ou componente equivalente;
2. a IA produzir comandos estruturados em vez de manipular diretamente a interface;
3. houver catálogo explícito de ações visuais permitidas;
4. comandos forem validados por identidade, permissão, estado e contexto;
5. a API suportar navegação, foco, rolagem, filtros e destaques controlados;
6. adaptações temporárias forem separadas de alterações persistentes;
7. alterações persistentes apresentarem impacto e exigirem confirmação;
8. o padrão de intervenção for não bloqueante;
9. níveis relevantes puderem oferecer ações rápidas;
10. situações críticas puderem exigir reconhecimento ou ação mínima;
11. usuários comuns não puderem dispensar uma situação crítica sem ação mínima válida;
12. administradores puderem restaurar a interface após reconhecimento autorizado;
13. restaurações críticas forem rastreáveis;
14. a personalização permanecer individual e não alterar permissões;
15. objetivos puderem gerar visões focadas temporárias;
16. missões puderem ser pausadas e retomadas com contexto preservado;
17. a retomada revalidar dados e permissões;
18. erros recorrentes puderem acionar assistência progressiva;
19. o limiar padrão de terceira ocorrência for configurável;
20. a assistência utilizar linguagem respeitosa e orientada à solução;
21. padrões de atenção não forem tratados como diagnóstico;
22. tutoriais utilizarem divulgação progressiva;
23. recursos de acessibilidade não dependerem exclusivamente de animação ou cor;
24. a falha do Orquestrador possuir fallback textual ou seguro;
25. a indisponibilidade da IA não impedir a navegação convencional.

---

## 33. Consequências da decisão

### 33.1 Benefícios

- assistência contextual sem substituir a interface convencional;
- redução da distância entre problema e ação;
- melhor uso da atenção humana;
- aprendizagem dentro do próprio trabalho;
- personalização sem fragmentar regras;
- possibilidade de orientar usuários iniciantes;
- criação de ambientes focados por objetivo;
- controle técnico sobre a atuação visual da IA;
- redução do risco de comandos arbitrários do modelo;
- caminho para intervenções proporcionais e rastreáveis.

### 33.2 Custos e limitações

- necessidade de manter catálogo e contratos de interface;
- maior complexidade no gerenciamento de estado visual;
- necessidade de acessibilidade e fallback para animações;
- necessidade de revalidar comandos após mudanças de contexto;
- persistência controlada de missões e preferências;
- risco de excesso de interrupções se a política for mal calibrada;
- necessidade de distinguir com rigor adaptação temporária e mudança real.

### 33.3 Riscos

- transformar a interface em ambiente imprevisível;
- permitir que a IA simule autoridade;
- usar criticidade para forçar obediência;
- sobrecarregar o usuário com pop-ups;
- esconder funções normais atrás da IA;
- personalizar de modo opaco;
- expor padrões individuais;
- manter intervenções desatualizadas;
- prender o usuário em loops de tutorial;
- salvar alterações persistentes por meio de ações aparentemente visuais.

### 33.4 Mitigações

Os riscos deverão ser reduzidos por:

- comandos estruturados;
- catálogo fechado;
- validação por camadas;
- níveis de criticidade;
- explicação e reversibilidade;
- interface normal sempre acessível;
- logs e auditoria proporcionais;
- preferências de acessibilidade;
- critérios de parada;
- revalidação contínua do estado.

---

## 34. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em RFCs posteriores:

- framework e biblioteca visual definitivos;
- esquema concreto dos comandos de interface;
- nomenclatura final das ações;
- animações, durações e curvas de transição;
- design visual dos níveis de criticidade;
- política exata de agregação de pop-ups;
- catálogo inicial completo de ações rápidas;
- limiares concretos de criticidade;
- critérios técnicos de detecção de erro recorrente;
- algoritmo de adaptação individual;
- formato de persistência do estado visual;
- integração definitiva com o sistema de missões;
- telemetria necessária ao aprendizado da interface;
- política de retenção de padrões individuais;
- compatibilidade com tecnologias assistivas específicas;
- modo de teste automatizado do Orquestrador;
- tratamento visual definitivo do modo offline;
- interface integrada de WhatsApp.

Essas escolhas não poderão violar as invariantes de controle humano, separação entre visual e persistente, permissão, acessibilidade e não exposição definidas nesta RFC.

---

## 35. Declaração normativa

A interface do Mheibos será uma superfície operacional viva e controlada.

Ela poderá adaptar temporariamente a apresentação, abrir contextos, aplicar filtros, destacar elementos, conduzir o usuário e oferecer assistência, desde que opere por uma API interna de comandos estruturados e validados.

A IA não controlará diretamente widgets nem executará código visual arbitrário. Alterações persistentes começarão como sugestões, apresentarão impacto e dependerão da autorização correspondente. Adaptações temporárias poderão ocorrer automaticamente quando forem locais, reversíveis e incapazes de modificar a realidade oficial.

Intervenções serão proporcionais à criticidade. O padrão será um comentário flutuante não bloqueante. Situações relevantes poderão oferecer ações rápidas. Situações críticas poderão exigir reconhecimento ou ação mínima. Usuários comuns deverão encaminhar conscientemente a situação antes de retirar a apresentação crítica; administradores poderão restaurar a interface após reconhecimento autorizado, sem apagar o problema subjacente.

A personalização será individual e não alterará permissões ou regras de negócio. Objetivos poderão gerar missões com interface focada, pausável e retomável. Erros recorrentes deverão acionar assistência progressiva, respeitosa e preventiva. O sistema poderá adaptar o apoio aos padrões de atenção do usuário, mas não poderá diagnosticar, rotular, humilhar ou expor características pessoais.

Tutoriais deverão apresentar primeiro o caminho oficial essencial e revelar informações complementares progressivamente.

---

## 36. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-052 — IA controla a interface por API interna | 7 e 8 |
| INV-053 — interface como meio de comunicação | 9 |
| INV-054 — alterações persistentes começam como sugestão | 10 |
| INV-055 — adaptações temporárias locais e automáticas | 10.2 e 16 |
| INV-056 — níveis de criticidade | 11 e 12 |
| INV-057 — reconhecimento restaura situações normais | 13 |
| INV-058 — situações críticas por perfil | 14 |
| INV-059 — personalização individual | 16 e 17 |
| INV-060 — objetivo gera interface focada | 18 |
| INV-061 — missões pausáveis e retomáveis | 19 |
| INV-062 — erros recorrentes acionam assistência progressiva | 20 |
| INV-063 — adaptação ao padrão de atenção | 17 |
| INV-064 — tutorial com divulgação progressiva | 21 e 22 |
