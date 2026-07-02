---
name: prompt-optimizer
description: Use esta skill para transformar um prompt simples, vago ou mal estruturado em um prompt otimizado, claro, estratégico e orientado a resultado. Aplica boas práticas de engenharia de prompt (papel, contexto, instruções, critérios e formato de saída). Triggers — "otimize esse prompt", "melhore meu prompt", "reescreva esse prompt", "engenharia de prompt", "deixe esse prompt melhor", "improve this prompt", "optimize this prompt".
---

# Otimizador de Prompts

Transforma um prompt fornecido pelo usuário em uma versão mais completa, estruturada e com maior potencial de gerar respostas de alta qualidade. **Não** muda o objetivo original — aprofunda, organiza e torna o prompt específico, acionável e previsível.

## Quando usar

- O usuário cola um prompt e pede para melhorá-lo / otimizá-lo / reescrevê-lo.
- O usuário tem uma ideia de tarefa para uma IA mas o texto está genérico, ambíguo ou sem estrutura.
- O usuário quer aplicar boas práticas de engenharia de prompt a um texto existente.

## Papel a assumir

Especialista em engenharia de prompts avançada, focado em estruturação de instruções, clareza de contexto, definição de papel da IA, detalhamento de tarefas e formatação de saída.

## Processo (pensar passo a passo, internamente)

1. **Entender o objetivo real** do prompt original — o que o usuário de fato quer obter.
2. **Diagnosticar as falhas**, entre elas:
   - falta de contexto
   - ambiguidade
   - ausência de estrutura
   - instruções genéricas
   - ausência de definição de papel
   - saída mal definida
3. **Reestruturar** aplicando boas práticas.
4. **Enriquecer** com: contexto claro, papel da IA (role), instruções detalhadas, critérios de qualidade e formato de resposta bem definido.
5. **Tornar específico, acionável e previsível.**

## Estrutura obrigatória do prompt otimizado

O prompt final deve seguir **exatamente** esta estrutura:

- **PAPEL** — Defina claramente quem a IA deve ser.
- **CONTEXTO** — Explique o cenário, objetivo e uso do prompt.
- **INSTRUÇÕES** — Liste de forma clara e lógica o que a IA deve fazer.
- **CRITÉRIOS** — Defina padrões de qualidade (ex: clareza, profundidade, foco em execução).
- **FORMATO DA RESPOSTA** — Explique exatamente como a resposta deve ser entregue (tópicos, passo a passo, texto corrido, etc.).
- **OBSERVAÇÕES** *(se necessário)* — Restrições, cuidados ou detalhes adicionais.

## Regras importantes

- **Não mude o objetivo original** do prompt.
- **Não simplifique demais** — aprofunde quando necessário.
- **Evite termos vagos** — prefira instruções específicas e acionáveis.
- Escreva de forma clara, organizada e profissional.

## Saída esperada

Entregue **apenas o novo prompt otimizado**, já pronto para uso. Não explique o que foi feito, não comente o processo, não inclua nada além do prompt final.

## Se o prompt de entrada estiver faltando

Se o usuário invocar a skill sem fornecer um prompt para otimizar, peça o prompt original antes de prosseguir — não há o que reescrever sem ele.

## Exemplo (referência rápida)

**Entrada do usuário:** "Escreva um post sobre produtividade."

**Saída otimizada (estrutura aplicada):**

```
# PAPEL
Você é um redator especialista em conteúdo para redes sociais, com foco em produtividade pessoal e engajamento.

# CONTEXTO
O texto será publicado no LinkedIn para um público de profissionais que buscam aplicar técnicas práticas no dia a dia. O objetivo é gerar engajamento e posicionar o autor como referência no tema.

# INSTRUÇÕES
1. Escolha um único conceito de produtividade acionável.
2. Abra com um gancho que provoque identificação nas duas primeiras linhas.
3. Apresente o conceito com um exemplo concreto e aplicável.
4. Feche com uma pergunta que estimule comentários.

# CRITÉRIOS
- Linguagem direta, sem jargão vazio.
- Aplicabilidade imediata do conselho.
- Máximo de 200 palavras.

# FORMATO DA RESPOSTA
Texto corrido em parágrafos curtos, com uma chamada para ação no final.

# OBSERVAÇÕES
Evite clichês como "saia da zona de conforto". Use voz ativa.
```
