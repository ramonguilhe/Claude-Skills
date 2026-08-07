# PROMPT — Onda 6: enquadramento, economia de elevação, bosses, duelo e conquistas

> **Decisões do fundador já tomadas, não reabrir:**
> 1. **Duelo continua contra oponente sintético**, mas refeito de ponta a ponta, com as interfaces TypeScript prontas para ligar backend depois. Nenhum backend, conta ou serviço pago nesta onda.
> 2. **A moeda da loja é a elevação** (metros subidos), lida do app Saúde. Se a leitura confiável não existir no aparelho, o fundador **já autorizou** a alternativa: economia por recompensas (marcos, conquistas, streaks).
> 3. **Ambiente: Mac novo com Xcode e iPhone.** Validação em aparelho físico é exigida.
> 4. Direção visual da `Onda 5B.1` segue aprovada; tema claro e escuro; bibliotecas gratuitas do ecossistema Expo pré-autorizadas.
>
> Registrar as quatro em `docs/DECISIONS.md` na primeira sessão. As regras de honestidade, custo e segurança de `AGENTS.md` e `CLAUDE.md` continuam valendo integralmente.

# OBJETIVO E CRITÉRIO DE SUCESSO

Levar `apps/mobile` de "protótipo bonito com furos" para um app que aguenta uso diário real: nada cortado na tela, campanha longa e variada, duelo que resolve, progresso que rende conquistas e uma economia própria com loja.

Condição de sucesso, verificável por um leitor adversarial:

1. **Enquadramento zero-defeito.** Nenhum texto, número, ícone ou controle cortado, sobreposto ou escondido em nenhuma tela, nas larguras 320, 375, 390, 393 e 430pt, nos dois temas, com Dynamic Type padrão e ampliado. Provado por screenshots dessa matriz e por revisão no iPhone físico.
2. **Campanha recalibrada.** Primeiro boss com 10.000 de vida, curva crescente até o último, com tabela de progressão publicada mostrando dias estimados em três perfis de usuário. Nenhum boss matematicamente indeflagrável para quem bate a meta — provado por simulação versionada.
3. **≥ 12 mecânicas de boss distintas**, declarativas, compostas em até três por boss, cada uma com regra testada, explicação honesta em pt-BR na interface e simulação de balanceamento.
4. **Arte plugável.** Todo boss e o boss global renderizam hoje um placeholder identificável por cor e forma, e aceitam a arte definitiva depois trocando um arquivo, sem migração de dados e sem tocar em código de domínio. Convenção documentada e testada.
5. **Duelo resolve sempre.** Ao fim do prazo há vencedor, placar final, variação de Elo, recompensa, registro no histórico e notificação — inclusive quando o app estava fechado no instante do fim. Nunca existe duelo em limbo. Interface refeita, com percepção clara de disputa.
6. **Conquistas e perfil.** Motor de conquistas idempotente, selos no perfil e perfil completo com estatísticas reais. Nenhuma conquista concedida duas vezes, nenhuma perdida em migração.
7. **Loja e economia.** Moeda definida, fonte verificada no aparelho, loja funcionando, e `docs/product/ECONOMIA.md` provando com números que a campanha é vencível sem gastar nada e que quem gasta o máximo avança no máximo 30% mais rápido.
8. **Notificações locais** opt-in, por tipo, com janela de silêncio e teto diário, validadas no iPhone.
9. `npm run check` verde, bundle medido antes e depois, zero regressão em passos, saúde, dano, campanha e ranking. Migração de estado preserva todo o progresso existente.

# CONTEXTO E INSUMOS

## Ambiente novo — ler antes de qualquer coisa

O fundador trocou de Mac. **O que existe é o repositório no GitHub**, `ramonguilhe/step-boss-app` (privado). Consequências que economizam muito tempo se você tratar já no começo:

- Clonar do GitHub e rodar `npm ci` em `apps/mobile`. Não procurar nada em `/Users/ramon/Documents/App_passos`.
- **O contrato antigo `/Users/ramon/Documents/Otimização Code/PROMPT_MESTRE_APP_JORNADA_POR_PASSOS.md` não existe neste Mac e não está no repositório.** Não bloquear por causa dele, não tentar reconstruí-lo. Ele foi substituído pelos prompts desta série; registrar isso em `DECISIONS.md`.
- `graphify-out/`, `.serena/`, `.env`, `ios/`, `android/` e `node_modules/` são ignorados pelo Git e **não vieram**. Reconstruir o que for necessário: `graphify update .` (instalar o CLI se faltar), `npx expo prebuild` para o build nativo, `.env` a partir de `.env.example` se houver. Não recriar `.serena/`.
- Arquivos que só existiam no Mac antigo (ZIPs de upload, `~/Desktop/duplicatas-app-passos/`) estão perdidos e são irrelevantes. Não procurar.
- **Corrigir os caminhos absolutos obsoletos** em `AGENTS.md`, `CLAUDE.md`, `docs/AGENT_HANDOFF.md` e onde mais aparecerem, trocando por caminhos relativos ao repositório. Um agente futuro não pode voltar a travar nisso.

Depois disso, o portão normal: `AGENTS.md`, `docs/PROJECT_BRIEF.md`, `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/AGENT_HANDOFF.md`, `docs/WORK_QUEUE.md`, mais `git status --short` e `git log -1 --oneline`. Reivindicar a tarefa em `WORK_QUEUE.md` antes de editar.

## Defeitos já observados na tela Hoje, em iPhone real

Tratar como evidência, não como hipótese. A captura do fundador mostra, numa única tela:

- o cabeçalho passa **por baixo da barra de status** — o relógio do sistema cobre "HOJE · ATIVIDADE REAL" e a data; "Sincronizado" e o horário de sincronização colidem com os ícones de bateria e sinal;
- o número grande `3.643` está **cortado em cima e embaixo** — altura de linha menor que a caixa do glifo;
- o cartão do obstáculo é **cortado no meio da frase** ("A batalha aparece como…") e o resto fica **atrás da barra de abas**, sem afordância de rolagem;
- a frase "Refrigerante de Todo Dia já perdeu 0 de vida" é uma construção ruim em português;
- o ícone da aba **Duelo é um "X"**, que o usuário lê como fechar ou cancelar;
- o modelo de reserva é incompreensível na tela: passos hoje 3.643, "+106 nesta sincronização", reservas de 40.713 e 22.642, e "Dano hoje: 0". Um usuário não consegue ligar esses números.

Esses são sintomas de regras ausentes, não erros isolados. Corrigir a regra, depois a tela.

## Stack

Expo SDK 57, React Native 0.86, TypeScript. Ler a documentação exata do SDK 57 antes de alterar API Expo. Domínio validado que não pode regredir: leitura e reconciliação de passos (`src/domain/steps.ts`, `src/health/*`). App inteiramente em pt-BR via i18n, sem texto hardcoded.

# ESCOPO E RESTRIÇÕES

- **Sem backend, conta, billing ou serviço pago.** Tudo local. Duelo, ranking e boss global continuam com dados sintéticos **rotulados como simulação** na própria tela, com contratos TypeScript prontos para servidor.
- **Nada de estética de jogo ou RPG**: sem pixel art, moldura de fantasia, avatar de personagem, HUD, XP, mana, guilda, loot. Vocabulário permitido: passos, elevação, dano, vida do boss, duelo, ranking, temporada, conquista, selo, impulso. Referência é app de saúde premium.
- **Powerups nunca são obrigatórios.** Aceleram, não destravam. Nenhuma compra com dinheiro real nesta onda.
- **Dados de saúde não saem do aparelho.**
- Sem secrets, sem automação persistente (hook/watch), sem publicar, sem DNS.
- Toda alteração de regra de dano, economia ou saúde é isolada em commit próprio e justificada no relatório.

# EXECUÇÃO

## Ferramentas e economia de tokens

- **Graphify**: reconstruir o índice logo após o clone (`graphify update .`); depois usar `query`, `explain` e `path` antes de qualquer mudança transversal ou pergunta ampla de arquitetura, no lugar de grep amplo. Nunca `extract`, `label`, hooks ou watch. Confirmar no código conclusões vindas de aresta `INFERRED` ou `AMBIGUOUS`.
- **Xcode**: extensão do Claude no Xcode para prebuild, compilar, instalar e diagnosticar. Enquadramento, háptico, notificação e fluidez de animação **só contam como validados no iPhone físico**.
- **Skills**: usar as skills de criação e design de app disponíveis. Procurar e **instalar as gratuitas e locais que ajudem (design mobile/HIG, acessibilidade, UX writing, visualização de dados para os gráficos de estatística) — pré-autorizado pelo fundador**. Skill paga ou com automação persistente exige pergunta antes.
- **Delegação de modelos** (orquestrador em Fable): reservar Fable para economia, balanceamento, arquitetura de estado e revisão final. Delegar com objetivo, saída esperada, ferramentas permitidas e limite de escopo:
  - **Sonnet**: telas, componentes, motor de conquistas, refatoração, testes, scripts de simulação.
  - **Haiku**: inventários e varreduras mecânicas (fichas de boss a partir do schema, chaves i18n, caça a cor literal, `fontSize` cru, altura fixa em container de texto, alvo <44pt).
  Subagente não integra sozinho; o orquestrador revisa com contexto fresco.
- Ler sob demanda; comprimir logs e listagens; preservar literal apenas erro difícil, diff, contrato e evidência.

## Fase 0 — Reancorar o ambiente

Clonar, instalar, rodar `npm run check` para estabelecer a linha de base, reconstruir o Graphify, fazer `prebuild`, compilar e instalar no iPhone **antes de mudar qualquer coisa**. Registrar o estado inicial: testes passando, tamanho do bundle, versão do Expo, resultado do `expo-doctor`. Corrigir os caminhos obsoletos da documentação. Commit próprio.

## Fase 1 — Enquadramento (prioridade máxima)

Instituir regras, não remendos por tela:

- **Safe area obrigatória.** Um container de tela único que aplica `useSafeAreaInsets`; nenhum cabeçalho desenha sob a barra de status; nenhum conteúdo interativo fica sob a barra de abas. Rolagem sempre com `contentContainerStyle` reservando `insets.bottom + altura da tab bar + espaçamento`.
- **Tipografia que não corta.** Para todo papel tipográfico, `lineHeight` explícito ≥ 1,05 × `fontSize`; `includeFontPadding: false` no Android; nunca altura fixa em container de texto. Números de display usam ajuste medido para caber (redução até um piso definido), de modo que sete dígitos ainda entrem em 320pt.
- **Truncamento é decisão, não acidente.** `numberOfLines` só onde a truncagem é intencional, sempre com reticências e com o texto completo acessível. Texto de conteúdo quebra e rola.
- **Afordância de rolagem.** Nenhuma tela pode terminar num corte que pareça o fim do conteúdo.
- **Matriz de conteúdo extremo** como fixture: 0 passos, 99.999 passos, 999.999 de reserva, nome de perfil longo, nome de boss longo, descrição longa, ranking com empate, e a virada de dia com a tela aberta.
- **Ícones com semântica correta.** Trocar o "X" da aba Duelo por um símbolo que signifique confronto. Revisar todos os ícones pelo mesmo critério.
- **Clareza do modelo de reserva.** Ou a interface passa a explicar em uma frase de onde vem cada número (passos → reserva → dano, e por que "Dano hoje" pode ser 0), ou o modelo é simplificado até ser autoexplicativo. Escolher, justificar em uma linha e implementar.
- **Varredura de copy** em todas as telas: frases como "já perdeu 0 de vida" reescritas na voz pt-BR do projeto.

Verificação: screenshots em 320/375/390/393/430, dois temas, Dynamic Type padrão e ampliado, mais revisão no iPhone. Uma regra de lint que falhe em altura fixa de container de texto e em `fontSize` sem `lineHeight`.

## Fase 2 — Fonte da moeda e economia

**Spike primeiro, desenho depois.** No iPhone físico, verificar o que o wrapper HealthKit realmente entrega como **total diário**:

1. elevação ascendida em metros, se existir como agregado diário;
2. senão, `flightsClimbed` (andares subidos), convertido pela razão da Apple de 1 andar ≈ 3,048 m, e rotulado na interface como estimativa a partir de andares;
3. senão, acionar a alternativa já autorizada: economia por recompensas.

Registrar o resultado com evidência (número lido no app versus número no app Saúde) em `docs/DECISIONS.md`. Não desenhar a economia antes desse veredito.

Depois, `docs/product/ECONOMIA.md` com números, não adjetivos:

- nome da moeda em pt-BR, curto, sem jargão de jogo;
- taxa de ganho em três perfis reais — **terreno plano com elevador (perto de zero)**, rotina urbana com escadas, pessoa muito ativa;
- **piso garantido**: como quem não sobe nada mesmo assim participa da loja. Sem isso a loja exclui usuários, e isso é requisito, não sugestão;
- teto diário anti-inflação e anti-contador inflado;
- custo de cada powerup e tempo de acumulação por perfil;
- simulação de 30 e 90 dias com saldo e poder de compra;
- prova de que a campanha é vencível gastando zero e que o gasto máximo acelera no máximo 30%.

Separação conceitual a preservar e a deixar explícita na interface: **passos são dano; elevação é moeda.** São coisas diferentes e nunca se convertem uma na outra.

## Fase 3 — Bosses: vida, mecânicas e arte plugável

**Vida.** Primeiro boss 10.000. Curva crescente por posição e por arco, publicada em tabela com dias estimados nos três perfis. Se a campanha inteira passar de um horizonte razoável, recalibrar a curva antes de seguir — e apresentar a tabela no relatório.

**Mecânicas** (mínimo 12, declarativas no schema, interpretadas pelo domínio, compostas em até três por boss). Implementar pelo menos estas e propor outras:

regeneração em dia sem meta; blindagem que só cai com condição cumprida; camada de escudo que ignora dano bônus; imunidade a bônus (só passos reais); janela de vulnerabilidade com dano dobrado em faixa horária; contra-ataque que devolve dano se o dia fechar abaixo de um limiar; vida que infla a cada dia sem ataque; teto de dano diário, forçando consistência em vez de um único dia enorme; piso de dano diário, ignorando esforço simbólico; fases que mudam o comportamento ao cruzar 50% e 25%; enfraquecimento progressivo por streak de metas batidas; adaptação à média dos últimos 7 dias do próprio usuário; névoa que esconde a vida restante até 25%; vínculo entre dois bosses do mesmo arco.

Cada mecânica precisa de: regra pura testada, texto honesto em pt-BR explicando ao usuário o que está acontecendo e por quê, e simulação provando que não trava o progresso de quem cumpre a meta.

**Arte plugável.** Campo de arte por boss resolvido em um registro explícito (`require` não aceita caminho dinâmico em React Native). Enquanto não houver arte, renderizar um placeholder compartilhado tingido pelo token de cor do boss e marcado pela inicial ou forma do arco, de modo que os bosses já pareçam distintos. Documentar a convenção de entrega — caminho, nome derivado do id, dimensão, proporção, margem segura, legibilidade nos dois temas — e cobrir com teste que todo id resolve sem quebrar. Mesmo mecanismo para o boss global, por temporada.

## Fase 4 — Boss derrotado

Sequência: impacto final, flash, o boss desaturar e sair, selo de conquista entrando, recompensa contando, chamada para o próximo. Total ≤ 2,5s, pulável por toque, háptico de sucesso, e sob Reduce Motion vira transição curta sem perder a informação. Estados de vitória também para o boss global e para o fim de temporada.

## Fase 5 — Conquistas, selos e perfil

Motor declarativo, avaliado em mudança de estado, **idempotente** (nunca concede duas vezes), persistido com data de desbloqueio, e resistente a migração. Famílias: volume, consistência, campanha, duelo, contribuição global, superação de recorde pessoal, exploração do app. Cada conquista com nome pt-BR, critério visível, progresso parcial e recompensa.

Perfil completo: nome editável, meta diária ajustável, total de passos, média diária, melhor dia, streak atual e maior, elevação acumulada, bosses derrotados por arco, histórico de duelos, Elo com faixa nomeada, contribuição no boss global, vitrine de selos, gráficos de semana e mês, preferências de notificação, privacidade explicando que os dados ficam no aparelho, **exportar e importar o progresso** (o fundador acabou de trocar de máquina; o usuário também troca de telefone), idioma e versão.

## Fase 6 — Loja de powerups

Loja com moeda da Fase 2. Catálogo sugerido, a calibrar pela economia: multiplicador de dano por 24h; proteção de streak; revelar vida oculta; quebrar blindagem; dobrar a reserva do dia; refazer o pareamento do duelo; anular um contra-ataque; ampliar o teto diário; segunda chance no duelo. Cada item com efeito determinístico, duração explícita, teto de acúmulo, confirmação antes de gastar e registro no histórico. Nada de aleatoriedade paga, caixa surpresa ou mecânica de sorte.

## Fase 7 — Duelo refeito

O defeito central é que o prazo acaba e nada acontece. Corrigir a regra antes da tela:

- **Resolução determinística e retroativa**: ao abrir o app, todo duelo com prazo vencido é resolvido na hora, com vencedor, placar final, variação de Elo, recompensa, entrada no histórico e notificação. Estado `resolvido` persistido. Nunca há limbo.
- **Percepção de disputa**: placar lado a lado ao vivo, diferença em destaque ("você está X passos à frente"), tempo restante proeminente, marcos da virada, e estados distintos para aguardando, em andamento, últimas horas e resolvido.
- **Oponente sintético crível e honesto**: perfil de atividade com variação diária realista, não uma reta; rótulo de simulação permanente, sem nunca fingir ser pessoa.
- **Pareamento justo** por faixa de média de passos, não por Elo puro — senão o usuário sedentário perde sempre e abandona.
- Histórico, sequência de vitórias, faixas de Elo nomeadas em pt-BR, revanche.
- Interface inteira refeita dentro do sistema de design.

## Fase 8 — Notificações locais

`expo-notifications`, **somente locais** — sem servidor push. Eventos: meta batida; falta pouco para a meta no fim do dia; boss quase derrotado; duelo entrando nas últimas horas; duelo resolvido; streak em risco; conquista desbloqueada; nova temporada do boss global. Regras: opt-in explícito no momento certo, não no primeiro lançamento; preferências por tipo; teto diário; janela de silêncio noturna; nunca notificar o mesmo evento duas vezes; texto pt-BR que convida, sem culpa nem alarme. Registrar a limitação honesta: sem backend, o agendamento depende do app; não há push real.

## Fase 9 — Saúde do código e desempenho

Varredura e correção: erros de tipo e `any` desnecessário; promessa sem tratamento; ausência de error boundary; lista sem `keyExtractor` ou com re-render evitável; memoização onde há custo medido, não por reflexo; chave de i18n órfã ou faltando; código morto; dependência não usada; migração de estado (para a nova versão) com teste que prova preservação de progresso, conquistas e carteira. Medir bundle e tempo até interativo antes e depois, e reportar a diferença.

## Fase 10 — Fechamento

Screenshots antes/depois da matriz completa, build instalado no iPhone com veredito escrito, atualização de `PROGRESS.md`, `DECISIONS.md`, `AGENT_HANDOFF.md` e `WORK_QUEUE.md`, relatório final.

# EVIDÊNCIA E VALIDAÇÃO

- `npm run check` verde a cada fase; testes novos para mecânicas de boss, curva de vida, motor de conquistas (incluindo idempotência), resolução retroativa de duelo, economia e migração de estado.
- Simulações versionadas em `docs/product/`: progressão da campanha por perfil, balanceamento das mecânicas, acumulação de moeda em 30 e 90 dias.
- Playwright sobre `npm run export:web`: cada tela em 320/375/390/393/430, dois temas, Dynamic Type padrão e ampliado, Reduce Motion ligado e desligado, com a matriz de conteúdo extremo. Console sem erro. Screenshots em `docs/design/reviews/<data>/`.
- iPhone físico via extensão do Xcode: enquadramento real, leitura de elevação comparada ao app Saúde, háptico, notificação disparando, fluidez das animações, legibilidade sob luz forte.
- Toda afirmação importante com evidência rastreável: arquivo, teste, saída de comando, screenshot ou número medido. Relatório sem evidência não conta como execução.

# FORMATO DE ENTREGA

- Commits atômicos por fase.
- Documentos: `docs/product/ECONOMIA.md`, `docs/product/BALANCEAMENTO_BOSSES.md`, `docs/design/ARTE_BOSSES.md` (convenção de entrega da arte), `docs/design/AUDITORIA_ENQUADRAMENTO.md`, atualização de `DESIGN_SYSTEM.md`.
- Relatório final com os quatro estados — `concluído`, `parcial`, `simulado`, `não validado` — mais lista numerada das adições feitas por iniciativa própria, para o fundador aprovar ou eliminar, e lista do que continua pendente de backend.
- Todo texto de UI em pt-BR via i18n.

# CONDIÇÕES DE PARADA E ESCALAÇÃO

- Prosseguir sem perguntar em tudo que for local, gratuito e reversível — inclusive decisões de design, copy, mecânica, balanceamento e features novas.
- Parar e perguntar somente para: qualquer serviço pago, backend, conta ou telemetria; enviar dado de saúde para fora do aparelho; publicar, alterar DNS ou lojas; apagar dado do aparelho ou histórico Git; conflito direto com decisão registrada em `DECISIONS.md`.
- Se o spike de elevação falhar, **não parar**: acionar a alternativa por recompensas já autorizada, registrar a decisão com a evidência e seguir.
- O retorno é definido pela condição de sucesso e suas evidências, nunca por confiança ou volume de texto. Se bloqueado: reportar bloqueio, evidência e a menor próxima ação segura.

# RESULTADOS QUE NÃO CONTAM COMO SUCESSO

- Qualquer tela ainda cortando texto, número ou controle em qualquer largura da matriz.
- Economia desenhada sobre uma fonte de elevação que não foi verificada no aparelho.
- Loja inacessível para quem vive em terreno plano.
- Mecânica de boss sem simulação de balanceamento, ou que trave o progresso de quem bate a meta.
- Boss ou boss global sem placeholder resolvido, ou arte que exija mudança de código para ser trocada.
- Duelo que ainda possa terminar sem resolução, ou que só resolva com o app aberto no instante exato.
- Conquista concedida duas vezes, perdida na migração, ou sem critério visível.
- Notificação sem opt-in, sem teto diário ou disparando de madrugada.
- Powerup obrigatório para vencer, ou com resultado aleatório.
- Interface com estética de jogo ou RPG.
- Enquadramento, háptico ou notificação declarados validados a partir de simulador ou web.
- `npm run check` vermelho, ou regressão em passos, saúde, dano, campanha e ranking.

# FALHAS A AUDITAR

- Safe area aplicada em algumas telas e esquecida em outras; conteúdo sob Dynamic Island ou sob a tab bar.
- Altura de linha menor que a caixa do glifo em número de display; dígito trocando de largura por falta de `tabular-nums`.
- Container de texto com altura fixa; `numberOfLines` em label crítico.
- Conversão de andares para metros aplicada com fator errado, ou apresentada como medida exata quando é estimativa.
- Moeda inflacionando por contador de passos manipulado, ou teto diário ausente.
- Curva de vida que torna a campanha longa demais para ser terminada, ou curta demais para ter graça.
- Duas mecânicas compostas que se multiplicam e travam o boss.
- Registro de arte com id divergente do id do boss, quebrando em silêncio.
- Resolução de duelo dependente do relógio do dispositivo sem tratar mudança de fuso ou de hora.
- Conquista avaliada em render em vez de em mudança de estado, gerando concessão duplicada.
- Notificação reagendada a cada abertura, empilhando avisos.
- Migração de estado que zera carteira, conquistas ou progresso de campanha.
- Animação na thread de JS causando engasgo; Reduce Motion ignorado ou obedecido a ponto de sumir com o feedback de toque.
- Caminho absoluto do Mac antigo reintroduzido na documentação.
- Queima de tokens por leitura ampla onde `graphify query`/`explain` bastava.
- Subagente saindo do escopo delegado ou integrando sem revisão do orquestrador.

# ESTADO E HANDOFF

Ao fim de cada sessão: atualizar `PROGRESS.md` e `DECISIONS.md` se houve mudança de estado ou decisão; registrar em `AGENT_HANDOFF.md` um estado pequeno e factual — decisões tomadas, arquivos alterados, validações executadas, screenshots geradas, resultado do spike de elevação, pendências e próximo passo; atualizar a posse em `WORK_QUEUE.md`; commit atômico. Nunca depender da memória implícita da conversa.
