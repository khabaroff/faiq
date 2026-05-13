"""Run all pipelines in sequence: A → B → C → D → E → G."""
from __future__ import annotations

import argparse
import sys
import logging

logger = logging.getLogger(__name__)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run all guides pipelines")
    ap.add_argument("--skip-d", action="store_true", help="Skip quality check (pipeline D)")
    ap.add_argument("--force", action="store_true", help="Force reprocess all stages")
    args = ap.parse_args()

    from guides.pipelines import a_ingest, b_summarize, c_wiki_update

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    logger.info("=== Pipeline A: ingest ===")
    rc = a_ingest.main(["--force"] if args.force else [])
    if rc:
        logger.error("Pipeline A failed with code %s", rc)
        return rc

    logger.info("=== Pipeline B: summarize ===")
    rc = b_summarize.main(["--force"] if args.force else [])
    if rc:
        logger.error("Pipeline B failed with code %s", rc)
        return rc

    logger.info("=== Pipeline C: wiki update ===")
    rc = c_wiki_update.main(["--force"] if args.force else [])
    if rc:
        logger.error("Pipeline C failed with code %s", rc)
        return rc

    if not args.skip_d:
        try:
            from guides.pipelines import d_quality_check
            logger.info("=== Pipeline D: quality check ===")
            d_quality_check.main([])
        except (ImportError, NotImplementedError):
            logger.warning("Pipeline D not ready, skipping")

    logger.info("=== Pipeline E: SEO optimization ===")
    try:
        from guides.pipelines import e_seo
        e_seo.main(["--force"] if args.force else [])
    except (ImportError, Exception) as e:
        logger.error("Pipeline E failed: %s", e)

    logger.info("=== Pipeline G: Telegram publish ===")
    try:
        from guides.pipelines import g_telegram
        # Telegram usually doesn't need --force as it depends on state[slug].published_telegram
        g_telegram.main([])
    except (ImportError, Exception) as e:
        logger.error("Pipeline G failed: %s", e)

    logger.info("=== All done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
