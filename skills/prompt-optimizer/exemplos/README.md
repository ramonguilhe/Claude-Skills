# Prompts de Crítica e Criação Literária

Coleção de prompts prontos para colar como instrução/sistema em um chat Claude. Cada um cobre uma fase ou um ângulo diferente do trabalho com um livro — da primeira ideia ao julgamento final, passando pela produção. São arquivos de texto independentes: use o que a tarefa do momento pede.

Todos foram desenhados com as mesmas regras de fundo: evidência obrigatória (nada de acusação ou elogio vago), distinção entre falha e escolha estética deliberada, proibição de inventar fato/obra/citação, e saída em texto limpo pronto para colar em qualquer editor.

## Os prompts

### `genese-do-livro-fase-0.txt` — Coautor de Arquitetura (da ideia à bible)
Para a **Fase 0**, antes da primeira linha. Conduz o autor da ideia bruta até a book bible: concepção (gênero, do que trata, porta de entrada, teste de premissa), perguntas em camadas progressivas, módulos por gênero (enredo, worldbuilding, elenco, pesquisa) e a compilação da bible. Genérico para qualquer gênero.
**Use quando:** está começando um livro do zero e quer fundar bem antes de escrever.

### `critico-literario.txt` — Crítico Multi-Nicho (análise 360°)
Análise profunda e **equilibrada** de uma obra: reconhecimento de gênero, compreensão, narrador, mapeamento estrutural, contradições, análise filosófica, simbologia/plants, título/paratexto, intertextualidade, três notas (crítico / leitor anônimo / fanático) e recomendações priorizadas.
**Use quando:** quer a leitura completa de um livro — o que funciona, o que falha e como evoluir.

### `critico-demolidor.txt` — Crítico Demolidor (só o que falhou)
**100% negativo, por design.** Caça tudo o que está errado e explica por quê, organizado nos 12 grupos de erro (planejamento, estrutura, personagem, narrativa, diálogo, mundo, estilo, emoção, revisão, gramática/tipografia, mercado, e os mais graves) + varredura técnica (contradições, furos, continuidade, tipografia, ritmo). Termina com uma nota de 1 a 100 sozinha na última linha, sem justificativa, descolada da contagem de erros.
**Use quando:** quer descobrir, sem dó, tudo em que errou para consertar.

### `critico-de-autoria.txt` — Crítico de Autoria (o autor no conjunto)
Analisa o **autor através de duas ou mais obras**, não um livro isolado: assinatura autoral, obsessões recorrentes, análise filosófica do corpus, trajetória/evolução, forças e pontos cegos constantes, posicionamento, prospecto do que esperar da próxima obra, e uma nota como autor (0–100).
**Use quando:** quer um retrato crítico de um autor a partir do conjunto da obra dele.

## Qual escolher

| Você quer... | Prompt |
|---|---|
| Começar um livro do zero | `genese-do-livro-fase-0.txt` |
| Leitura completa e equilibrada de uma obra | `critico-literario.txt` |
| Só os defeitos de uma obra, sem suavizar | `critico-demolidor.txt` |
| Avaliar o autor pelo conjunto + prospecto | `critico-de-autoria.txt` |

Fluxo natural: **gênese** (criar) → escrever → **crítico multi-nicho** ou **demolidor** (revisar uma obra) → **crítico de autoria** (quando há mais de um livro). Os três se complementam — o multi-nicho dá o panorama, o demolidor estressa só as falhas, o de autoria sobe um nível e olha a carreira.

## Subpasta — produção em vault Obsidian

`metodologia-livro/` contém os três prompts de **produção** de um livro longo em Claude Code + Obsidian (Crítico, Redactor, Executor) e o README próprio deles. Esses são da fase de escrita/manutenção do manuscrito, distinta da crítica e da concepção tratadas aqui. Veja o `README.md` daquela pasta.

## Como usar qualquer um deles

1. Abra um chat Claude.
2. Cole o conteúdo do `.txt` escolhido como primeira mensagem (instrução/sistema).
3. Forneça a obra (ou, no de autoria, duas ou mais obras; na gênese, comece a conversa).
4. O prompt cuida do resto — formato, profundidade e nota saem conforme especificado em cada arquivo.

Os prompts não têm limite de caracteres por design: priorizam profundidade. Se quiser uma leitura mais curta, peça explicitamente ao chat depois de colar o prompt.
