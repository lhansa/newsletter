# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Automation for a personal Spanish-language email newsletter (leonardohansa.com), sent via the
MailerLite API. Newsletter issues live as Markdown files with YAML frontmatter; a Python script
turns any issue marked ready into a MailerLite campaign.

Code, comments, and content in this repo are written in Spanish — match that convention when
editing scripts or newsletter issues.

## Repository structure

- `correos/` — newsletter issues, one Markdown file per issue (`YYYY-MM-DD-slug.md`), each with a
  YAML frontmatter block (see Content workflow below) followed by the Markdown body.
- `scripts/send_mail.py` — main automation entry point: scans `correos/`, creates a MailerLite
  campaign draft for any issue ready to send, then updates that issue's frontmatter.
- `scripts/utils.py` — frontmatter parsing/update helpers (`parse_markdown_with_frontmatter`,
  `update_frontmatter_field`) used by `send_mail.py`.
- `scripts/requirements.txt` — dependencies for everything under `scripts/` and `rest/`.
- `rest/get_id.py` — standalone helper that lists MailerLite group IDs/names, for looking up the
  `groups` value used in `send_mail.py`.

There is no build step, test suite, or linter configured in this repo.

## Setup and commands

```bash
pip install -r scripts/requirements.txt
export MAILERLITE_API_KEY=...        # required by both scripts below
```

Run the newsletter sender (paths are relative, so run from inside `scripts/`):

```bash
cd scripts && python send_mail.py
```

Look up MailerLite group IDs (paths are relative, so run from inside `rest/`; also expects a
`.env.local` at `scripts/.env.local` via python-dotenv):

```bash
cd rest && python get_id.py
```

## Content workflow

Each file in `correos/` has frontmatter with these fields:

- `title` — used as both the campaign name and email subject.
- `status` — lifecycle state: `draft` → `sending` (ready to send) → `sent` (set automatically by
  `send_mail.py` after a successful API call). Only files with `status: sending` are processed.
- `date` — issue date.
- `send_at` — ISO 8601 datetime the email should go out.
- `lang` — content language (`es`).

`send_mail.py` converts the Markdown body to HTML via the `markdown` package before sending.

## Known quirks

- In `send_mail.py`, `crear_newsletter()` sends a hardcoded `scheduled_for` value and hardcoded
  `content: "hola"` in the campaign payload — `send_at` and the converted `cuerpo_html` are
  computed but not actually wired into the request. Check this before relying on scheduling or
  body content working end-to-end.
- The MailerLite `groups` ID in `crear_newsletter()` is hardcoded; use `rest/get_id.py` to find the
  correct group ID rather than guessing.
- `scripts/send_mail.py` reads `MAILERLITE_API_KEY` straight from the environment (its `dotenv`
  loading is commented out), while `rest/get_id.py` loads it from `scripts/.env.local` via
  `python-dotenv`. Set the env var accordingly depending on which script you're running.

## CI

`.github/workflows/opencode.yml` runs the `opencode` GitHub Action when a PR/issue comment
contains `/oc` or `/opencode`, using `opencode/claude-sonnet-5`.
