"""Run all pipelines in sequence: A → B → C → D → E → G."""
from __future__ import annotations

import argparse
import logging
import sys
from typing import NamedTuple, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


class PipelineResult(NamedTuple):
    name: str
    success: bool
    exit_code: int = 0
    error: str | None = None


@runtime_checkable
class Pipeline(Protocol):
    name: str

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        ...


class IngestPipeline:
    name = "A: Ingest"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import a_ingest
        # A doesn't support --slug in main, it handles what's in inbox
        # or specific --url/--file/--repo which we don't pass from run_all yet
        argv = ["--force"] if force else []
        rc = a_ingest.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


class SummarizePipeline:
    name = "B: Summarize"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import b_summarize
        argv = []
        if force:
            argv.append("--force")
        if slug:
            argv.extend(["--slug", slug])
        rc = b_summarize.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


class WikiUpdatePipeline:
    name = "C: Wiki Update"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import c_wiki_update
        argv = []
        if force:
            argv.append("--force")
        if slug:
            argv.extend(["--slug", slug])
        rc = c_wiki_update.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


class QualityCheckPipeline:
    name = "D: Quality Check"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import d_quality_check
        argv = []
        if slug:
            argv.extend(["--slug", slug])
        rc = d_quality_check.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


class SeoPipeline:
    name = "E: SEO"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import e_seo
        argv = []
        if force:
            argv.append("--force")
        if slug:
            argv.extend(["--slug", slug])
        rc = e_seo.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


class TelegramPipeline:
    name = "G: Telegram"

    def run(self, force: bool = False, slug: str | None = None) -> PipelineResult:
        from guides.pipelines import g_telegram
        argv = []
        if force:
            argv.append("--force")
        if slug:
            argv.extend(["--slug", slug])
        rc = g_telegram.main(argv) or 0
        return PipelineResult(self.name, rc == 0, rc)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run all guides pipelines")
    ap.add_argument("--skip-d", action="store_true", help="Skip quality check (pipeline D)")
    ap.add_argument("--force", action="store_true", help="Force reprocess all stages")
    ap.add_argument("--slug", help="Process only this slug (B through G)")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    # Dependency graph A -> B -> C -> D -> E -> G
    sequence: list[Pipeline] = [
        IngestPipeline(),
        SummarizePipeline(),
        WikiUpdatePipeline(),
        # D is optional via --skip-d
        QualityCheckPipeline(),
        SeoPipeline(),
        TelegramPipeline(),
    ]

    for pipe in sequence:
        if args.skip_d and isinstance(pipe, QualityCheckPipeline):
            logger.info("Skipping %s", pipe.name)
            continue

        logger.info("=== %s ===", pipe.name)
        
        # Note: ImportError is NOT caught here, allowing it to bubble up and fail-fast.
        try:
            res = pipe.run(force=args.force, slug=args.slug)
            if not res.success:
                logger.error("%s failed with code %s", res.name, res.exit_code)
                return res.exit_code or 1
        except Exception:
            logger.exception("Unexpected error in %s", pipe.name)
            raise

    logger.info("=== All done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
