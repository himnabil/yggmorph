# Dialect Companion

An AI companion that chats with you in Arabic dialects — starting with the
**Oran dialect (Wahrani / الوهرانية)** of western Algeria — and translates every
exchange into standard languages (English and French).

Built on the Anthropic Claude API (`claude-opus-4-8`) with streaming responses,
adaptive thinking, and prompt caching.

## Features

- **Chat in dialect** — the companion speaks authentic Wahrani (Arabic script +
  Latin transliteration), understands Arabic script, Arabizi (`wech rak 5oya`),
  French, and English input.
- **Live translation** — after each exchange it shows what *you* said and what
  *it* said in both English and French, so you can learn or verify meaning.
- **One-shot translation** — `dialect-companion translate "..."` returns a
  structured translation: Modern Standard Arabic, English, French, plus notes
  on idioms and loanwords.
- **Extensible dialect registry** — Oran, Algiers, and Constantine ship today;
  adding a dialect is one entry in `dialect_companion/dialects.py`.

## Install

Requires Python 3.10+ and [uv](https://github.com/astral-sh/uv) (or pip).

```bash
cd dialect-companion
uv sync          # or: pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### Interactive chat

```bash
uv run dialect-companion chat
```

```
you > wech rak khoya, wechraki l'famille?

واه الحمد لله غاية، نتينا كيراك؟ الدار بخير الحمد لله
(wah hamdoullah ghaya, ntina kirak? eddar bkhir hamdoullah)
---
📥 You said → EN: How are you bro, how's the family?
           → FR: Comment vas-tu frère, comment va la famille ?
📤 I said  → EN: Yes, thank God, all good — and you, how are you? The family is fine.
           → FR: Oui, Dieu merci, tout va bien — et toi, ça va ? La famille va bien.
```

In-chat commands: `/translate on|off` toggles the translation block,
`/dialects` lists available dialects, `/quit` exits.

### One-shot translation

```bash
uv run dialect-companion translate "kayen bezzaf la pluie derwak f wahran"
```

```
Input (Oran Algerian Arabic (Wahrani)):
  كاين بزّاف لابلي درْوك في وهران

MSA: يوجد الكثير من المطر الآن في وهران
EN:  There's a lot of rain right now in Oran.
FR:  Il pleut beaucoup en ce moment à Oran.
```

### Other dialects

```bash
uv run dialect-companion --dialect algiers chat
uv run dialect-companion --dialect constantine translate "tawa nji"
```

## Roadmap

- More dialects: Moroccan Darija, Tunisian, Egyptian, Levantine, Gulf
- Voice input/output (speech-to-text + TTS)
- More target languages (Spanish, German, ...)
