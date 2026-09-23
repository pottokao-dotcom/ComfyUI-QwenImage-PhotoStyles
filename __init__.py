"""
Qwen-Image-2.1 prompt rewriter with photographic styles — V3+ (single stage).

Sends the user's prompt to a PE-T2I rewriter served by any OpenAI-compatible endpoint
(vLLM, llama-server, LM Studio, ...). A bundled style-edition system prompt
(style_sp_plus.txt, adapted from Qwen's official PE-T2I system prompt under the
Qwen Research License) is used as the system message; the chosen style sheet is
appended to the user message, so the style only decides what the user left open.

Two extras that come from the experiments:
  * A mood sub-preset is picked from the seed (presets.json) and appended as a
    "Mood for this image:" line, so re-rolling the seed varies the feeling.
  * Film-grain styles carry a fixed coarse-grain bracket (Grain lead / Grain closer
    lines in the style sheet). The rewriter dilutes grain wording inside its long
    paragraph and the DiT renders clean, so the node wraps the rewrite with the
    bracket to keep grain dominant. Per-style negatives are emitted too.
"""
import json
import logging
import math
import os
import re
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "[QwenImage-PhotoStyles]"
MIN_PROMPT_CHARS = 200
RETRIES = 3
SYSTEM_PROMPT_FILE = os.path.join(HERE, "style_sp_plus.txt")
PRESETS_FILE = os.path.join(HERE, "presets.json")
# Safe for every style; per-style additions come from a "Negative:" line in the sheet.
# ("blurry" is deliberately absent — several styles want motion blur / soft focus.)
BASE_NEGATIVE = ("gibberish text, garbled letters, watermark, signature, "
                 "extra fingers, deformed hands, extra limbs, lowres, jpeg artifacts")
DIRECTIVE_KEYS = ("Negative:", "Grain lead:", "Grain closer:")


def _read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read().strip()


def _system_prompt(path=""):
    if path.strip():
        with open(os.path.expanduser(path.strip()), encoding="utf-8") as f:
            return f.read().strip()
    return _read("style_sp_plus.txt")


def _load_presets():
    try:
        with open(PRESETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


PRESETS = _load_presets()


def _style_names():
    names = {}
    for fn in sorted(os.listdir(os.path.join(HERE, "styles"))):
        if fn.endswith(".txt"):
            first = _read("styles", fn).splitlines()[0]
            m = re.match(r"###\s*Style:\s*(.+)", first)
            names[m.group(1).strip() if m else fn[:-4]] = fn
    return names


STYLES = _style_names()


def _split_sheet(text):
    """Pull node-side directives (Negative / Grain lead / Grain closer) out of a style
    sheet. Returns (sheet_without_directives, directives_dict). The remaining sheet is
    what the rewriter sees; the directives are applied by the node afterwards."""
    kept, directives = [], {}
    for line in text.splitlines():
        s = line.strip()
        for key in DIRECTIVE_KEYS:
            if s.startswith(key):
                directives[key[:-1].lower().replace(" ", "_")] = s[len(key):].strip()
                break
        else:
            kept.append(line)
    return "\n".join(kept).strip(), directives


def _mood_line(slug, seed):
    ps = PRESETS.get(slug) or []
    if not ps:
        return ""
    p = ps[seed % len(ps)]
    moving = "caught in motion" if p.get("motion") == "motion" else "a still, held instant"
    return f"\nMood for this image: {p['delta']}. The moment is {moving}."


def _dims(ratio, pixels=1024 * 1024, step=32):
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*$", str(ratio or ""))
    r = float(m.group(1)) / float(m.group(2)) if m else 1.0
    w = math.sqrt(pixels * r)
    h = w / r
    return max(step, round(w / step) * step), max(step, round(h / step) * step)


def _chat(endpoint, model, system, user, temperature, seed, timeout):
    url = endpoint.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/v1/chat/completions" if not url.endswith("/v1") else "/chat/completions"
    body = {
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": 4096,
        "temperature": temperature,
        "seed": seed,
    }
    if model:
        body["model"] = model
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            msg = json.loads(r.read())["choices"][0]["message"]
    except urllib.error.URLError as e:
        raise RuntimeError(f"{TAG} can't reach the PE-T2I server at {url}: {e}. "
                           f"Start the PE-T2I rewriter first (see README).")
    return (msg.get("content") or msg.get("reasoning_content") or "").strip()


def _parse(raw):
    text = raw.rpartition("</think>")[2].strip() or raw
    i, j = text.find("{"), text.rfind("}")
    if i < 0 or j <= i:
        return None, None
    try:
        d = json.loads(text[i:j + 1])
    except json.JSONDecodeError:
        return None, None
    prompt = d.get("rewritten_prompt")
    if not prompt:  # unexpected key: take the longest string value
        strings = [v for v in d.values() if isinstance(v, str)]
        prompt = max(strings, key=len) if strings else None
    return prompt, d.get("wh_ratio")


class QwenImagePhotoStylePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "style": (["None"] + list(STYLES.keys()),),
                "endpoint": ("STRING", {"default": "http://127.0.0.1:8207"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.5, "step": 0.05}),
            },
            "optional": {
                "model": ("STRING", {"default": ""}),
                "timeout_s": ("INT", {"default": 600, "min": 30, "max": 3600}),
                "system_prompt_path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "INT", "STRING")
    RETURN_NAMES = ("prompt", "negative", "width", "height", "wh_ratio")
    FUNCTION = "rewrite"
    CATEGORY = "Qwen-Image"

    def rewrite(self, prompt, style, endpoint, seed, temperature, model="", timeout_s=600,
                system_prompt_path=""):
        if not prompt.strip():
            raise ValueError(f"{TAG} the prompt is empty.")
        system = _system_prompt(system_prompt_path)
        user = prompt.strip()
        directives = {}
        if style != "None":
            slug = STYLES[style][:-4]
            sheet, directives = _split_sheet(_read("styles", STYLES[style]))
            user += "\n\n---\n" + sheet + _mood_line(slug, seed)
        last = None
        for attempt in range(RETRIES):
            raw = _chat(endpoint, model, system, user, temperature, seed + attempt, timeout_s)
            text, ratio = _parse(raw)
            if text and len(text) >= MIN_PROMPT_CHARS:
                lead, closer = directives.get("grain_lead", ""), directives.get("grain_closer", "")
                if lead or closer:
                    text = " ".join(p for p in (lead, text, closer) if p)
                negative = BASE_NEGATIVE
                if directives.get("negative"):
                    negative += ", " + directives["negative"]
                w, h = _dims(ratio)
                logging.info(f"{TAG} {style}: {len(text)} chars, ratio {ratio} -> {w}x{h}")
                return {"ui": {"text": [text]}, "result": (text, negative, w, h, ratio or "1:1")}
            last = raw
            logging.warning(f"{TAG} attempt {attempt + 1}: rewrite missing or too short, retrying.")
        raise RuntimeError(f"{TAG} no usable rewrite after {RETRIES} attempts. Last reply: {str(last)[:300]}")


NODE_CLASS_MAPPINGS = {"QwenImagePhotoStylePrompt": QwenImagePhotoStylePrompt}
NODE_DISPLAY_NAME_MAPPINGS = {"QwenImagePhotoStylePrompt": "PE-T2I Photo Style Prompt"}
