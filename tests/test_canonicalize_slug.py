from guides.slugify import canonicalize_slug


def test_exact_match_returns_existing():
    assert canonicalize_slug("Claude Code", ["claude-code"], "tool") == "claude-code"


def test_fuzzy_match_above_threshold():
    # "claud-code" is very similar to "claude-code"
    result = canonicalize_slug("Claud Code", ["claude-code"], "tool")
    assert result == "claude-code"


def test_new_name_below_threshold():
    result = canonicalize_slug("Cursor IDE", ["claude-code"], "tool")
    assert result == "cursor-ide"


def test_empty_existing_returns_candidate():
    assert canonicalize_slug("New Tool", [], "tool") == "new-tool"


def test_empty_name_returns_string():
    result = canonicalize_slug("", ["claude-code"], "tool")
    assert isinstance(result, str)


def test_all_existing_slugs_checked_not_just_ten():
    # More than 10 existing slugs — dedup must still work
    existing = [f"tool-{i:03d}" for i in range(20)] + ["claude-code"]
    assert canonicalize_slug("Claude Code", existing, "tool") == "claude-code"
