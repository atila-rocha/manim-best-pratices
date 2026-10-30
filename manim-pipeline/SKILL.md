---
name: manim-pipeline
description: >-
  Fluxo de produção de vídeos Manim do zero à entrega: portão de validação 480p antes do 1080p60,
  comandos de render com --media_dir, preservação do código/vídeo antigo (sufixo _new e snapshot de
  hashes), fila serial de renders em background, verificação pós-render (SHA-256 + duração via
  ffmpeg) e armadilhas do ambiente Windows/PowerShell.
---

# Manim: Pipeline de Render e Verificação

Regra de ouro: **só renderiza 1080p60 depois que o 480p foi validado com o autor.**

## 1. Portão de validação (2 gates)

1. **Gate 1 — 480p**: renderize tudo em baixa resolução (`-ql` = 480p15). Valide com o autor.
2. **Gate 2 — 1080p60**: só após aprovação, renderize a qualidade final (`-qh` = 1080×60).
3. Se o autor pedir ajuste, corrija, re-valide em **480p**, e só então outra vez 1080p.

## 2. Comandos de render

```powershell
# Ambiente do projeto
$env:PYTHONIOENCODING='utf-8'          # sempre antes de python no PowerShell

# 480p (validação)
.venv\Scripts\python -m manim -ql --media_dir media_corrigido src\arquivo_new.py Cena_new

# 1080p60 (final)
.venv\Scripts\python -m manim -qh --media_dir media_corrigido src\arquivo_new.py Cena_new OutraCena_new
```

- **Um arquivo `.py` por invocação** (várias cenas no mesmo arquivo podem ser passadas juntas).
- `--media_dir` mantém todo o media dentro do projeto, separado dos vídeos antigos.

## 3. Armadilhas do ambiente (Windows/PowerShell)

- **`manim` retorna exit code 1 no PowerShell mesmo com sucesso.** Nunca confie no exit code;
  verifique se o `.mp4` foi gerado (caminho e `LastWriteTime`).
- Render é **CPU-bound por padrão (renderer Cairo)**; `--renderer=opengl` usa GPU, mas o contexto
  GL padrão em notebook híbrido cai na **iGPU (Intel UHD)**, não na NVIDIA. Confirme com
  `moderngl.create_standalone_context()` e `GL_RENDERER`. Para forçar a GPU dedicada, marque
  `python.exe` como alto desempenho no Windows/NVIDIA Control Panel (teste a equivalência visual
  antes de trocar o pipeline).
- **Não rode renders em paralelo na mesma máquina**: render em background e enfileire o próximo com
  `Wait-Process -Id <PID anterior> -Timeout <...>` para não disputar a CPU.

## 4. Preservação e higiene de arquivos

- **Nunca edite código antigo nem sobrescreva vídeos antigos.** Todo código novo vai em `*_new.py`,
  toda cena nova tem sufixo `_new`, e todos os vídeos novos vão para uma pasta de mídia separada
  (ex.: `media_corrigido/`).
- Antes de qualquer render, tire um **snapshot de hashes** do material antigo:
  `media_antes/hashes_antes.txt` com linhas `relativopath<TAB>bytes<TAB>SHA-256`.

## 5. Verificação pós-render (script de entrega)

```python
# verificar_entrega.py — o que ele garante
# 1. SHA-256 de cada vídeo antigo em media/videos == hash do snapshot (8/8 intactos).
# 2. Duração e hash de cada vídeo novo 1080p60 (medir via ffprobe/ffmpeg de imageio_ffmpeg).
# 3. Relatório Markdown final (tabela tamanho | duração | hash).
```

- Compare as durações do 1080p60 com as do 480p: devem conferir dentro de ~0,3 s (arredondamento
  de container). Diferenças grandes indicam take diferente.
- Compare revisões por **índice de passo** (usando `stages.json`), nunca por timestamp do vídeo.

## 6. Sequência completa recomendada

1. Snapshot de hashes dos vídeos antigos (`media_antes/`).
2. Desenvolver cenas `_new`; validar com testes dourados (`manim-algoritmo`).
3. Render 480p de tudo → validar com o autor.
4. Ajustes (repetir passo 3 até aprovação).
5. Render 1080p60 enfileirado serialmente em background.
6. Rodar `verificar_entrega.py`: hashes antigos intactos + relatório dos novos.
7. Atualizar a tabela de entregáveis (duração × hash) no relatório do projeto.
