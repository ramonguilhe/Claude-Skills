# Templates de Prompt de Recuperação de Contexto

> Três templates de prompt de recuperação de contexto para uso com a metodologia de criação de livros descrita em `Metodologia de Criacao de Livros - Claude Code + Obsidian.md` (pasta pai).

## O que cada template é

Quando você divide o trabalho de escrita de um livro em três chats Claude com papéis distintos (Crítico, Redactor, Executor), cada chat precisa ler **um prompt de recuperação de contexto específico do seu papel** ao iniciar sessão. Sem isso, cada chat opera com contexto pobre e produz erros.

Os três templates aqui são esqueletos prontos para você customizar com as decisões canônicas do seu livro.

## Os três arquivos

### `prompt-recuperacao-contexto-critico.md`
Para o chat Crítico (Claude Opus). É a **mente pensante** do projeto: trabalho estratégico — esqueletos, análise crítica, verificação de coerência, pacotes para o Executor, filtragem de crítica externa. **30 seções** (1–18 base + 19–30 de expansão), incluindo critérios concretos para fechamento de esqueletos e análise crítica de rascunhos.

### `prompt-recuperacao-contexto-redactor.md`
Para o chat Redactor (Claude Sonnet). É a **mão que escreve**: produção textual de rascunhos a partir de esqueletos do Crítico. **23 seções** (1–13 base + 14–23 de expansão), com checklist de fechamento de rascunho e procedimento detalhado de aplicação de ajustes literais.

### `prompt-recuperacao-contexto-executor.md`
Para o chat Executor (Claude Sonnet). É o **guardião do vault**: aplicação de pacotes de atualização gerados pelo Crítico. **23 seções** (1–11 base + 12–23 de expansão), com templates dos arquivos atômicos típicos do projeto e tipos de tarefa que costumam aparecer em pacotes.

## O que cada papel faz de melhor (resumo)

A divisão de trabalho mantém cada chat focado no que entrega com excelência:

| Papel | Modelo | Entrega central | Não faz |
|---|---|---|---|
| **Crítico** | Opus | Pensa a arquitetura: esqueletos, diagnóstico macro, análise crítica, coerência, filtragem de crítica externa, pacotes | Não escreve rascunhos; não aplica pacotes |
| **Redactor** | Sonnet | Escreve a prosa: rascunhos a partir do esqueleto, sustentando voz e temperatura, sem inventar | Não cria esqueletos; não toca no vault além dos próprios caps + progresso |
| **Executor** | Sonnet | Mantém o vault: aplica pacotes, cria atômicos, INDEX, wikilinks, integridade do grafo | Não escreve/edita capítulos; não decide o canônico |

O fluxo de uma sessão de escrita: **Crítico** gera esqueleto → **Redactor** redige rascunho → **Crítico** avalia → **Redactor** ajusta → **Crítico** gera pacote do vault → **Executor** aplica o pacote e reporta de volta ao Crítico.

## Expansões v1.1 (o que foi acrescentado a cada prompt)

Os três prompts ganharam um bloco de expansões (sem remover nada da base), para que cada papel opere no melhor da sua função:

- **Crítico (seções 19–30):** anatomia do esqueleto detalhado (template do que entrega ao Redactor), diagnóstico de arquitetura macro (curva de tensão, distribuição de plants), procedimento de filtragem de crítica externa, estrutura da análise crítica interna, receitas de grep + protocolo grave/leve de coerência, detecção de drift de voz, autoexame anti-sycophancy, anti-hallucination de plants, consciência de estágio do manuscrito, coragem editorial para cortar, economia de modelo, ponte com a bíblia.
- **Redactor (seções 14–23):** técnica concreta de sustentação de voz, aquecimento de voz antes de escrever, craft cena a cena, ativação de plants sem sublinhar, uso de frases canônicas em variação, gestão de tamanho alvo, detecção de repetições não-intencionais, anti-drift dentro do próprio capítulo, checklist de fechamento ampliado, formato da entrada no `progresso.md`, push back do Redactor.
- **Executor (seções 12–23):** saúde do grafo Obsidian (órfãos, backlinks, aliases), convenção de nomes de arquivos, sincronização bíblia↔atômico (detectar e reportar), tarefa de atualização de "Aparições nos capítulos", detecção de duplicatas, conformidade de template, idempotência na re-execução, protocolo de descartados, git/backup, sinalização de memória persistente defasada, formato padrão de relatório, manutenção do INDEX.

## Como usar

### Setup inicial (uma vez por projeto)

1. **Copie os três arquivos** para a pasta `Notas/prompts/Prompt Recuperacao contexto/` do seu vault Obsidian:
   ```
   livro/
   └── Notas/
       └── prompts/
           └── Prompt Recuperacao contexto/
               ├── prompt-recuperacao-contexto-critico.md
               ├── prompt-recuperacao-contexto-redactor.md
               └── prompt-recuperacao-contexto-executor.md
   ```

2. **Customize cada um** preenchendo os campos `[ENTRE COLCHETES]` com as decisões canônicas do seu projeto:
   - Nome do projeto e autor
   - Tipo de obra
   - Voz narrativa canônica
   - Princípios operantes
   - Léxico vetado
   - Plants firmados
   - Personagens com decisões fixas

3. **Não preencha tudo de uma vez.** Os prompts evoluem com o projeto. Comece com o essencial (papel, voz canônica, estrutura) e adicione conforme decisões canônicas se firmam.

### Uso em cada sessão

Quando abrir um chat Claude para trabalhar no projeto:

1. **Identifique o papel da sessão** (Crítico, Redactor ou Executor)
2. **Peça ao chat para ler o prompt correspondente** logo na primeira mensagem:
   ```
   Leia o arquivo Notas/prompts/Prompt Recuperacao contexto/prompt-recuperacao-contexto-[papel].md
   antes de começar. Carregue todo o contexto do projeto antes de operar.
   ```
3. **Confirme que o chat carregou o contexto** antes de pedir trabalho efetivo. Você pode perguntar algo simples para testar: "Qual é a voz canônica do livro?" — se o chat responde corretamente, está pronto.

### Manutenção dos prompts

Os prompts são **documentos vivos**. Atualize-os sempre que:

- Decisão canônica nova for firmada
- Novo plant for adicionado
- Novo personagem ganhar arquivo atômico
- Léxico vetado mudar
- Capítulo novo for fechado
- Erro grave for documentado (vira lição firmada)

Quem atualiza:
- **Crítico** atualiza o próprio prompt e pode atualizar o do Redactor quando relevante
- **Executor** atualiza o próprio prompt e o INDEX do vault
- **Redactor** atualiza o próprio prompt com últimas decisões e o `progresso.md`

## Por que três prompts separados (e não um só)?

Em projeto longo, o contexto de cada chat cresce com o tempo. Se você usa um único chat para tudo (esqueletos + escrita + manutenção do vault), o chat fica saturado e começa a "esquecer" coisas estabelecidas no início.

A divisão por papel mantém cada chat focado e com contexto manejável. Economia de tokens, performance melhor, menos contradições.

**Se seu projeto é pequeno** (50k palavras ou menos, sem plants distribuídos complexos), você pode operar com um chat só usando o prompt do Crítico como base universal. A divisão em três é otimização para projetos longos e densos.

## Estrutura recomendada do vault

Para que os prompts funcionem como pensados, organize o vault assim (já descrito na Metodologia, repito aqui por conveniência):

```
livro/
├── CLAUDE.md
├── biblia.md
├── progresso.md
├── INDEX.md
├── livro completo.md (consolidado, quando aplicável)
├── Capitulos/
│   └── descartados/
├── Partes/
├── Personagens/
├── Lugares/
├── Conceitos/
├── Tramas/
├── Profissoes/ (se relevante)
├── Notas/
│   ├── pacotes/
│   ├── esqueletos/
│   ├── prompts/
│   │   └── Prompt Recuperacao contexto/
│   │       ├── prompt-recuperacao-contexto-critico.md
│   │       ├── prompt-recuperacao-contexto-redactor.md
│   │       └── prompt-recuperacao-contexto-executor.md
│   └── sessoes/
└── Analise Critica/
```

## Convenção de campos a preencher

Em todos os templates, campos a customizar aparecem como `[TEXTO ENTRE COLCHETES MAIÚSCULOS]`. Substitua tudo entre os colchetes (incluindo os colchetes) pelo conteúdo do seu livro.

Exemplo:
- Template: `**Tipo de obra:** [Romance / Conto longo / Novela / ...]`
- Customizado: `**Tipo de obra:** Romance literário denso em primeira pessoa retrospectiva`

## Versionamento dos prompts

Cada prompt tem na última linha: `*Última atualização deste prompt: [DATA]*`

Atualize a data sempre que modificar substancialmente o prompt. Útil para saber quando o conteúdo refletido nele foi consolidado.

Os três prompts estão na versão de base + expansão **v1.1** (bloco de expansões claramente delimitado por comentário no fim de cada arquivo; nada da base foi removido).

## Limites dos prompts

- **Não são substitutos da bíblia.** Os prompts são resumo operacional + procedimentos. A bíblia é a fonte canônica primária do livro.
- **Não são substitutos da memória persistente** do Claude Code (em `~/.claude/projects/`). A memória persistente injeta contexto automaticamente; o prompt é leitura ativa por sessão.
- **Não substituem leitura dos capítulos.** Em sessões de revisão crítica, ler os capítulos relevantes é insubstituível.

Os prompts são **âncoras de contexto** que aceleram o setup inicial de cada sessão e mantêm os três chats alinhados ao projeto.

---

*Para entender o método completo por trás desses prompts, consulte `Metodologia de Criacao de Livros - Claude Code + Obsidian.md` na pasta pai.*
