"""Run all pipelines in sequence: A → B → C → D → E → G."""
from __future__ import annotations

import argparse
import logging
import sys

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
            rc = d_quality_check.main([]) or 0
            if rc:
                logger.error("Pipeline D failed with code %s", rc)
                return rc
        except ImportError:
            logger.warning("Pipeline D not ready, skipping")

    logger.info("=== Pipeline E: SEO optimization ===")
    try:
        from guides.pipelines import e_seo
        rc = e_seo.main(["--force"] if args.force else []) or 0
        if rc:
            logger.error("Pipeline E failed with code %s", rc)
            return rc
    except ImportError as e:
        logger.error("Pipeline E import failed: %s", e)
        return 1

    logger.info("=== Pipeline G: Telegram publish ===")
    try:
        from guides.pipelines import g_telegram
        rc = g_telegram.main([]) or 0
        if rc:
            logger.error("Pipeline G failed with code %s", rc)
            return rc
    except ImportError as e:
        logger.error("Pipeline G import failed: %s", e)
        return 1

    logger.info("=== All done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
