# Manim Best Practices Skill

Este repositório contém a **Skill de Boas Práticas do Manim Community Edition (ManimCE)**, estruturada para ser consumida e utilizada diretamente por agentes de inteligência artificial (Antigravity, Cursor, Claude Code, GitHub Copilot, Windsurf, Aider, ChatGPT, etc.) ou desenvolvedores.

---

## 🤖 Como Usar Esta Skill com Qualquer IA

Se estiver usando uma IA ou assistente de código, você pode orientá-la a seguir as diretrizes deste repositório fornecendo o arquivo [`SKILL.md`](SKILL.md) como prompt de contexto ou regra de projeto.

### Prompt de Inicialização para IAs:
```markdown
Você é um especialista em animações matemáticas usando Manim Community Edition (ManimCE).
Antes de gerar qualquer cena ou código Manim, você DEVE consultar e seguir estritamente as diretrizes em:
- SKILL.md (regras essenciais e fluxo de trabalho)
- references/layout_guidelines.md (regras de enquadramento 16:9, containers e espaçamento)
- references/best_practices.md (paleta de cores, tipografia e performance)
- references/syntax.md (sintaxe recomendada de Mobjects e animações)
- examples/ (estruturas e templates executáveis)
```

---

## 📁 Estrutura de Arquivos

```
.
├── SKILL.md                          # Ponto de entrada principal da skill com diretrizes centrais
├── README.md                         # Documentação e instruções de uso universal
├── references/                       # Guias detalhados e referências técnicas
│   ├── layout_guidelines.md          # Canvas 16:9, grid budgeting, bounding boxes e anti-sobreposição
│   ├── best_practices.md             # Pacing visual, harmonia de cores, boas práticas de código e performance
│   └── syntax.md                     # Catálogo de sintaxe de Mobjects, animações, LaTeX e transformações
└── examples/                         # Exemplos Python executáveis
    ├── basic_scene.py                # Exemplo essencial de transformações LaTeX e updaters
    └── split_screen_layout.py        # Template de tela dividida em cards e painéis independentes
```

---

## 🎯 Resumo das Diretrizes Principais

1. **Layout e Bounding Box (16:9)**:
   - Canvas padrão do Manim: largura `14.22`, altura `8.0` (`[-7.11, 7.11]` em X e `[-4.0, 4.0]` em Y).
   - Use containers (`RoundedRectangle`) para limitar espacialmente o texto e os diagramas.
   - Sempre utilize `.arrange()` ou posicionamentos relativos (`next_to`, `shift`) para evitar sobreposição de elementos.

2. **Tipografia e LaTeX**:
   - Sempre declare strings LaTeX como raw strings: `r"..."`.
   - Isole termos com `substrings_to_isolate` ou `{{ ... }}` para transformações precisas (`TransformMatchingTex`).

3. **Fluidez e Transições**:
   - Prefira `ReplacementTransform` ou `.animate` para evitar mobjects fantasmas no grafo de renderização.
   - Utilize `ValueTracker` com `always_redraw(...)` para variáveis e gráficos dinâmicos.

4. **Ciclo de Desenvolvimento**:
   - Sempre teste cenas com renderização rápida em baixa resolução:
     ```bash
     manim -pql examples/split_screen_layout.py SplitScreenLayoutScene
     ```
   - Renderize a versão final em alta qualidade:
     ```bash
     manim -pqh examples/split_screen_layout.py SplitScreenLayoutScene
     ```
