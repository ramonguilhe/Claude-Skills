# PROMPT MESTRE — Reforma completa do app de passos (v1, 2026-07-23)

> Decisão do fundador: este prompt substitui `PROMPT_MESTRE_APP_JORNADA_POR_PASSOS.md` como contrato de execução e descarta a direção visual e o conteúdo atuais. Registrar a substituição em `docs/DECISIONS.md` na primeira sessão. As regras de honestidade, segurança e custo de `AGENTS.md` e `CLAUDE.md` continuam valendo.

# OBJETIVO E CRITÉRIO DE SUCESSO

Transformar `apps/mobile` (Expo SDK 57 + React Native 0.86 + TypeScript) de protótipo cru em um app que um usuário final usa sem explicação de desenvolvedor, inteiramente em português do Brasil.

Condição de sucesso, verificável por um leitor adversarial:

1. `npm run check` verde (typecheck estrito, ESLint, todos os testes), com a suíte ampliada para bosses, rankings e migração de estado.
2. Build instalado no iPhone do fundador via extensão do Claude no Xcode, navegável do pré-cadastro até a última aba sem crash.
3. Catálogo com **≥ 30 bosses** data-driven — cada um com identidade própria (nome, arco temático, descrição, cor, ícone), vida incremental testada como crescente e, quando couber, mecânica própria declarativa. Sem imagens nesta fase.
4. Boss global ativo por temporada e rankings de: níveis superados; maior dano em um dia; passos na semana, no mês e no total; Elo de duelo; contribuição no boss global. Tudo funcionando localmente com dados simulados **rotulados como simulação** e com contratos TypeScript prontos para o backend futuro.
5. Fluxo inicial de pré-cadastro completo (boas-vindas com proposta de valor, perfil local, meta diária, permissão de saúde, caminho de permissão negada) e todas as telas reconstruídas na nova identidade visual.
6. Nenhuma tela com texto em inglês, jargão de desenvolvedor ou estética de jogo; infraestrutura i18n preservada com pt-BR como único idioma ativo.

# CONTEXTO E INSUMOS

- Portão de leitura obrigatório, nesta ordem: `AGENTS.md`, `docs/PROJECT_BRIEF.md`, `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/AGENT_HANDOFF.md`, `docs/WORK_QUEUE.md`; depois `git status --short` e `git log -1 --oneline`. Reivindicar a tarefa em `WORK_QUEUE.md` antes de editar.
- Módulos centrais atuais (referência de intenção, não de forma): `App.tsx`; `src/screens/{OnboardingScreen,MainScreens}.tsx`; `src/domain/{steps,campaign,duel,leaderboard}.ts`; `src/storage/prototypeRepository.ts` (migrações v1→v6); `src/health/*` (HealthKit validado em iPhone físico — T1–T4, T6, T7); `src/i18n/*`; `src/ui/{theme,components}`.
- O design e o conteúdo atuais são a primeira versão e serão descartados. Usar o código só para entender a intenção; reimaginar estrutura, navegação, textos e visual livremente — inclusive nomes de abas, hierarquia e features.
- O produto **não é um jogo**: é um app de passos em que passos reais viram dano contra bosses temáticos (maus hábitos) e contra oponentes de duelo. A honestidade sobre o que é real, simulado e não validado é identidade do projeto.

# ESCOPO E RESTRIÇÕES

- **Estética proibida**: interface de jogo ou RPG — pixel art, molduras de fantasia, avatares de personagem, HUD de jogo, e termos como XP, mana, classe, guilda, loot, inventário de itens. **Vocabulário permitido** (mecânica central): passos, dano, vida do boss, duelo, ranking, temporada, boost. Referência visual: app de saúde/fitness premium — limpo, tipografia forte, dados em primeiro plano.
- **Idioma**: todo texto de UI em pt-BR, sempre via i18n (nada hardcoded). Manter o mecanismo de i18n para traduções futuras; desativar o seletor de idioma e remover os catálogos EN/ES para não haver deriva de conteúdo.
- **Bosses sem imagens**: identidade por nome, token de cor, token de ícone e descrição; estrutura pronta para receber arte polida depois sem migração de dados.
- **Domínio de saúde intocável em comportamento**: leitura, reconciliação e não-duplicação de passos (`src/domain/steps.ts`, `src/health/*`) não podem regredir. Toda migração de estado (v6 → v7+) preserva o progresso existente do usuário e tem teste próprio.
- **Sem backend nem serviço pago sem autorização explícita do fundador**: boss global, rankings e duelo nascem local-first com amostras simuladas transparentes; nunca apresentar dado sintético como humano real. Definir as interfaces TypeScript de API que o backend futuro implementará (submissão de dano, snapshot de ranking, pareamento de duelo), de forma que ligar o servidor não exija refazer a UI.
- Sem secrets em commit, sem automação persistente (hooks, watch), sem publicar, sem DNS, sem cobrança.

# EXECUÇÃO

## Ferramentas e economia de tokens

- **Xcode**: usar a extensão do Claude no Xcode (Claude Desktop) para compilar, instalar no iPhone e diagnosticar erros de build. Build físico é o único critério de "roda no aparelho".
- **Graphify**: `graphify update .` uma vez no início da sessão; `graphify query`, `explain` e `path` antes de qualquer mudança transversal ou pergunta ampla de arquitetura, no lugar de grep amplo ou leitura extensa. Nunca usar `extract`, `label`, hooks ou watch. Confirmar no código toda conclusão vinda de aresta `INFERRED` ou `AMBIGUOUS`.
- **Skills**: usar as skills já preparadas (`emil-design-eng` para design, `app-development-workflow` para processo). Antes da Fase 2, procurar nos marketplaces disponíveis skills de design mobile/iOS (Human Interface Guidelines, UX writing, design system) e **instalar as que forem gratuitas e locais — o fundador pré-autoriza a instalação neste prompt**; qualquer skill paga ou que instale automação persistente exige pergunta antes.
- **Delegação de modelos** (o orquestrador roda em Fable): reservar Fable para arquitetura, migração de estado, decisões de design e revisão final. Delegar para subagentes de modelo mais econômico:
  - **Sonnet**: implementação de telas a partir de spec fechada, refactors médios, escrita de testes.
  - **Haiku**: conteúdo tabular (fichas dos bosses a partir do schema aprovado, chaves i18n, variações de copy) e tarefas mecânicas de renomeação.
  Cada subagente recebe objetivo, saída esperada, ferramentas permitidas e limite de escopo; o orquestrador revisa com contexto fresco antes de integrar.
- Ler arquivos sob demanda; não reler o repositório inteiro; comprimir logs e saídas repetitivas, preservando literal apenas erros difíceis, diffs, contratos e evidências.

## Fases

Cada fase termina com validação proporcional e um commit atômico. Não iniciar a fase seguinte com a anterior quebrada.

**Fase 1 — Espinha de produto.** Documento curto em `docs/design/`: novo mapa de telas, arquitetura de informação, nomes das abas e guia de voz pt-BR (tom adulto, direto, motivador, sem infantilizar, sem gíria gamer; toda label compreensível no primeiro uso). Este documento governa as fases seguintes.

**Fase 2 — Sistema visual novo.** Tokens (cor, tipografia, espaçamento, raio, elevação) e componentes base, criados com as skills de design — não derivar do `theme.ts` atual. Acessibilidade desde o token: contraste AA, alvos de toque ≥ 44pt, suporte a Dynamic Type.

**Fase 3 — Pré-cadastro.** Boas-vindas com proposta de valor em no máximo 3 telas; nome/perfil local (texto transparente de que é local, sem conta em servidor); meta diária inicial sugerida; pedido de permissão de saúde com explicação honesta do uso dos dados; caminho completo para permissão negada ou adiada.

**Fase 4 — Catálogo de bosses.** Schema data-driven, por exemplo:

```ts
type Boss = {
  id: string;                    // "acucar-01"
  nome: string;                  // pt-BR, ex.: "Pico de Açúcar"
  arco: ArcoTematico;            // "sedentarismo" | "acucar" | "fast-food" | "preguica" | ...
  descricao: string;             // 1–2 frases no guia de voz
  vidaBase: number;
  crescimentoVida: number;       // fator por posição na trilha; teste garante vida estritamente crescente
  mecanica?: MecanicaBoss;       // declarativa, opcional
  recompensa: Recompensa;
  desbloqueio: CriterioDesbloqueio; // ex.: boss anterior derrotado, streak mínima
  identidade: { corToken: string; iconeToken: string };
};
```

Produzir **≥ 30 bosses** organizados em arcos temáticos de maus hábitos — sedentarismo, açúcar, fast-food, preguiça, excesso de telas/scroll infinito, sono ruim, estresse, procrastinação, e outros que o guia de voz comporte. Mecânicas próprias como dados declarativos interpretados pelo domínio, por exemplo: regenera vida em dia sem meta batida; escudo que só quebra com streak de 3 dias; janela diária de dano em dobro; imune a dano bônus (só passos reais). Conteúdo das fichas pode ser gerado por subagente Haiku a partir do schema aprovado, com revisão do orquestrador.

**Fase 5 — Boss global.** Um boss mundial ativo por temporada, com vida enorme e contribuição de passos de todos os usuários. Por enquanto a comunidade é simulada e **rotulada como simulação** na própria tela; o contrato TS de submissão/leitura fica pronto para o backend real.

**Fase 6 — Rankings.** Placares de: níveis/bosses superados; maior dano em um dia; passos na semana, no mês e no total; Elo de duelo; contribuição no boss global. Locais, com amostras simuladas rotuladas, períodos com virada bem definida (semana/mês no fuso do usuário) e contrato TS pronto para servidor.

**Fase 7 — Telas principais reconstruídas.** Hoje (passos reais em primeiro plano, dano do dia, boss atual); trilha de bosses (campanha); Arena (duelo 72h + preparação para PvP humano futuro); Rankings; Estatísticas (histórico, recordes, tendências); Perfil (edição de nome incluída, preferências, privacidade). Renomear, fundir ou dividir telas conforme a Fase 1 — sem obrigação de manter a navegação atual.

**Fase 8 — Camada de retenção.** Propor e implementar as de baixo risco, registrando cada uma numa lista numerada para o fundador aprovar ou eliminar depois: meta diária ajustável; streak com proteção de falha; conquistas ligadas a passos reais; resumo semanal; notificações locais opt-in (lembrete de meta, boss quase derrotado); feedback tátil; estados vazios bem escritos; tela de privacidade explicando que os dados de saúde ficam no aparelho; exportação de dados. Ideias adicionais são bem-vindas nesse mesmo regime de triagem.

**Fase 9 — Varredura final.** Checklist de conteúdo tela a tela (zero inglês, zero jargão dev, rótulos de simulação onde houver dado sintético); build físico via extensão do Xcode; atualização de `PROGRESS.md`, `DECISIONS.md`, `AGENT_HANDOFF.md` e `WORK_QUEUE.md`; relatório final.

# EVIDÊNCIA E VALIDAÇÃO

- `npm run check` verde a cada fase; testes novos para schema dos bosses, monotonicidade das curvas de vida, mecânicas declarativas, viradas de período dos rankings e migração de estado v6→v7+.
- `npm run export:web` e travessia dos fluxos completos com Playwright em pt-BR, console sem erros: pré-cadastro (incluindo permissão negada), derrotar um boss, boss global, rankings, duelo, perfil.
- Build via extensão do Claude no Xcode com instalação no iPhone; registrar o resultado. O que só passou na web/simulador permanece `não validado` para nativo.
- Toda afirmação importante com evidência rastreável: arquivo, teste, saída de comando ou trecho verificável. Relatório sem evidência não conta como execução.

# FORMATO DE ENTREGA

- Commits atômicos por fase, mensagens descritivas.
- Relatório final com os quatro estados — `concluído`, `parcial`, `simulado`, `não validado` — mais: lista numerada das features extras adicionadas (para triagem do fundador) e lista do que fica pendente de backend real.
- Todo texto de UI em pt-BR via i18n; documentos de design curtos e fatuais em `docs/design/`.

# CONDIÇÕES DE PARADA E ESCALAÇÃO

- Prosseguir sem perguntar em tudo que for local, gratuito e reversível — inclusive decisões de design, conteúdo e features novas.
- Parar e perguntar somente para: contratar backend ou qualquer serviço pago (apresentar opção concreta com custo estimado); publicar, alterar DNS ou lojas; apagar dados do aparelho do fundador ou histórico Git; conflito direto com decisão registrada em `DECISIONS.md`.
- O retorno é definido pela condição de sucesso e suas evidências, nunca por confiança ou volume de texto. Se bloqueado: reportar bloqueio, evidência e a menor próxima ação segura.

# RESULTADOS QUE NÃO CONTAM COMO SUCESSO

- Documento de design sem telas implementadas.
- Catálogo de bosses sem schema tipado e sem testes.
- Ranking ou boss global que aparente conter humanos reais sem rótulo de simulação.
- Interface com estética de jogo/RPG.
- App com idiomas misturados ou texto hardcoded fora do i18n.
- `npm run check` vermelho em qualquer entrega.
- "Pronto" declarado para item nativo com base só em web preview, bundle ou simulador.
- Migração de estado que zera ou corrompe progresso do usuário.

# FALHAS A AUDITAR

- Duplicação ou inflação de passos após refactor do domínio.
- Migração destrutiva do estado v6.
- Texto em inglês residual; jargão gamer; rótulo de simulação ausente.
- Contraste reprovado, alvo de toque pequeno, quebra com Dynamic Type.
- Regressão nos adaptadores de saúde ou na reconciliação diária.
- Secret commitado; hook ou automação persistente instalada sem autorização.
- Queima de tokens por leitura ampla onde `graphify query/explain` bastava.
- Subagente saindo do escopo delegado ou entregando sem revisão do orquestrador.

# ESTADO E HANDOFF

Ao fim de cada sessão: atualizar `PROGRESS.md` e `DECISIONS.md` se houve mudança de estado ou decisão; registrar em `AGENT_HANDOFF.md` um estado pequeno e factual — decisões tomadas, arquivos alterados, validações executadas, pendências e próximo passo; atualizar a posse em `WORK_QUEUE.md`; commit atômico. Nunca depender da memória implícita da conversa.
