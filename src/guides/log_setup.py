import logging

from guides.utils.redact import redact_tokens


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_tokens(str(record.msg))
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(
                    redact_tokens(a) if isinstance(a, str) else a
                    for a in record.args
                )
            elif isinstance(record.args, dict):
                record.args = {
                    k: redact_tokens(v) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
        return True


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    handler.addFilter(RedactFilter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
