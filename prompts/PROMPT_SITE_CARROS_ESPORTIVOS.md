# PROMPT — Site de anúncio de carros esportivos (projeto novo)

> **Decisões do fundador já tomadas, não reabrir:**
> 1. **Stack:** Astro com ilhas React, hospedado no Cloudflare Pages (a conta já existe, `ramonapps.com`).
> 2. **Contato:** WhatsApp com mensagem pré-preenchida mais e-mail direto. **Sem formulário**, sem backend, sem coleta de dado pessoal.
> 3. **Catálogo:** um arquivo de dados por carro no repositório, com validação de schema que quebra o build.
> 4. **Modelo 3D:** buscar primeiro um modelo livre do chassi ZN6/ZC6 com licença comercial limpa e peças separadas; se não houver, construir o carro estilizado em código. Modelo pago só com autorização.
>
> Primeiro idioma e único por enquanto: **português do Brasil**, com o texto isolado em arquivos de conteúdo para permitir tradução depois.

# OBJETIVO E CRITÉRIO DE SUCESSO

Construir e publicar um site que venda carros esportivos do próprio fundador com credibilidade e presença: narrativa que se revela conforme a pessoa rola, um GT86 explorável em 3D, fotos reais como prova, especificações claras e um caminho de contato de um toque.

Condição de sucesso, verificável por um leitor adversarial:

1. Site no ar no Cloudflare Pages com home, catálogo, página de carro, sobre e contato, tudo em pt-BR, sem erro de console e sem recurso 404.
2. Página do GT86 com visualizador 3D interativo — girar, aproximar, abrir o que o modelo permitir, entrar no interior quando houver — que **degrada com elegância**: sem WebGL, com contexto perdido ou em aparelho fraco, cai para galeria e poster. Canvas em branco é falha.
3. Toda seção anima ao entrar em cena dentro de um vocabulário fechado, e existe um **caminho completo sob `prefers-reduced-motion`** em que o site continua legível, completo e vendendo.
4. **Mobile equivalente, não reduzido**: mesma narrativa, mesma informação, mesma qualidade de acabamento. Nenhuma afordância depende de hover.
5. Lighthouse mobile com throttling de rede e CPU: Performance ≥ 85 na home e ≥ 75 na página com 3D; Acessibilidade ≥ 95; Boas Práticas ≥ 95; SEO 100. LCP < 2,5s, CLS < 0,1, INP < 200ms.
6. Adicionar um carro novo é **criar um arquivo de dados e uma pasta de fotos** — sem tocar em componente. Carro sem modelo 3D funciona. Carro vendido continua no ar, marcado como vendido, sem oferta ativa.
7. `LICENSES.md` cobrindo cada fonte, ícone, modelo, textura e HDRI, com origem e licença verificadas.
8. `docs/FERRAMENTAS.md` relatando as skills, plugins, MCPs e agentes pesquisados, instalados e recusados, com o motivo de cada recusa.

# CONTEXTO E INSUMOS

- **O produto é pessoal, não é concessionária.** São os carros do fundador. Isso é vantagem competitiva e precisa aparecer: quem vende, por que vende, o que o carro tem de bom e de ruim.
- **Fotos reais, quilometragem, histórico de manutenção, preço e detalhes vêm do fundador.** Enquanto não chegarem, usar espaços reservados **visivelmente marcados como pendentes**, nunca dado inventado. Preço e especificação são declarações comerciais: nada de estimar.
- **O 3D é camada de experiência; as fotos reais são a fonte da verdade.** Se o modelo 3D divergir do carro real em roda, aerofólio, cor ou acabamento, isso é dito na página.
- Domínio: subdomínio de `ramonapps.com`, a definir. Alterar DNS exige autorização explícita.
- Não existe repositório ainda. Criar do zero, com Git desde o primeiro commit.

# ESCOPO E RESTRIÇÕES

- **Custo zero sem autorização.** Nada de plano pago, fonte licenciada, asset comprado, API paga ou serviço com cobrança. Compra de modelo 3D é escalação com custo estimado.
- **Licenças de asset — filtro duro.** Aceitar apenas CC0, CC-BY ou royalty-free com uso comercial. **Rejeitar NC**, porque anunciar um carro à venda é uso comercial, **e rejeitar ND**, porque o pipeline exige decimar, comprimir e separar malhas. Registrar cada asset com link e licença.
- **Marca de terceiro.** Nomear "Toyota GT86" para descrever o carro à venda é uso nominativo e está correto. O site **não** pode adotar a identidade visual da Toyota, usar o logotipo como marca própria, nem parecer canal oficial.
- **Sem sequestro de scroll.** Fixar seção durante a rolagem é permitido; impedir o usuário de rolar, não. Sempre é possível chegar ao fim da página rolando normalmente.
- Sem autoplay com som. Sem cookie ou rastreador de terceiros — o que evita banner de consentimento e simplifica LGPD.
- Sem coleta de dado pessoal: não há formulário, então não há base de dados a proteger.
- Orçamento de performance é restrição dura, não meta: JavaScript da home ≤ 150 KB comprimido fora o 3D; pacote 3D total ≤ 6 MB, carregado sob demanda e nunca no caminho crítico.

# EXECUÇÃO

## Fase 0 — Descoberta de ferramentas (obrigatória)

O fundador pediu explicitamente: **não presuma que o que está instalado basta.**

1. Inventariar skills, plugins, MCPs e agentes já disponíveis.
2. Pesquisar na web e nos marketplaces por ferramentas que ajudem de verdade neste projeto: animação dirigida por scroll, GSAP e ScrollTrigger, Three.js e React Three Fiber, otimização de glTF, Core Web Vitals, acessibilidade, SEO técnico, redação de venda.
3. **Instalar as gratuitas e locais — pré-autorizado.** Paga, com telemetria ou com automação persistente exige pergunta antes.
4. Verificar a licença de cada biblioteca de animação antes de adotar, inclusive as que mudaram de modelo recentemente. Licença é decisão de projeto, não detalhe.
5. Criar, com `skill-creator`, uma **skill do próprio projeto** que codifique o vocabulário de motion, o schema do carro, os orçamentos de performance e o guia de voz — para que o segundo e o terceiro carro custem uma fração do primeiro.
6. Criar subagentes de escopo fechado, cada um com objetivo, saída esperada, ferramentas permitidas e limite: **crítico de motion** (audita animação contra o contrato), **guardião de performance** (roda Lighthouse e traces, bloqueia regressão), **revisor de voz** (mantém o texto na primeira pessoa do dono).
7. Entregar `docs/FERRAMENTAS.md` com achados, instalações, recusas e motivos.

## Fase 1 — Identidade e voz humana

Definir nome, marca, paleta, tipografia e tom: futurista e esportivo sem virar clichê de classificado. Escuro por padrão combina com o tema, mas a decisão é do agente com justificativa em uma linha.

**A voz é a do dono, em primeira pessoa.** Isso é o "coração humano" pedido, e ele se constrói com conteúdo concreto, não com adjetivo:

- por que este carro entrou na garagem e por que está saindo;
- o que foi feito nele, com data e quilometragem;
- **o que ele tem de ruim** — risco no para-choque, pneu para trocar, retrabalho pendente. Admitir defeito vende mais que superlativo vazio, e protege a negociação;
- o que o próximo dono precisa saber para conviver com o carro;
- rosto e nome de quem vende, na página Sobre.

Proibido: texto genérico de anúncio, superlativo sem evidência, foto de banco de imagens, "oportunidade única", "impecável" sem foto que sustente. Fechar um guia de voz curto que governe todo o texto do site.

## Fase 2 — Conteúdo como dado

Coleções de conteúdo do Astro com validação de schema que **quebra o build** em campo faltando ou inválido.

Schema do carro: identificador, nome de exibição, marca, modelo, ano de fabricação e modelo, cor, quilometragem, câmbio, motor, potência, torque, tração, combustível, 0–100, número de portas, preço, **status (`disponivel` | `reservado` | `vendido`)**, mês e ano da venda, destaque, galeria com texto alternativo por foto, especificações livres, história em primeira pessoa, pontos fortes, pontos de atenção, referência opcional ao modelo 3D, ordem de exibição.

**Carro vendido continua publicado.** Recebe tratamento visual próprio (dessaturado, selo "Vendido"), o preço dá lugar a "Vendido em <mês/ano>", some dos botões de contato — e passa a funcionar como histórico e prova de que a operação é real. No JSON-LD, a oferta deixa de estar disponível.

Página de carro **sem** modelo 3D precisa funcionar inteira, caindo para galeria. Provar com um segundo carro fictício no ambiente de teste.

## Fase 3 — Sistema de motion

Vocabulário fechado, cinco tipos, nada além disso sem justificativa:

1. **Revelar ao entrar** — uma vez, por `IntersectionObserver`, deslocamento curto mais opacidade, escalonamento de no máximo três elementos.
2. **Ligado ao progresso do scroll** — a rolagem da seção controla um valor contínuo: paralaxe discreta, contador de número, rotação do carro, avanço de linha do tempo.
3. **Transição de rota** — coerente entre páginas, curta.
4. **Micro-interação** — toque e ponteiro, ≤150ms.
5. **Sequência cinematográfica** — exclusiva do herói e do 3D.

Regras: animar apenas `transform`, `opacity` e `filter`, nunca propriedade de layout; `will-change` aplicado e removido; preferir linha do tempo de scroll nativa do CSS onde houver suporte, com alternativa em JavaScript; nenhum elemento animado pode gerar deslocamento de layout; 60fps **medido** em trace, não presumido.

**Mobile tem orçamento menor**: paralaxe pesada desligada, escalonamento reduzido, nada dependente de hover, respeito a `prefers-reduced-data`, atenção a aquecimento e bateria. A experiência é equivalente em narrativa e informação, mais econômica em efeito.

**`prefers-reduced-motion` recebe um caminho completo**, não um interruptor que apaga o site: o conteúdo aparece, as transições viram fade curto, a sequência do herói vira imagem forte, o 3D vira visualização estática navegável. Quem liga essa preferência precisa entender o carro igual.

## Fase 4 — Modelo 3D, com portão de decisão

**Passo 1 — busca com prazo fechado.** O chassi tem três nomes; procurar por todos amplia muito o acervo: *Toyota GT86*, *Toyota 86*, *Scion FR-S*, *Subaru BRZ*, *ZN6*, *ZC6*.

**Filtro de licença:** CC0, CC-BY ou royalty-free comercial. NC e ND estão fora, pelos motivos já declarados.

**Filtro técnico:** capô, portas e mala como malhas separadas com pivô utilizável; interior modelado; contagem de triângulos viável para web.

**Portão:** se, dentro do prazo, nenhum candidato passar nos dois filtros, **não insistir** — construir o carro estilizado em código, que é a alternativa garantida e coerente com a estética futurista. Registrar a decisão com a lista de candidatos avaliados e o motivo de cada rejeição. Modelo pago só com autorização do fundador, apresentando link, licença e custo.

**Pipeline obrigatório:** glTF/GLB com compressão de malha, texturas em KTX2, orçamento total respeitado, níveis de detalhe, carregamento sob demanda atrás de um poster. Renderização por demanda em vez de laço contínuo, densidade de pixel adaptativa, suspensão quando fora da viewport, descarte completo ao desmontar, sombra de contato pré-calculada em vez de sombra dinâmica cara.

**Interação:** órbita com limites que impeçam ver a malha por dentro; hotspots como **botões reais**, acessíveis por teclado, com rótulo em pt-BR; abrir capô, mala e porta quando o modelo permitir; transição de câmera para o interior com saída óbvia. Tudo que o ponteiro faz, o teclado faz. Nenhuma informação existe **só** dentro do 3D.

**Honestidade:** rótulo permanente de que o 3D é representação ilustrativa e as fotos são o carro real, com aviso explícito de qualquer divergência conhecida.

**Degradação:** sem WebGL, com contexto perdido ou em aparelho fraco, trocar por galeria e poster automaticamente.

## Fase 5 — Páginas

- **Home**: herói com o carro, proposta em uma frase, destaque atual, prova (o que já foi vendido), chamada para o WhatsApp.
- **Catálogo**: grade com separação entre disponíveis e vendidos.
- **Carro**: 3D → galeria real → especificações → história em primeira pessoa → pontos de atenção → preço e contato → outros carros.
- **Sobre**: quem é, por que faz isso, como a venda funciona na prática — documentação, transferência, test drive, forma de pagamento.
- **Contato**: WhatsApp com mensagem já preenchida citando o carro que a pessoa estava vendo, e-mail, cidade (não endereço) e horários. No desktop, o link precisa cair no WhatsApp Web.
- **404** e rodapé com atribuições de licença.

## Fase 6 — Fotos reais

Entregar ao fundador um guia curto de captura: ângulos obrigatórios, horário de luz, distância, e a instrução de **fotografar também os defeitos**. Pipeline: AVIF e WebP com fallback, `srcset` responsivo, dimensões explícitas para não causar salto, carregamento tardio exceto a primeira, borrão de baixa resolução como placeholder, visualizador ampliado acessível por teclado, texto alternativo descritivo em pt-BR.

## Fase 7 — Performance, SEO e acessibilidade

Orçamentos como teste que falha. JSON-LD de veículo e oferta, mapa do site, `robots.txt`, cartões de compartilhamento com imagem do carro, canônico. WCAG AA: contraste, foco visível, ordem de tabulação, landmarks, `lang="pt-BR"`. Sem rastreador de terceiros; se houver interesse em métricas, propor a analítica sem cookie do próprio Cloudflare como decisão do fundador.

## Fase 8 — Publicação

Cloudflare Pages com pré-visualização por branch. Publicar em domínio definitivo e mexer em DNS exige autorização. Checklist final antes de anunciar.

## Ferramentas e economia de tokens

- **Graphify** deixa de ser útil num repositório vazio; construir o índice assim que a base de código existir e usar `query`, `explain` e `path` antes de mudanças transversais, no lugar de busca ampla.
- **Playwright** para percorrer, capturar e medir; **Cloudflare** apenas para o deploy aprovado.
- **Delegação de modelos**, cada subagente com escopo fechado e revisão do orquestrador antes de integrar: o modelo mais forte decide sistema de motion, pipeline 3D e arquitetura; um modelo intermediário implementa páginas, componentes e testes; um modelo econômico faz inventário de conteúdo, texto alternativo, varredura de licença e conversão de imagem.
- Ler sob demanda, comprimir logs e listagens, preservar literal apenas erro difícil, diff, licença e evidência.

# EVIDÊNCIA E VALIDAÇÃO

- Playwright percorrendo cada página em 360, 390, 768, 1280 e 1920: capturas por seção, ausência de rolagem horizontal, animações completando, console limpo.
- Execução paralela com `prefers-reduced-motion` ativo provando que todo o conteúdo aparece.
- Lighthouse com throttling de rede e CPU, contra os orçamentos declarados, na home e na página com 3D.
- Teste de degradação: WebGL desabilitado, contexto de WebGL perdido, JavaScript desabilitado (o conteúdo essencial precisa existir no HTML) e rede lenta.
- Testes de schema: carro sem 3D, carro vendido, carro com campo faltando — o último deve quebrar o build.
- Revisão no iPhone real do fundador: fluidez, toque, leitura sob luz forte, consumo de bateria no 3D.
- `LICENSES.md` com cada asset, origem e licença conferidas — não presumidas.

# FORMATO DE ENTREGA

- Repositório novo com commits atômicos por fase.
- Documentos: `docs/FERRAMENTAS.md`, `docs/VOZ.md`, `docs/MOTION.md`, `docs/CONTEUDO.md` (como adicionar um carro, passo a passo, para o próprio fundador), `docs/PERFORMANCE.md`, `LICENSES.md`.
- Relatório final com os quatro estados — `concluído`, `parcial`, `simulado`, `não validado` — mais lista numerada das adições feitas por iniciativa própria, para o fundador aprovar ou eliminar, e **lista do que só o fundador pode fornecer**: fotos reais, quilometragem, histórico, preço, contato, decisão de domínio.

# CONDIÇÕES DE PARADA E ESCALAÇÃO

- Prosseguir sem perguntar em tudo que for local, gratuito e reversível — inclusive identidade visual, motion, estrutura e texto.
- Parar e perguntar somente para: comprar modelo 3D, fonte ou qualquer asset pago; publicar em domínio definitivo ou alterar DNS; contratar serviço com cobrança; adotar rastreador; **publicar preço, quilometragem ou especificação que o fundador não confirmou**.
- Se a busca por modelo 3D livre falhar, **não parar**: construir o carro em código, registrar a decisão e seguir.
- O retorno é definido pela condição de sucesso e suas evidências, nunca por confiança ou volume de texto. Se bloqueado: reportar bloqueio, evidência e a menor próxima ação segura.

# RESULTADOS QUE NÃO CONTAM COMO SUCESSO

- Visualizador 3D que trava, esquenta o aparelho ou deixa canvas em branco em qualquer cenário de falha.
- Animação sem caminho equivalente sob `prefers-reduced-motion`.
- Scroll sequestrado, ou seção da qual não se sai rolando.
- Mobile entregue como versão pobre do desktop.
- Asset com licença NC, ND ou não verificada.
- Preço, quilometragem, potência ou histórico inventados ou estimados.
- Adicionar um carro exigindo editar componente.
- Carro vendido desaparecendo do site, ou mantendo oferta ativa no JSON-LD.
- Lighthouse abaixo dos orçamentos declarados.
- Texto genérico de classificado, sem a voz do dono.
- Ausência do relatório de skills, plugins e agentes — foi pedido explicitamente.

# FALHAS A AUDITAR

- Deslocamento de layout causado por animação de entrada.
- Vazamento de memória de WebGL ao trocar de rota; modelo não descartado mantendo a GPU ativa.
- Paralaxe engasgando no Safari do iPhone.
- `100vh` brigando com a barra do navegador no mobile.
- Fonte bloqueando a renderização.
- Imagem sem dimensão explícita causando salto.
- Hotspot do 3D inalcançável por teclado; informação que só existe dentro do 3D.
- Hover como única afordância.
- Link de WhatsApp sem alternativa no desktop.
- Oferta ativa em carro já vendido no dado estruturado.
- Licença NC ou ND aceita por engano na pressa.
- Divergência entre o modelo 3D e o carro real não declarada.
- Rolagem horizontal em 360px de largura.
- Mídia com autoplay sonoro.
- Espaço reservado de conteúdo indo ao ar como se fosse dado real.
- Tokens queimados em leitura ampla onde uma consulta ao índice bastava; subagente integrando sem revisão do orquestrador.

# ESTADO E HANDOFF

Ao fim de cada sessão: registrar em `docs/HANDOFF.md` um estado pequeno e factual — decisões tomadas, arquivos alterados, validações executadas, capturas geradas, resultado do portão do modelo 3D, pendências e próximo passo; commit atômico. Nunca depender da memória implícita da conversa.
