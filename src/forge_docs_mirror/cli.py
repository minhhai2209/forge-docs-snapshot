from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Deque, Iterable, List, Optional, Set
from urllib import robotparser
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page, sync_playwright
from readability import Document

DEFAULT_ROOT = "https://developer.atlassian.com/platform/forge/"
DEFAULT_OUTPUT = "mirror"
DEFAULT_UA = "ForgeDocsMirror/1.0 (+https://github.com/minhhai2209/forge-docs-snapshot)"
DEFAULT_CONTENT_SELECTOR = "article, main, [role='main']"


@dataclass(slots=True)
class CrawlStats:
    discovered: int
    downloaded: int
    skipped: int
    duration_seconds: float
    failures: List[str]


class ForgeDocsMirror:
    def __init__(
        self,
        root_url: str = DEFAULT_ROOT,
        output_dir: Path | str = DEFAULT_OUTPUT,
        *,
        delay: float = 0.25,
        max_pages: int | None = None,
        user_agent: str = DEFAULT_UA,
        keep_query: bool = False,
        respect_robots: bool = True,
        timeout: float = 20.0,
        content_selector: str | None = DEFAULT_CONTENT_SELECTOR,
        browser: str = "chromium",
        headless: bool = True,
        wait_until: str = "networkidle",
        seed_urls: Optional[List[str]] = None,
    ) -> None:
        self.root_url = self._normalize_seed(root_url)
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.delay = max(delay, 0.0)
        self.max_pages = max_pages
        self.user_agent = user_agent
        self.keep_query = keep_query
        self.timeout = timeout
        self.content_selector = content_selector
        self.browser_name = browser
        self.headless = headless
        self.wait_until = wait_until

        self.base_parts = urlparse(self.root_url)
        self.base_netloc = self.base_parts.netloc
        self.base_path = self.base_parts.path.rstrip("/") or "/"

        self.visited: Set[str] = set()
        if seed_urls:
            normalized_seeds = [self._normalize_url(url) for url in seed_urls]
            self.queue: Deque[str] = deque(normalized_seeds)
            self.enqueued: Set[str] = set(normalized_seeds)
        else:
            self.queue = deque([self.root_url])
            self.enqueued = {self.root_url}
        self.saved_pages = 0
        self.skipped_pages = 0
        self.failures: List[str] = []

        self.robot_parser = None
        if respect_robots:
            self.robot_parser = robotparser.RobotFileParser()
            robots_url = f"{self.base_parts.scheme}://{self.base_netloc}/robots.txt"
            try:
                self.robot_parser.set_url(robots_url)
                self.robot_parser.read()
                logging.debug("Loaded robots.txt from %s", robots_url)
            except Exception as exc:  # noqa: BLE001
                logging.warning("Could not load robots.txt (%s): %s", robots_url, exc)
                self.robot_parser = None

    # ------------------------------------------------------------------
    def run(self) -> CrawlStats:
        start = time.perf_counter()
        with sync_playwright() as playwright:
            browser_type = getattr(playwright, self.browser_name, None)
            if browser_type is None:
                msg = f"Unsupported browser '{self.browser_name}'. Choose from chromium|firefox|webkit."
                raise ValueError(msg)

            browser = browser_type.launch(headless=self.headless)
            context = browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1400, "height": 900},
            )
            page = context.new_page()

            try:
                self._crawl(page)
            finally:
                context.close()
                browser.close()

        duration = time.perf_counter() - start
        stats = CrawlStats(
            discovered=len(self.enqueued),
            downloaded=self.saved_pages,
            skipped=self.skipped_pages,
            duration_seconds=duration,
            failures=self.failures.copy(),
        )
        self._write_manifest(stats)
        return stats

    # ------------------------------------------------------------------
    def _crawl(self, page: Page) -> None:
        while self.queue:
            if self.max_pages is not None and self.saved_pages >= self.max_pages:
                logging.info("Reached max page limit (%s)", self.max_pages)
                break

            target = self.queue.popleft()
            if target in self.visited:
                continue
            self.visited.add(target)

            if not self._in_scope(target):
                logging.debug("Skipping out-of-scope URL %s", target)
                self.skipped_pages += 1
                continue

            if self.robot_parser and not self.robot_parser.can_fetch(self.user_agent, target):
                logging.debug("robots.txt disallows %s", target)
                self.skipped_pages += 1
                continue

            try:
                page.goto(
                    target,
                    wait_until=self.wait_until,
                    timeout=int(self.timeout * 1000),
                )
            except PlaywrightTimeoutError as exc:
                logging.warning("Timed out loading %s: %s", target, exc)
                self.skipped_pages += 1
                self.failures.append(f"timeout: {target}")
                continue
            except PlaywrightError as exc:  # noqa: BLE001
                logging.warning("Playwright failed for %s: %s", target, exc)
                self.skipped_pages += 1
                self.failures.append(f"playwright: {target}")
                continue

            self._dismiss_cookie_banner(page)

            html = page.content()
            markdown = self._render_markdown(html, page)
            self._save_document(target, markdown)
            self.saved_pages += 1

            for link in self._extract_links(html, target):
                if link not in self.visited and link not in self.enqueued:
                    self.queue.append(link)
                    self.enqueued.add(link)

            if self.delay:
                time.sleep(self.delay)

    # ------------------------------------------------------------------
    def _write_manifest(self, stats: CrawlStats) -> None:
        manifest = {
            "root_url": self.root_url,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "discovered_urls": stats.discovered,
            "downloaded_pages": stats.downloaded,
            "skipped_pages": stats.skipped,
            "duration_seconds": round(stats.duration_seconds, 2),
            "user_agent": self.user_agent,
            "delay_seconds": self.delay,
            "failures": stats.failures,
        }
        manifest_path = self.output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        logging.info("Wrote manifest to %s", manifest_path)

    # ------------------------------------------------------------------
    def _dismiss_cookie_banner(self, page: Page) -> None:
        selectors = [
            "#onetrust-accept-btn-handler",
            "button:has-text('Accept All')",
            "button:has-text('Accept all')",
            "button:has-text('Accept')",
        ]
        for selector in selectors:
            try:
                locator = page.locator(selector)
                if locator.count() and locator.first.is_visible():
                    locator.first.click()
                    logging.debug("Dismissed cookie banner via %s", selector)
                    break
            except PlaywrightError:
                continue

    # ------------------------------------------------------------------
    def _render_markdown(self, html: str, page: Page) -> str:
        snippet_html: Optional[str] = None
        if self.content_selector:
            snippet_html = self._selector_html(page, self.content_selector)

        readable_title: Optional[str] = None
        readable_html: Optional[str] = None
        try:
            doc = Document(html)
            readable_html = doc.summary(html_partial=True)
            readable_title = doc.short_title()
        except Exception as exc:  # noqa: BLE001
            logging.debug("Readability failed: %s", exc)

        body_html = snippet_html or readable_html or html
        markdown = md(body_html, heading_style="ATX", bullets="*")
        markdown = markdown.strip()

        title = (readable_title or page.title() or "").strip()
        if title:
            if not markdown.startswith("# "):
                markdown = f"# {title}\n\n{markdown}" if markdown else f"# {title}"
        return markdown + "\n"

    # ------------------------------------------------------------------
    def _selector_html(self, page: Page, selector: str) -> Optional[str]:
        try:
            locator = page.locator(selector)
            if locator.count() > 0:
                return locator.first.inner_html()
        except PlaywrightError as exc:
            logging.debug("Selector %s failed: %s", selector, exc)
        return None

    # ------------------------------------------------------------------
    def _save_document(self, url: str, markdown: str) -> None:
        target_path = self._url_to_path(url)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(markdown, encoding="utf-8")
        logging.info("Saved %s", target_path)

    # ------------------------------------------------------------------
    def _extract_links(self, html: str, base: str) -> Iterable[str]:
        soup = BeautifulSoup(html, "html.parser")
        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href")
            absolute = urljoin(base, href)
            normalized = self._normalize_url(absolute)
            if not normalized:
                continue
            if self._in_scope(normalized):
                yield normalized

    # ------------------------------------------------------------------
    def _url_to_path(self, url: str) -> Path:
        parsed = urlparse(url)
        rel_path = parsed.path
        if rel_path.startswith(self.base_path):
            rel_path = rel_path[len(self.base_path) :]
        rel_path = rel_path.lstrip("/")

        if not rel_path:
            rel_path = "index.md"
        else:
            if rel_path.endswith("/"):
                rel_path = f"{rel_path}index.md"
            elif not Path(rel_path).suffix:
                rel_path = f"{rel_path}/index.md"
            else:
                rel_path = rel_path.rsplit(".", 1)[0] + ".md"

        if self.keep_query and parsed.query:
            safe_query = re.sub(r"[^0-9A-Za-z_-]+", "_", parsed.query)
            stem, suffix = rel_path.rsplit(".", 1)
            rel_path = f"{stem}__{safe_query}.{suffix}"

        return self.output_dir / rel_path

    # ------------------------------------------------------------------
    def _in_scope(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc != self.base_netloc:
            return False
        path = parsed.path.rstrip("/") or "/"
        return path.startswith(self.base_path)

    # ------------------------------------------------------------------
    def _normalize_seed(self, url: str) -> str:
        parsed = urlparse(url.strip())
        if not parsed.scheme:
            parsed = parsed._replace(scheme="https")
        if not parsed.path:
            parsed = parsed._replace(path="/")
        if parsed.path.endswith("/"):
            parsed = parsed._replace(path=parsed.path.rstrip("/"))
        if parsed.path and not parsed.path.startswith("/"):
            parsed = parsed._replace(path=f"/{parsed.path}")
        return urlunparse(parsed._replace(fragment="", query=""))

    # ------------------------------------------------------------------
    def _normalize_url(self, url: str) -> str:
        absolute = urljoin(self.root_url + "/", url)
        parsed = urlparse(absolute)
        if not parsed.scheme:
            parsed = parsed._replace(scheme=self.base_parts.scheme)
        if not parsed.netloc:
            parsed = parsed._replace(netloc=self.base_netloc)
        path = parsed.path or "/"
        path = re.sub(r"/+", "/", path)
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")
        normalized = parsed._replace(path=path, fragment="")
        if not self.keep_query:
            normalized = normalized._replace(query="")
        return urlunparse(normalized)


# ----------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mirror the Atlassian Forge documentation as Markdown via headless Playwright.",
    )
    parser.add_argument(
        "--root-url",
        default=DEFAULT_ROOT,
        help="Root URL to crawl (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT,
        help="Directory to store mirrored pages (default: %(default)s)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.25,
        help="Delay in seconds between page visits (default: %(default)s)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional cap on the number of pages to download",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_UA,
        help="User-Agent header to send (default: %(default)s)",
    )
    parser.add_argument(
        "--keep-query",
        action="store_true",
        help="Treat unique query strings as separate documents",
    )
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="Do not consult robots.txt (be careful)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Per-page timeout in seconds (default: %(default)s)",
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Playwright browser engine to use",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run the browser with a visible UI (useful for debugging)",
    )
    parser.add_argument(
        "--wait-until",
        choices=["load", "domcontentloaded", "networkidle"],
        default="networkidle",
        help="Playwright wait policy before scraping (default: %(default)s)",
    )
    parser.add_argument(
        "--content-selector",
        default=DEFAULT_CONTENT_SELECTOR,
        help=(
            "CSS selector that targets the main article content. "
            "Falls back to Readability heuristics if missing."
        ),
    )
    parser.add_argument(
        "--seed-url",
        action="append",
        default=[],
        help="Optional specific URLs to crawl (repeatable). Skips the default root when set.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


# ----------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s | %(levelname)5s | %(message)s",
    )

    mirror = ForgeDocsMirror(
        root_url=args.root_url,
        output_dir=args.output_dir,
        delay=args.delay,
        max_pages=args.max_pages,
        user_agent=args.user_agent,
        keep_query=args.keep_query,
        respect_robots=not args.ignore_robots,
        timeout=args.timeout,
        content_selector=args.content_selector,
        browser=args.browser,
        headless=not args.headful,
        wait_until=args.wait_until,
        seed_urls=args.seed_url or None,
    )

    stats = mirror.run()

    logging.info(
        "Downloaded %s pages (skipped %s) in %.2fs",
        stats.downloaded,
        stats.skipped,
        stats.duration_seconds,
    )
    if stats.failures:
        logging.info("Encountered %s failures. See manifest.json for details.", len(stats.failures))
    return 0


if __name__ == "__main__":
    sys.exit(main())
