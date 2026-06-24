# Capital Blindado - Bezerra Borges Advogados

Quiz interativo que identifica a estrutura internacional ideal para o perfil patrimonial do usuario, com checkout integrado ao Hotmart.

## Sobre

Landing page com quiz de 4 perguntas que gera 16 combinacoes unicas de resultado. Cada resultado sugere uma estrutura internacional especifica (offshore, holding, cidadania etc.) e direciona para o checkout do infoproduto **Capital Blindado** (PDF + planilha de simulacao).

## Stack

- HTML + CSS + JavaScript puro
- Fonte: Inter + Source Serif 4
- Design dark (#070d0a)
- Responsivo (mobile-first)

## Estrutura

```
index.html              # Landing page + quiz interativo
checkout.html           # Pagina de checkout (integracao Hotmart)
favicon.ico             # Favicon BBLAW
assets/
  bblaw-branco.svg      # Logo BBLAW branca
entregaveis/
  Capital-Blindado.pdf          # PDF do infoproduto
  Capital-Blindado-Calculadora.xlsx  # Planilha de simulacao
gerar_pdf.py            # Script para gerar o PDF
gerar_planilha.py       # Script para gerar a planilha
```

## Quiz

| Pergunta | Opcoes |
|----------|--------|
| Patrimonio | Faixas de valor |
| Objetivo | Protecao, expansao, sucessao etc. |
| Tipo de ativo | Imoveis, investimentos, empresas etc. |
| Abertura a relocacao | Sim/nao/parcial |

16 resultados unicos com recomendacao personalizada de estrutura internacional.

## Deploy

Estatico — hospedavel em qualquer CDN, Vercel ou Netlify.

## Licenca

Propriedade de **Bezerra Borges Advogados**. Uso restrito.
