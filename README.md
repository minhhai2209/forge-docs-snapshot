# Forge Docs Mirror

Simple, polite crawler that renders the Forge docs site with Playwright and saves the
resulting article content as Markdown. Useful when an agent needs a local, greppable
reference without hitting the live docs.

## Why?
- Keep a lightweight local copy of the Forge docs for fast grepping or embedding.
- Respect Atlassian's crawl rules by default (robots.txt + request spacing).
- Capture docs into a deterministic folder tree and `manifest.json` for auditing.

## Quickstart
1. Clone and set up a virtual environment:
   ```bash
   git clone git@github.com:minhhai2209/forge-docs-snapshot.git
   cd forge-docs-snapshot
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   playwright install chromium  # run once per machine
   ```
2. Run the mirror (the defaults already target the Forge docs root):
   ```bash
   forge-docs-mirror --output-dir mirror --delay 0.25 --verbose --max-pages 5
   ```
3. Browse the saved HTML under `mirror/` (mirrors the site path) and inspect
   `mirror/manifest.json` for crawl metadata (timestamp, URL count, etc.).

## CLI options
- `--content-selector`: CSS selector for the main article container. Defaults to
  `article, main, [role='main']` then falls back to Readability heuristics + Markdownify.
- `--root-url`: Point the crawler at a different subtree if Atlassian reorganizes the docs.
- `--browser`: Choose the Playwright engine (`chromium`, `firefox`, `webkit`).
- `--wait-until`: Control Playwright's load strategy (`load`, `domcontentloaded`, `networkidle`).
- `--max-pages`: Stop after _n_ rendered pages—helpful for smoke tests.
- `--delay`: Throttle between requests in seconds (default 0.25).
- `--keep-query`: Treat `?foo=bar` variants as distinct files (off by default).
- `--ignore-robots`: Skip `robots.txt` checks—**only use if you have explicit permission**.
- `--user-agent`: Brand your requests when running inside automation.
- `--seed-url`: Crawl only the given URL(s) instead of starting from the root.

## Output layout
- `mirror/<path>/index.md` – Rendered Markdown for each docs URL. Paths without an
  explicit filename gain an `index.md`, mirroring the site structure.
- `mirror/manifest.json` – Crawl summary (root URL, counts, runtime, delay, user-agent,
  failure list).
- Playwright-rendered DOM ensures client-side nav + tabs make it into the Markdown.

## Automation tips
- Run the tool on a schedule (cron/CI) and keep `playwright install chromium` in the job
  bootstrap so the browser is available.
- Point embedding or grep workflows at `mirror/` to give agents fast offline context.
- Track `manifest.json` in your knowledge repo to prove snapshot freshness + failures.

## License
MIT — see [LICENSE](LICENSE) for details.
