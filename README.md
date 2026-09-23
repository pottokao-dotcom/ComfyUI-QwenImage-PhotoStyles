# ComfyUI-QwenImage-PhotoStyles

A single ComfyUI node — **PE-T2I Photo Style Prompt** — that turns a short prompt into a
rich, styled one for **Qwen-Image-2.1**.

Pick a **photographic style** from a dropdown (17 styles), type a short prompt, and the node
sends it to a **PE-T2I rewriter** (any OpenAI-compatible endpoint) together with that style's
sheet. It returns a long English prompt, a matching **negative prompt**, and the **width /
height** for the aspect ratio the rewriter chose.

Each style is described as **camera language + mood** — never a photographer's name. Your
subject, and whatever text / counts / colours / positions you specify, stay yours; the style
only decides what you left open. The shorter your prompt, the more the style shows through.

> **This is not a model loader.** It only produces text (prompt / negative) and two integers
> (width / height). It has nothing to do with GGUF / NVFP4 / fp8 / bf16 — those only matter for
> the loader nodes downstream. Use it with any Qwen-Image-2.1 setup, in any format.

## How it works

```
[PE-T2I Photo Style Prompt] --prompt----> TextEncodeQwenImage21.prompt
                            --negative--> TextEncodeQwenImage21.negative_prompt
                            --width-----> EmptyLatentImage.width
                            --height----> EmptyLatentImage.height
```

It is a self-contained node: it follows the ComfyUI node interface and uses only the Python
standard library (`urllib`, `json`). It does not import `comfy` or `torch`, and it does not
subclass or bundle any other node — the loaders, `TextEncodeQwenImage21` and the samplers are
your existing Qwen-Image-2.1 nodes; this node just wires into them.

## Requirements

1. A ComfyUI that can already run **Qwen-Image-2.1** (i.e. it provides `TextEncodeQwenImage21`
   and the UNet / CLIP / VAE loaders you use).
2. A running **PE-T2I rewriter** on an OpenAI-compatible `/v1/chat/completions` endpoint,
   serving `Qwen/Qwen-Image-2.1-PE-T2I` (any backend — vLLM, llama-server, LM Studio, ...; any
   weight format). Point the node's `endpoint` at it (default `http://127.0.0.1:8207`).

No Python dependencies to install.

## Install

Clone into your `custom_nodes` folder and restart ComfyUI:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/pottokao-dotcom/ComfyUI-QwenImage-PhotoStyles
```

Or install from the ComfyUI Registry via ComfyUI Manager (search "Qwen-Image Photo Styles").

## Inputs / Outputs

**Inputs** — `prompt` (multiline), `style` (dropdown: `None` + 17 styles), `endpoint`, `seed`,
`temperature`; optional `model`, `timeout_s`, `system_prompt_path`.

**Outputs** — `prompt` (STRING), `negative` (STRING), `width` (INT), `height` (INT),
`wh_ratio` (STRING).

`seed` also picks one of the style's mood sub-presets, so re-rolling it varies the feeling.

## The 17 styles

Black Fury · Geometry of Light · Warm Documentary · White Leap · Corner Elegance · Cold Power ·
Hyper Chic East · Private Diary · Color Behind Glass · Frozen Film Still · Fairytale Giants ·
Soft Everyday Light · Street in the Mirror · Pale Light Moments · Everyday Punchline ·
Vivid Garden · Playful Film.

Each style sheet in `styles/*.txt` specifies, per style: **Look, Lens language, Light, Emotion,
People, Scene & props, Colour**, plus per-style negatives and — for film-look styles — a
fixed grain clause. Grain is baked into the style (film styles such as Black Fury wrap the
rewrite in a coarse-grain clause, because the rewriter otherwise dilutes grain wording and the
model renders too clean).

## Example

See `example_workflow_api.json` (API format — enable *Dev mode* in ComfyUI settings, then
*Load (API Format)*). The loader nodes and model file names there are just an example; swap in
whatever Qwen-Image-2.1 models and format you use.

## Licensing

- Node code, style sheets, `presets.json`, docs — **MIT** (see `LICENSE`).
- `style_sp_plus.txt` is adapted from Qwen's official Qwen-Image-2.1-PE-T2I system prompt and
  remains under the **Qwen Research License** (see `NOTICE`). Review it before commercial use.
