# PROMPT — Auditoria e elevação de design do app de passos (Onda de acabamento, 2026-07-23)

> **Decisões do fundador já tomadas, não reabrir:** (1) a direção visual da galeria `Onda 5B.1` está **aprovada** — portar para o app e refinar a partir dela, não redesenhar do zero; (2) instalar bibliotecas **gratuitas do ecossistema Expo** para motion, gesto, fonte e háptico está **pré-autorizado**; (3) o app tem **tema claro e escuro**, com contraste validado nos dois. Registrar as três em `docs/DECISIONS.md` na primeira sessão.
>
> As regras de honestidade, custo e segurança de `AGENTS.md` e `CLAUDE.md` continuam valendo integralmente.

# OBJETIVO E CRITÉRIO DE SUCESSO

Elevar `apps/mobile` do nível "funciona" para o nível "parece um app de saúde comercial no iPhone", tratando design como sistema — tipografia, cor, forma, espaço, movimento e acessibilidade — e não como ajuste solto de tela.

Condição de sucesso, verificável por um leitor adversarial:

1. Existe um sistema de design aplicado, não apenas documentado: **zero** cores literais, tamanhos de fonte, raios, espaçamentos e durações hardcoded fora dos tokens em `src/**` (verificado por lint ou script que falha o build).
2. `npm run check:contrast` (novo) calcula o contraste WCAG 2.1 de **todos** os pares de cor em uso, nos dois temas, e falha se algum violar: 4.5:1 para texto normal, 3:1 para texto grande e para bordas/ícones que carregam estado. Relatório em tabela versionado.
3. Toda tela e todo overlay passam na auditoria tela a tela definida abaixo, com os estados obrigatórios implementados: carregando, vazio, erro, permissão negada, primeiro uso e valores extremos.
4. Todo elemento interativo tem os cinco estados (repouso, pressionado, desabilitado, carregando, foco de VoiceOver), alvo de toque ≥44×44pt e feedback de movimento coerente com o vocabulário de motion definido.
5. Dynamic Type até XXL sem texto cortado, sobreposto ou truncado em label crítico; VoiceOver percorre cada tela em ordem lógica com rótulos em português.
6. `AccessibilityInfo.isReduceMotionEnabled` é honrado de verdade no app — não só no toggle da galeria.
7. Screenshots antes/depois de cada tela em 390×844 e 430×932, nos dois temas, versionadas; e o build instalado no iPhone físico via extensão do Claude no Xcode, com motion e háptico avaliados no aparelho.
8. `npm run check` verde. Nenhuma regressão em passos, saúde, dano, campanha ou ranking.

# CONTEXTO E INSUMOS

- Portão de leitura obrigatório, nesta ordem: `AGENTS.md`, `docs/PROJECT_BRIEF.md`, `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/AGENT_HANDOFF.md`, `docs/WORK_QUEUE.md`; depois `git status --short` e `git log -1 --oneline`. Reivindicar a tarefa em `WORK_QUEUE.md` antes de editar.
- **Galeria `Onda 5B.1`** (HTML/CSS/JS local, aprovada): superfícies `Hoje`, `Campanha`, `Global`, `Duelo 5B.2` (a versão válida — `Duelo rejeitado` é histórico, ignorar), `Você`, storyboard `Ataque`, estados de `Boss`, `Antes/depois` e `Notas`; referências de tela 390×844 e 430×932; toggle de Reduce Motion. Ler o CSS da galeria como fonte de intenção visual e extrair dele os tokens reais, em vez de reinventar valores.
- Stack: Expo SDK 57, React Native 0.86, TypeScript. Ler a documentação exata do SDK 57 antes de alterar API Expo.
- Domínio validado que **não pode regredir**: leitura e reconciliação de passos (`src/domain/steps.ts`, `src/health/*`), HealthKit aprovado em iPhone físico.
- App inteiramente em pt-BR via i18n. Nenhum texto novo hardcoded; toda mudança de copy entra como chave.

# ESCOPO E RESTRIÇÕES

- **Foco é design e experiência.** Regra de negócio, economia de dano, catálogo de bosses e integração de saúde só mudam quando a experiência exigir (por exemplo: um estado de carregamento precisa de um campo de estado). Toda mudança de comportamento entra no relatório final, isolada e justificada.
- **Nada de estética de jogo ou RPG**: sem pixel art, moldura de fantasia, avatar de personagem, HUD de jogo, XP, mana, guilda ou loot. Referência é app de saúde/fitness premium: dado em primeiro plano, tipografia forte, superfície calma.
- **Dependências permitidas** (gratuitas, sem serviço externo): `react-native-reanimated`, `react-native-gesture-handler`, `expo-haptics`, `expo-font`, `react-native-safe-area-context`, ícones vetoriais do ecossistema Expo. Cada instalação registrada com a razão. Nada pago, nada com backend, nada com telemetria.
- Sem secrets, sem automação persistente (hook/watch), sem publicar, sem DNS, sem cobrança.
- No máximo **duas famílias tipográficas** e **quatro pesos** no app inteiro.

# EXECUÇÃO

## Ferramentas e economia de tokens

- **Graphify**: `graphify update .` no início da sessão. Antes de tocar em qualquer componente compartilhado (`src/ui/*`), usar `graphify query`/`explain`/`path` para levantar todos os consumidores, em vez de grep amplo. Nunca usar `extract`, `label`, hooks ou watch. Confirmar no código conclusões vindas de aresta `INFERRED` ou `AMBIGUOUS`.
- **Xcode**: extensão do Claude no Xcode para compilar, instalar no iPhone e diagnosticar build. Motion e háptico **só contam como validados no aparelho físico** — simulador não reproduz háptico e mente sobre performance de animação.
- **Skills**: usar as skills de design já disponíveis. Antes da Fase 1, procurar nos marketplaces skills de design mobile/iOS (Human Interface Guidelines, acessibilidade, UX writing, sistema de design) e **instalar as gratuitas e locais — pré-autorizado pelo fundador**. Skill paga ou que instale automação persistente exige pergunta antes.
- **Delegação de modelos** (orquestrador em Fable): reservar Fable para as decisões de sistema (tipografia, cor, motion), a auditoria crítica e a revisão final. Delegar com objetivo, saída esperada, ferramentas permitidas e limite de escopo:
  - **Sonnet**: aplicar tokens nas telas, refatorar componentes para os cinco estados, escrever testes e o script de contraste.
  - **Haiku**: varreduras mecânicas e inventários tabulares — encontrar cor literal, `fontSize` numérico, `borderRadius` cru, `numberOfLines` em label crítico, alvo <44pt, texto fora do i18n.
  O orquestrador revisa com contexto fresco antes de integrar; subagente não integra sozinho.
- Ler sob demanda, comprimir logs e listagens; preservar literal apenas erro difícil, diff, contrato e evidência.

## Fase 1 — Extrair e fechar o sistema de design

Produzir `docs/design/DESIGN_SYSTEM.md` e os tokens em código, derivados da galeria 5B.1.

**Tipografia.** Escolher a família e justificar em uma linha (padrão recomendado: fonte do sistema para UI, o que garante Dynamic Type e legibilidade; família própria só para o contador, se a galeria pedir). Definir uma escala com papéis nomeados — contador/display, título de tela, título de seção, corpo, corpo forte, legenda, rótulo, numérico — e para cada papel: tamanho, peso, altura de linha, tracking e o **limite máximo de escala sob Dynamic Type**. Todo número que muda (contador de passos, vida do boss, dano, cronômetro do duelo, posição no ranking) usa `fontVariant: ['tabular-nums']`; sem isso o número treme a cada atualização. Blocos de texto entre 45 e 75 caracteres por linha.

**Cor.** Tokens **semânticos**, nunca literais: `texto/primario`, `texto/secundario`, `texto/terciario`, `fundo/base`, `fundo/elevado`, `borda/sutil`, `borda/forte`, `acento`, `perigo`, `sucesso`, `aviso`, `boss/vida`, `dano/real`, `dano/bonus`. Cada token com par claro/escuro. Cor nunca é o único portador de informação — a diferença entre dano real e bônus precisa de rótulo ou forma, não só matiz. Verificar os pares que carregam significado contra deuteranopia e protanopia.

**Forma e linha.** Escala de raio com quatro níveis mais `pill`; raio aninhado segue `interno = externo − padding`. Espessuras: `hairlineWidth` para divisor, 1pt para contorno de card, 2pt para foco e seleção. Divisor com recuo alinhado ao conteúdo quando há ícone ou avatar à esquerda, nunca de borda a borda. Elevação no iOS por contraste de superfície mais borda sutil; se houver sombra, uma escala de três níveis com fonte de luz única. Proibido acumular borda + sombra + fundo distinto no mesmo elemento.

**Espaço e área visível.** Grade de 4pt com espaçamentos nomeados. `useSafeAreaInsets` em toda tela: Dynamic Island no topo, indicador de home embaixo, nada interativo sob a tab bar. Alvo de toque ≥44×44pt sempre, com `hitSlop` quando o visual for menor; ≥8pt entre alvos adjacentes. Definir por tela o que precisa estar **acima da dobra** e garantir afordância de rolagem — nunca cortar conteúdo num limite que pareça o fim da tela.

**Motion.** Vocabulário fechado de duração: 100ms para press, 200ms para mudança de estado e fade, 300ms para transição de tela e sheet, 500ms+ só para celebração de boss derrotado. Curvas: `easeOut` na entrada, `easeIn` na saída, spring com damping e stiffness tokenizados para movimento que desloca posição. Animar apenas `transform` e `opacity`, na thread de UI (Reanimated); nunca animar `width`, `height` ou `margin` dentro de lista. Nunca animar layout que empurre conteúdo sob o dedo do usuário.

**Háptico.** Mapa fechado: seleção de aba ou opção = `selection`; confirmação de ação = `impact light`; boss derrotado ou conquista = `notification success`; erro ou permissão negada = `notification error`. Proibido háptico em rolagem ou em evento repetitivo.

## Fase 2 — Biblioteca de componentes

Padronizar, cada um com os cinco estados (repouso, pressionado, desabilitado, carregando, foco de VoiceOver): botão primário/secundário/terciário/destrutivo em três tamanhos (48–52pt, 44pt, 36pt com `hitSlop`); campo de texto; card; barra de vida do boss; contador de passos; linha de lista e linha de ranking; tabs; chip de filtro; sheet e modal; toast; badge; anel ou barra de meta; skeleton; estado vazio; estado de erro; banner de permissão.

Regras de botão: no máximo **um** primário por tela; o desabilitado permanece legível (≥3:1) e explica por que está desabilitado quando não for óbvio; o press combina escala 0.96–0.98, mudança de superfície e háptico em spring curto — nunca apenas `opacity`; o botão de ação principal respeita a margem lateral, sem colar nas bordas.

## Fase 3 — Auditoria tela a tela

Telas: pré-cadastro completo (todas as etapas, incluindo permissão negada e adiada), `Hoje`, `Campanha`, `Global`, `Duelo`, `Você`, mais todos os overlays. Para **cada** uma, percorrer e corrigir: hierarquia visual (o primeiro elemento que o olho encontra é o mais importante da tela); densidade e ritmo vertical; alinhamento óptico; consistência de espaçamento; comportamento de header ao rolar; clareza da ação primária; texto na voz pt-BR, sem jargão de desenvolvedor; os seis estados obrigatórios; motion; contraste nos dois temas; alvos de toque; safe area.

Casos-limite obrigatórios em cada tela que exibe dado: 0 passos, 99.999 passos, nome de perfil muito longo, boss com 1 de vida, ranking com empate, lista vazia, e a virada de dia ocorrendo com a tela aberta.

## Fase 4 — Movimento aplicado

Implementar, cada um respeitando Reduce Motion: feedback de toque em todo interativo; transição entre abas e telas; entrada de conteúdo com stagger curto (no máximo três itens, nunca a lista inteira); contador de passos e de dano animando por contagem, não por salto; barra de vida do boss drenando com easing; flash de dano; celebração ao derrotar boss; skeleton no carregamento em vez de spinner solto; pull-to-refresh. Sob Reduce Motion, transformação e paralaxe viram crossfade curto ou estado imediato — mas o **feedback de estado nunca desaparece**, porque sem ele o usuário não sabe se o toque registrou.

## Fase 5 — Acessibilidade

`accessibilityLabel`, `accessibilityRole`, `accessibilityHint` e `accessibilityState` em todo interativo; agrupamento com `accessible` onde a leitura elemento a elemento for ruidosa; ordem de foco lógica; `announceForAccessibility` em ataque registrado e boss derrotado. Dynamic Type até XXL sem altura fixa em container de texto e sem `numberOfLines={1}` em label crítico. Honrar Reduce Transparency e Increase Contrast se houver blur.

## Fase 6 — Fechamento

Screenshots antes/depois de cada tela, build físico via Xcode, atualização de `PROGRESS.md`, `DECISIONS.md`, `AGENT_HANDOFF.md` e `WORK_QUEUE.md`, relatório final.

# EVIDÊNCIA E VALIDAÇÃO

- `npm run check` verde a cada fase.
- `npm run check:contrast` novo: calcula WCAG 2.1 sobre os tokens reais em uso, nos dois temas, falha o build em violação e emite a tabela completa para `docs/design/CONTRASTE.md`. Contraste **medido**, nunca estimado a olho.
- Lint ou script que falha ao encontrar cor literal, `fontSize` numérico, `borderRadius` cru, espaçamento fora da grade ou duração de animação hardcoded em `src/**`.
- Playwright sobre `npm run export:web`: cada tela em 390×844 e 430×932, tema claro e escuro, Dynamic Type padrão e ampliado, Reduce Motion ligado e desligado. Console sem erro. Screenshots em `docs/design/reviews/<data>/`.
- Testes: escala tipográfica, mapa de tokens, cálculo de contraste, e um teste por componente garantindo os cinco estados.
- Build físico no iPhone pela extensão do Xcode, com veredito escrito sobre fluidez de animação, acerto do háptico e legibilidade sob luz forte. O que só passou na web permanece `não validado` para nativo.
- Toda afirmação importante com evidência rastreável: arquivo, teste, saída de comando, screenshot ou trecho verificável.

# FORMATO DE ENTREGA

- Commits atômicos por fase.
- `docs/design/DESIGN_SYSTEM.md` (tokens e regras), `docs/design/CONTRASTE.md` (tabela gerada), `docs/design/AUDITORIA_TELAS.md` (achado por tela, com veredito e correção).
- Relatório final com os quatro estados — `concluído`, `parcial`, `simulado`, `não validado` — mais lista numerada das mudanças de experiência propostas por iniciativa própria, para você aprovar ou eliminar, e lista do que continua pendente de aparelho ou backend.
- Todo texto de UI em pt-BR via i18n.

# CONDIÇÕES DE PARADA E ESCALAÇÃO

- Prosseguir sem perguntar em tudo que for local, gratuito e reversível — inclusive decisões de tipografia, cor, motion, copy e reorganização de tela.
- Parar e perguntar somente para: dependência paga, com serviço externo ou com telemetria; mudança que altere regra de dano, economia ou domínio de saúde; publicar, alterar DNS ou lojas; apagar dado do aparelho ou histórico Git; conflito direto com decisão registrada em `DECISIONS.md`.
- O retorno é definido pela condição de sucesso e suas evidências, nunca por confiança ou volume de texto. Se bloqueado: reportar bloqueio, evidência e a menor próxima ação segura.

# RESULTADOS QUE NÃO CONTAM COMO SUCESSO

- Sistema de design documentado mas não aplicado nas telas.
- Contraste estimado, declarado ou "conferido visualmente" em vez de calculado por script.
- Contraste validado só no tema escuro — o tema claro é onde a maioria das violações aparece.
- Motion existindo na galeria mas não no app.
- Screenshots em um único tamanho, tema ou configuração de acessibilidade.
- Háptico ou fluidez de animação declarados validados a partir de simulador.
- Cor literal, `fontSize` numérico ou raio cru remanescente em `src/**`.
- Componente entregue sem os cinco estados.
- Dynamic Type quebrando qualquer tela.
- `npm run check` vermelho, ou regressão em passos, saúde, dano, campanha e ranking.

# FALHAS A AUDITAR

- Contraste reprovado no tema claro enquanto o escuro passa.
- Texto cortado, truncado ou sobreposto sob Dynamic Type ampliado.
- Alvo de toque abaixo de 44pt, ou dois alvos adjacentes sem separação.
- Safe area ignorada: conteúdo sob Dynamic Island, sob o indicador de home ou sob a tab bar.
- Animação rodando na thread de JS e causando engasgo na rolagem.
- Reduce Motion ignorado, ou obedecido a ponto de remover o feedback de toque.
- Háptico excessivo ou disparado em rolagem.
- Número sem `tabular-nums` pulando de largura a cada atualização.
- Mais de um botão primário na mesma tela; hierarquia de ação ambígua.
- Estado vazio, de erro ou de permissão negada sem tratamento, caindo em tela branca.
- Borda, sombra e fundo acumulados no mesmo elemento; raio aninhado errado.
- Regressão no domínio de passos ou nos adaptadores de saúde.
- Dependência instalada sem necessidade real ou sem registro da razão.
- Queima de tokens por leitura ampla onde `graphify query`/`explain` bastava.
- Subagente saindo do escopo delegado ou integrando sem revisão do orquestrador.

# ESTADO E HANDOFF

Ao fim de cada sessão: atualizar `PROGRESS.md` e `DECISIONS.md` se houve mudança de estado ou decisão; registrar em `AGENT_HANDOFF.md` um estado pequeno e factual — decisões tomadas, arquivos alterados, validações executadas, screenshots geradas, pendências e próximo passo; atualizar a posse em `WORK_QUEUE.md`; commit atômico. Nunca depender da memória implícita da conversa.
