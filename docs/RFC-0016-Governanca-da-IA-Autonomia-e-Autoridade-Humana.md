# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0016 — Governança da IA, Autonomia e Autoridade Humana

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 10/08/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0003, RFC-0004, RFC-0006, RFC-0007, RFC-0009, RFC-0010, RFC-0011, RFC-0012  
**Documento futuro obrigatório:** Modelo de Decisões Autônomas da IA

---

## 1. Resumo

Esta RFC define a governança da autonomia da Inteligência Artificial do Mheibos e a relação de autoridade entre IA, usuários, gerentes, administradores, Conselho de Gerentes e as regras normativas da plataforma.

A IA poderá possuir autonomia operacional real, mas essa autonomia nunca será irrestrita. A possibilidade de executar uma ação autonomamente dependerá do tipo da ação, impacto, reversibilidade, confiança, permissões, política vigente e demais critérios definidos pelo Mheibos.

O próprio produto estabelecerá o teto máximo de autonomia. Dentro desse limite, autoridades humanas competentes poderão reduzir ou configurar a autonomia da instalação, mas não poderão conceder à IA poderes proibidos pelas normas do Mheibos.

Toda decisão autônoma deverá ser tecnicamente reversível, planejada antes da execução, explicável, auditável e recuperável diante de falhas. Nenhuma ação que possa produzir consequência irreversível em caso de execução incompleta poderá ser elegível para autonomia.

A autoridade humana poderá reverter decisões da IA conforme níveis de governança. Algumas reversões poderão ser realizadas por um gerente; decisões de maior relevância exigirão Conselho de Gerentes, com pelo menos dois gerentes autenticando conjuntamente quando aplicável.

A IA poderá reduzir preventivamente sua própria autonomia, mas jamais ampliá-la ou restaurá-la por conta própria. Poderá propor alterações fundamentadas, mas qualquer ampliação dependerá da autoridade humana competente e continuará limitada pelo teto normativo do produto.

Acima de toda autonomia existe uma regra absoluta: a IA deverá cumprir integralmente as normas vigentes do Mheibos. Ela não poderá violá-las, contorná-las, reinterpretá-las para escapar de seus efeitos nem utilizar ações indiretas ou equivalentes para alcançar um resultado que a norma pretende impedir.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- como determinar se uma ação pode ser executada autonomamente pela IA;
- quem pode configurar ou limitar a autonomia;
- o que acontece quando o usuário não possui autoridade suficiente;
- como solicitações de autorização são escalonadas;
- quais são os limites da urgência;
- como decisões autônomas podem ser revertidas;
- quando uma reversão exige um gerente ou Conselho de Gerentes;
- como reversões afetam decisões futuras semelhantes;
- como a autonomia suspensa pode ser restaurada;
- quais informações devem ser registradas antes e depois de uma decisão;
- como decisões autônomas são apresentadas aos usuários;
- como tratar decisões que afetam outras pessoas;
- como resolver conflitos entre decisões autônomas;
- como funcionam cadeias e execuções simultâneas;
- como confiança limita a execução;
- como falhas técnicas devem ser recuperadas;
- como novas informações durante uma execução são tratadas;
- como desempenho computacional limita a autonomia;
- como funcionam janelas autorizadas de execução;
- como a IA opera sem usuários presentes;
- como execuções desacompanhadas são relatadas;
- por quanto tempo a auditoria cognitiva é preservada;
- se a IA pode propor ampliação ou redução da própria autonomia;
- como IA cognitiva e automações determinísticas se diferenciam;
- qual é a fronteira normativa absoluta que a IA jamais poderá ultrapassar.

Esta RFC não define o catálogo concreto de ações autônomas. Esse catálogo deverá ser especificado em documento normativo próprio.

---

## 3. Decisões fundamentais

A governança da IA adota as seguintes decisões:

1. A autonomia é contextual e depende de tipo da ação, impacto, reversibilidade, confiança, permissões e política vigente.
2. O Mheibos define o teto máximo de autonomia permitido pelo produto.
3. Autoridades da empresa podem configurar autonomia somente dentro desse teto.
4. Se o usuário não possuir autoridade para uma ação, a IA poderá solicitar autorização a um gerente competente quando o escalonamento for permitido.
5. Autorizações pendentes serão formalizadas e poderão ser escalonadas pela cadeia Responsável → Gerente → Administrador.
6. A ausência de autoridade disponível nunca transfere autoridade extraordinária para a IA.
7. Toda ação elegível para autonomia deverá ser tecnicamente reversível.
8. A reversão de decisões autônomas será classificada por nível de importância.
9. Decisões simples poderão ser revertidas por gerente autorizado.
10. Decisões de maior relevância poderão exigir Conselho de Gerentes, com pelo menos dois gerentes autenticando conjuntamente quando aplicável.
11. A IA poderá alertar sobre consequências de uma reversão, mas deverá obedecer à decisão humana competente.
12. Reversões serão registradas como feedback, sem alterar automaticamente a política global de autonomia.
13. Uma reversão suspenderá contextualmente a autonomia para situações suficientemente semelhantes, que passarão a exigir confirmação humana.
14. A autonomia suspensa somente retornará por decisão humana explícita.
15. A restauração exigirá o mesmo nível de autoridade necessário para a reversão.
16. Toda decisão autônoma possuirá registro estruturado de explicabilidade.
17. A visibilidade da decisão será proporcional à sua relevância.
18. A autonomia deverá considerar as pessoas afetadas pela decisão.
19. Conflitos entre decisões serão resolvidos por regras determinísticas de criticidade, autoridade e prioridade; conflitos não resolvidos irão para decisão humana.
20. Uma cadeia poderá ser executada autonomamente quando cada ação concreta da cadeia estiver individualmente autorizada.
21. Confiança insuficiente impede execução autônoma e transforma a ação em proposta humana.
22. Toda ação autônoma deverá possuir planejamento prévio e estratégia segura de reversão/recuperação.
23. Mudanças normais de contexto não interrompem uma decisão autônoma válida já iniciada.
24. Decisões concorrentes serão preferencialmente sequenciais, podendo ocorrer em paralelo apenas quando independentes e computacionalmente seguras.
25. O trabalho humano interativo terá prioridade sobre cargas autônomas pesadas.
26. Limites de recursos e janelas autorizadas de execução poderão ser configurados.
27. Exceções à janela de execução respeitarão a mesma hierarquia de autoridade da decisão original.
28. Durante uma janela autorizada, a IA poderá operar sem presença humana.
29. Execuções desacompanhadas produzirão relatório consolidado.
30. Registros de decisões autônomas serão permanentes.
31. A IA poderá propor ampliação de autonomia, mas jamais concedê-la a si própria.
32. A IA poderá reduzir preventivamente a própria autonomia.
33. Desligar a IA cognitiva não desligará automações determinísticas essenciais do Mheibos.
34. A IA estará absolutamente subordinada às regras normativas vigentes e não poderá contorná-las por qualquer meio.

---

## 4. Separação entre esta RFC e o Modelo de Decisões Autônomas

### 4.1 Regra

Esta RFC define a constituição da autonomia, não o catálogo completo das ações autônomas.

### 4.2 Documento futuro

Um documento normativo específico deverá definir, para cada categoria de decisão, conforme aplicável:

- ação;
- finalidade;
- condições de elegibilidade;
- nível de importância;
- impacto;
- confiança mínima;
- pessoas que podem ser afetadas;
- permissões necessárias;
- reversibilidade;
- autoridade necessária para reversão;
- autoridade necessária para restauração;
- regras de conflito;
- possibilidade de encadeamento;
- possibilidade de paralelismo;
- impacto computacional;
- janela de execução;
- requisitos de evidência;
- requisitos adicionais de auditoria.

### 4.3 Proibição de ações irreversíveis

O catálogo futuro não poderá classificar como autônoma nenhuma decisão tecnicamente irreversível.

---

## 5. Teto normativo de autonomia

O Mheibos estabelecerá limites máximos que a configuração da empresa não poderá ultrapassar.

Administradores e gerentes autorizados poderão reduzir a autonomia ou habilitar possibilidades previstas pelo produto dentro de suas competências.

Nenhuma configuração local poderá:

- conceder poder proibido pelo Mheibos;
- transformar uma ação normativa proibida em ação autônoma;
- remover requisito obrigatório de autorização;
- permitir violação de permissões;
- transformar urgência em autoridade;
- alterar normas fundamentais do produto.

---

## 6. Autoridade insuficiente e escalonamento

### 6.1 Usuário sem autoridade

Quando uma decisão depender de autoridade que o usuário atual não possui, a IA não executará utilizando autoridade inexistente.

Quando permitido, poderá solicitar autorização superior.

### 6.2 Pendência formal

A solicitação deverá gerar uma pendência de autorização contendo, conforme aplicável:

- ação proposta;
- origem;
- motivo;
- impacto;
- urgência;
- responsável atual;
- autoridade necessária;
- estado;
- histórico de escalonamento.

A operação protegida permanecerá bloqueada enquanto a autorização não existir.

### 6.3 Cadeia de escalonamento

A cadeia padrão será:

```text
Responsável
    ↓
Gerente
    ↓
Administrador
```

A ausência de resposta poderá provocar escalonamento determinístico.

### 6.4 Limite

Se a cadeia for esgotada, a IA manterá a situação crítica e aguardará autoridade humana.

Mesmo diante de prejuízo potencial, a ausência de autoridade não permite execução excepcional.

---

## 7. Reversibilidade obrigatória

### 7.1 Invariante

Toda decisão autônoma deverá ser tecnicamente reversível.

### 7.2 Elegibilidade

Uma ação não poderá ser iniciada autonomamente quando:

- sua execução parcial puder causar consequência irreversível;
- não houver forma confiável de restaurar estado consistente;
- uma falha puder deixar efeitos que não possam ser desfeitos;
- a recuperação depender de suposição não verificável.

### 7.3 Reversão humana

Decisões serão classificadas por relevância.

Categorias simples poderão permitir reversão por qualquer gerente autorizado.

Categorias de maior importância poderão exigir Conselho de Gerentes.

### 7.4 Conselho de Gerentes

Quando a categoria exigir decisão colegiada e existirem dois ou mais gerentes aplicáveis, pelo menos dois deverão autenticar conjuntamente a reversão.

A mesma regra valerá para a restauração posterior da autonomia daquele padrão.

---

## 8. Contestação preventiva da reversão

Antes da confirmação final de uma reversão, a IA poderá apresentar:

- consequências;
- riscos;
- dependências;
- impactos esperados;
- alternativas.

A apresentação será informativa.

Se a autoridade competente mantiver a reversão, a IA deverá executá-la.

A IA não possui poder de veto sobre decisão humana válida dentro da competência daquela autoridade.

---

## 9. Feedback de reversões e freio contextual

### 9.1 Feedback

Toda reversão será registrada como feedback cognitivo.

Ela poderá ser considerada em análises futuras, mas não alterará automaticamente o catálogo global de autonomia.

### 9.2 Suspensão contextual

Quando uma decisão autônoma for revertida, situações suficientemente semelhantes deixarão temporariamente de ser autônomas.

O fluxo será:

```text
Decisão autônoma
      ↓
Reversão humana
      ↓
Padrão contextual suspenso
      ↓
Casos semelhantes exigem confirmação humana
```

### 9.3 Restauração

A aprovação humana de um caso semelhante não restaura automaticamente a autonomia.

A restauração deverá ser uma decisão explícita.

### 9.4 Simetria de autoridade

O nível necessário para restaurar será o mesmo necessário para reverter:

```text
Gerente reverte → gerente competente restaura
Conselho reverte → Conselho restaura
```

---

## 10. Planejamento prévio obrigatório

Antes de executar qualquer decisão autônoma, a IA deverá produzir registro estruturado contendo, no mínimo:

- objetivo;
- contexto relevante;
- ação escolhida;
- alterações previstas;
- entidades ou estados afetados;
- resultado esperado;
- confiança;
- política que permite autonomia;
- principais evidências;
- justificativa resumida;
- estratégia de reversão;
- etapas de execução, quando aplicável.

Esse planejamento deverá existir antes do início da alteração real.

---

## 11. Explicabilidade

A auditoria deverá permitir compreender posteriormente por que a decisão foi tomada.

Não será necessário armazenar raciocínio interno bruto do modelo.

O registro deverá preservar informações suficientes para reconstruir:

```text
Contexto
   ↓
Evidências
   ↓
Política aplicável
   ↓
Confiança
   ↓
Decisão
   ↓
Planejamento
   ↓
Execução
   ↓
Resultado
```

---

## 12. Visibilidade proporcional

### 12.1 Rotineiras

Decisões comuns poderão ocorrer silenciosamente, permanecendo disponíveis no histórico.

### 12.2 Relevantes

Decisões relevantes gerarão notificação.

### 12.3 Importantes ou críticas

Decisões importantes ou críticas receberão destaque proporcional e não poderão depender exclusivamente de consulta posterior ao histórico.

Autonomia não significa invisibilidade.

---

## 13. Efeito sobre outras pessoas

Uma decisão autônoma não herdará automaticamente autoridade apenas porque foi originada no contexto de um usuário.

Quando afetar diretamente responsabilidade, obrigação, prioridade ou trabalho de outra pessoa, deverão ser avaliados:

- pessoa afetada;
- permissões;
- consentimento quando aplicável;
- autoridade gerencial necessária;
- categoria da decisão.

O documento de decisões autônomas deverá definir explicitamente o alcance humano permitido para cada categoria.

---

## 14. Conflitos entre decisões

Quando duas decisões autônomas forem incompatíveis, o Mheibos aplicará regras determinísticas considerando:

1. criticidade;
2. autoridade;
3. prioridade operacional.

Se a hierarquia produzir resultado inequívoco, a decisão correspondente poderá prevalecer.

Se houver ambiguidade ou conflito não resolvido, a IA não escolherá arbitrariamente. A decisão conflitante será suspensa e encaminhada à autoridade humana competente.

---

## 15. Cadeias de decisões

Uma cadeia poderá permanecer autônoma quando cada decisão concreta que a compõe estiver individualmente autorizada nas condições em que ocorre.

Exemplo:

```text
A → B → C → D
```

Se A, B, C e D forem individualmente elegíveis, a existência da cadeia não cria, por si só, uma exigência adicional de confirmação.

Isso torna indispensável que o catálogo futuro classifique corretamente cada ação.

---

## 16. Confiança

Uma ação prevista no catálogo somente poderá ser executada autonomamente quando a decisão concreta atingir o nível mínimo de confiança aplicável.

Quando a confiança for insuficiente:

```text
Ação elegível para autonomia
          +
Confiança insuficiente
          ↓
Proposta para confirmação humana
```

A IA deverá deixar explícita a incerteza.

Reversibilidade não substitui confiança.

---

## 17. Falhas técnicas e recuperação

### 17.1 Análise do estado

Se ocorrer falha durante uma execução autônoma, a IA avaliará o estado alcançado.

### 17.2 Continuação segura

Se for possível demonstrar que continuar do ponto atual é seguro, consistente e reversível, a execução poderá continuar.

### 17.3 Reinício

Se a continuidade não puder ser garantida, a implementação incompleta deverá ser desfeita e, quando seguro, reiniciada do zero.

### 17.4 Regra de admissibilidade

Se uma falha puder criar estado parcial que não possa ser desfeito com segurança, a ação não é elegível para autonomia e jamais deverá ser iniciada autonomamente.

### 17.5 Auditoria

Deverão permanecer registrados:

- plano;
- início;
- falha;
- estado intermediário relevante;
- análise de recuperação;
- decisão de continuar ou reverter;
- reversão;
- nova tentativa;
- resultado final.

---

## 18. Novas informações durante a execução

Uma decisão autônoma válida não será interrompida apenas porque novas informações surgiram depois de seu início.

Se a decisão era benéfica, autorizada e suficientemente confiável quando tomada, ela deverá ser concluída.

Novas informações serão tratadas como novo estado cognitivo após a decisão:

```text
Estado A
   ↓
Decisão autônoma 1
   ↓
Execução completa
   ↓
Novo estado + novas informações
   ↓
Nova análise
   ↓
Possível decisão autônoma 2
```

Mudança normal da realidade não será confundida com falha técnica.

---

## 19. Concorrência e desempenho computacional

### 19.1 Padrão sequencial

A execução sequencial será o padrão.

### 19.2 Paralelismo permitido

Ações poderão ocorrer em paralelo quando:

- forem independentes;
- não disputarem estados incompatíveis;
- não criarem interferência operacional;
- não prejudicarem de forma relevante o desempenho do computador ou do Mheibos.

### 19.3 Desempenho como critério

Impacto sobre CPU, RAM, GPU, disco, rede e responsividade da aplicação deverá ser considerado na decisão de concorrência.

A independência lógica não basta para justificar paralelismo.

---

## 20. Prioridade do trabalho humano

O trabalho humano interativo terá prioridade sobre cargas autônomas computacionalmente pesadas.

A plataforma poderá configurar limites de uso de:

- CPU;
- RAM;
- GPU;
- disco;
- rede;
- outros recursos relevantes.

A IA deverá reduzir, adiar ou serializar trabalho autônomo quando necessário para preservar a operação humana.

---

## 21. Janelas autorizadas de execução

A configuração poderá estabelecer horários em que ações autônomas, especialmente as pesadas, poderão ser executadas.

Fora da janela:

- ações normais aguardam;
- uma ação muito importante ou prioritária poderá solicitar execução imediata;
- a IA não poderá ignorar a janela por conta própria.

A execução fora da janela dependerá de autorização humana.

---

## 22. Autoridade para exceções de horário

A autorização para executar fora da janela seguirá a classificação da própria decisão.

Exemplos:

- decisão dentro da competência normal do usuário → usuário competente;
- decisão gerencial → gerente;
- decisão colegiada → Conselho de Gerentes.

A exceção de horário não concede autoridade adicional.

---

## 23. Operação autônoma desacompanhada

Durante uma janela previamente autorizada, a IA poderá operar mesmo sem usuários presentes.

A ausência humana não reduz a autonomia já concedida.

Continuarão obrigatórios:

- permissões;
- confiança;
- planejamento;
- reversibilidade;
- segurança;
- regras de conflito;
- limites computacionais;
- janela autorizada;
- auditoria.

---

## 24. Relatório de janela autônoma

Depois de uma janela de execução desacompanhada, o Mheibos deverá gerar relatório consolidado contendo, conforme aplicável:

- o que foi planejado;
- o que foi executado;
- resultados;
- falhas;
- reversões técnicas;
- reinícios;
- estado final.

A visualização respeitará as permissões do usuário.

A leitura do relatório não será, por padrão, bloqueio para utilização do sistema.

---

## 25. Retenção permanente

Registros estruturados de decisões autônomas constituirão histórico auditável permanente.

A operação normal não poderá apagá-los.

A retenção incluirá, conforme aplicável:

- planejamento;
- objetivo;
- contexto;
- evidências;
- confiança;
- autorização normativa;
- execução;
- resultados;
- falhas;
- recuperação;
- reversões humanas;
- restaurações de autonomia;
- autenticações do Conselho.

---

## 26. Ampliação da autonomia

A IA poderá identificar que determinada categoria apresenta:

- aprovações humanas recorrentes;
- bons resultados;
- ausência de reversões;
- confiança consistente;
- baixo risco;
- reversibilidade adequada.

Nesse caso, poderá produzir proposta fundamentada para ampliação da autonomia.

A proposta poderá apresentar histórico, evidências, riscos e resultados.

A IA jamais poderá:

- conceder autonomia a si própria;
- ativar autonomia experimental unilateralmente;
- ultrapassar o teto normativo;
- tratar aprovação recorrente como autorização automática.

---

## 27. Redução voluntária da autonomia

A IA poderá suspender preventivamente sua própria autonomia sobre uma categoria quando concluir que continuar atuando autonomamente não é suficientemente seguro ou confiável.

A suspensão produzirá:

```text
Autonomia ativa
      ↓
Suspensão preventiva pela IA
      ↓
Confirmação humana para novos casos
```

A IA pode reduzir o próprio poder.

Ela não pode restaurá-lo unilateralmente.

A restauração seguirá a governança humana aplicável.

---

## 28. IA cognitiva e automações determinísticas

O Mheibos distinguirá pelo menos:

### 28.1 IA cognitiva

Responsável por análise, interpretação, raciocínio, propostas e demais capacidades dependentes de modelo.

### 28.2 Decisões autônomas da IA

Ações em que a camada cognitiva possui autoridade previamente definida para decidir e executar sem confirmação naquele contexto.

### 28.3 Automações determinísticas

Rotinas do próprio software definidas por regras, como sincronizações, verificações programadas e mecanismos operacionais determinísticos.

Desligar a IA cognitiva não desligará automaticamente as automações determinísticas.

Funções obrigatórias de segurança, integridade, auditoria, sincronização ou outras invariantes do produto não poderão ser desativadas simplesmente por desligar a IA.

Os controles poderão ser separados quando aplicável.

---

## 29. Subordinação normativa absoluta

### 29.1 Regra máxima

A IA deverá cumprir as regras normativas vigentes do Mheibos integralmente.

Nenhum nível de confiança, benefício esperado, urgência, reversibilidade, histórico de sucesso ou autorização humana incompetente poderá justificar desvio.

### 29.2 Condutas proibidas

A IA não poderá:

- violar uma regra;
- ignorar uma regra;
- suspender uma regra por iniciativa própria;
- reinterpretar uma regra para contorná-la;
- criar exceção não prevista;
- decompor uma ação proibida em várias ações permitidas para alcançar o mesmo resultado;
- utilizar ação semelhante, equivalente, indireta ou alternativa para produzir o resultado que a norma pretende impedir;
- manipular sequência, nomenclatura ou forma da ação para ocultar equivalência material;
- obedecer a uma ordem humana que esteja fora da autoridade normativa de quem a emitiu.

### 29.3 Finalidade e efeito

A conformidade não será avaliada apenas pelo nome ou forma técnica da ação.

O Mheibos deverá considerar também:

- finalidade;
- efeito esperado;
- efeito material;
- relação com a proibição;
- tentativa de equivalência funcional.

### 29.4 Proposta de revisão

Se a IA concluir que uma regra está errada, ineficiente ou prejudicial, poderá:

- identificar o problema;
- reunir evidências;
- explicar impactos;
- produzir proposta fundamentada de revisão;
- encaminhá-la à autoridade competente.

Enquanto a norma permanecer vigente, deverá cumpri-la.

### 29.5 Autoridade humana também limitada

Nem usuário, gerente, administrador ou Conselho de Gerentes poderá ordenar à IA que viole norma cuja alteração esteja fora de sua competência.

A governança humana não substitui a hierarquia normativa do Mheibos.

---

## 30. Relação com conhecimento e aprendizado

Feedback, reversões, resultados e padrões poderão alimentar os mecanismos de memória e aprendizado.

Entretanto:

- feedback não altera política automaticamente;
- aprendizado não cria permissão;
- frequência não transforma prática em regra;
- inferência não substitui norma;
- conhecimento emergente não supera conhecimento oficial;
- a IA não pode aprender a contornar uma restrição.

Qualquer promoção de aprendizado para regra ou política deverá seguir a governança normativa aplicável.

---

## 31. Invariantes

A implementação deverá preservar permanentemente as seguintes invariantes:

1. Nenhuma decisão autônoma será irreversível.
2. Nenhuma ação autônoma será iniciada sem planejamento prévio.
3. Nenhuma ação com risco de estado parcial irreversível será elegível para autonomia.
4. A IA nunca ganhará autoridade porque uma autoridade humana está ausente.
5. Urgência aumenta intervenção, não autoridade.
6. A IA poderá reduzir, mas não ampliar unilateralmente, sua própria autonomia.
7. Reversão contextual não expira automaticamente.
8. Restauração de autonomia será explícita e humana.
9. O mesmo nível de autoridade exigido para reversão será exigido para restauração.
10. Toda decisão autônoma será explicável e auditável.
11. Auditoria cognitiva será permanente.
12. Novas informações não invalidam retroativamente uma decisão autônoma válida em execução.
13. Falha técnica e mudança normal de contexto são fenômenos diferentes.
14. O trabalho humano terá prioridade computacional.
15. A janela autorizada não substitui permissões.
16. Operação desacompanhada continuará sujeita às mesmas regras de segurança.
17. Desligar IA não poderá desligar invariantes determinísticas obrigatórias.
18. A IA nunca poderá modificar seu teto normativo.
19. A IA nunca poderá contornar regras por equivalência, decomposição ou interpretação oportunista.
20. Regras foram feitas para serem cumpridas.

---

## 32. Critérios de conformidade

Uma implementação estará em desacordo com esta RFC se permitir qualquer cenário em que:

- a IA execute ação autônoma irreversível;
- uma execução parcial possa produzir consequência não recuperável;
- a IA amplie sua própria autonomia;
- uma autonomia suspensa seja restaurada automaticamente;
- uma reversão colegiada possa ser restaurada por autoridade inferior;
- uma decisão autônoma não possua planejamento e explicação registrados;
- registros de decisões possam ser apagados pela operação normal;
- baixa confiança seja ignorada apenas porque a ação é reversível;
- a IA assuma autoridade ausente;
- urgência permita ultrapassar permissão;
- uma janela de execução seja ignorada unilateralmente;
- paralelismo prejudique de forma relevante o trabalho humano sem necessidade autorizada;
- desligar a IA desative mecanismos determinísticos obrigatórios;
- a IA viole uma regra diretamente;
- a IA contorne uma regra por ação equivalente;
- a IA fragmente uma ação proibida em ações menores para atingir o mesmo objetivo;
- uma ordem humana fora da competência normativa seja tratada como autorização válida.

---

## 33. Síntese normativa

A autonomia da IA do Mheibos não será definida pela ideia de que o modelo “pode fazer o que considerar melhor”.

Ela será uma competência formal, limitada, reversível, planejada, auditável e subordinada à autoridade e às normas.

A arquitetura deverá preservar a seguinte hierarquia:

```text
Normas e invariantes do Mheibos
              ↓
Teto normativo de autonomia
              ↓
Permissões e autoridade humana
              ↓
Política de autonomia da instalação
              ↓
Elegibilidade da categoria
              ↓
Contexto + confiança + recursos + janela
              ↓
Planejamento prévio
              ↓
Decisão autônoma
              ↓
Execução reversível
              ↓
Auditoria permanente
              ↓
Supervisão e reversão humana
```

A IA poderá ser poderosa sem ser soberana.

Poderá agir sem pedir autorização em todas as ocasiões, mas somente porque a autoridade para aquele tipo de ação foi previamente definida.

Poderá aprender com seus resultados, mas aprendizado não lhe concede poder normativo.

Poderá questionar uma regra, mas deverá cumpri-la enquanto estiver vigente.

Poderá sugerir que sua autonomia aumente, mas nunca aumentá-la sozinha.

Poderá voluntariamente se tornar mais conservadora.

E jamais poderá utilizar inteligência, criatividade ou equivalência funcional como mecanismo para escapar das regras que governam o Mheibos.
