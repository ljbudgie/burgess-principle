from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IRIS_HTML = (ROOT / "iris.html").read_text(encoding="utf-8")
IRIS_SYSTEM_PROMPT = (ROOT / "iris" / "system-prompt.md").read_text(encoding="utf-8")
WORKER = (ROOT / "worker.js").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")


def test_iris_html_contains_required_copy_and_controls():
    assert 'Was a human there?' in IRIS_HTML
    assert "Hello. I'm Iris. Tell me what happened — in your own words, however you like. I'll help you work out what to do next." in IRIS_HTML
    assert "I got a letter I don't understand" in IRIS_HTML
    assert "A company is chasing me for money" in IRIS_HTML
    assert "I think a decision about me was unfair" in IRIS_HTML
    assert "I need help writing a letter back" in IRIS_HTML
    assert 'Advanced — bring your own AI' in IRIS_HTML
    assert 'Your saved settings stay only in this browser.' in IRIS_HTML
    assert 'When you use Advanced, your browser sends requests directly to the provider or local endpoint you choose.' in IRIS_HTML
    assert 'claude-sonnet-4-20250514' in IRIS_HTML
    assert 'https://iris-worker.ljbarbers15.workers.dev' in IRIS_HTML
    assert 'sessionStorage' in IRIS_HTML
    assert 'localStorage' in IRIS_HTML


def test_iris_html_embeds_canonical_system_prompt_via_script_tag():
    """The single source of truth is iris/system-prompt.md.

    iris.html must embed the canonical prompt as the content of a
    `<script id="iris-system-prompt" type="text/plain">` block, and must
    NOT carry a divergent inline JS string literal.
    """
    open_tag = '<script id="iris-system-prompt" type="text/plain">'
    assert open_tag in IRIS_HTML, "iris.html must embed the canonical prompt as a script tag"
    start = IRIS_HTML.index(open_tag) + len(open_tag)
    end = IRIS_HTML.index('</script>', start)
    embedded = IRIS_HTML[start:end]
    assert embedded.strip() == IRIS_SYSTEM_PROMPT.strip(), (
        "Embedded #iris-system-prompt must match iris/system-prompt.md exactly. "
        "Run scripts/sync-iris-prompt.py or copy the file contents."
    )
    # Defence-in-depth: no second SYSTEM_PROMPT literal hard-codes the prompt.
    assert 'const SYSTEM_PROMPT = "You are Iris' not in IRIS_HTML


def test_iris_html_keeps_default_proxy_for_standard_mode():
    assert 'sendViaProxy(' in IRIS_HTML
    assert 'fetch(DEFAULT_PROXY_URL' in IRIS_HTML


def test_iris_html_routes_byo_ai_directly_to_selected_provider():
    assert 'https://api.anthropic.com/v1/messages' in IRIS_HTML
    assert 'https://api.openai.com/v1/chat/completions' in IRIS_HTML
    assert 'buildChatCompletionsUrl(baseUrl)' in IRIS_HTML
    assert 'const baseUrl = providerSelectEl.value === "compatible" ? endpointInputEl.value.trim() : undefined;' in IRIS_HTML
    assert 'if (normalized.endsWith("/chat/completions")) return normalized;' in IRIS_HTML


def test_iris_html_streams_via_sse_with_abort_support():
    """Replies must stream into the chat bubble and be cancellable."""
    assert 'AbortController' in IRIS_HTML
    assert 'text/event-stream' in IRIS_HTML
    assert 'parseSSEEvent' in IRIS_HTML
    assert 'readSSE' in IRIS_HTML
    assert 'id="stopButton"' in IRIS_HTML


def test_iris_html_has_accessibility_landmarks():
    """Composer is a labelled form, advanced toggle reflects state, skip link present."""
    assert 'class="skip-link"' in IRIS_HTML
    assert 'href="#composerInput"' in IRIS_HTML
    assert 'id="composerForm"' in IRIS_HTML
    assert 'class="sr-only"' in IRIS_HTML
    assert 'for="composerInput"' in IRIS_HTML
    assert 'aria-expanded="false"' in IRIS_HTML
    assert 'aria-controls="advancedPanel"' in IRIS_HTML
    assert 'prefers-reduced-motion' in IRIS_HTML
    assert 'prefers-color-scheme: dark' in IRIS_HTML


def test_iris_html_has_conversation_toolbar():
    """New / Export / Copy controls must be present and wired."""
    assert 'id="newConversationButton"' in IRIS_HTML
    assert 'id="exportMarkdownButton"' in IRIS_HTML
    assert 'id="exportJsonButton"' in IRIS_HTML
    assert 'id="copyLastReplyButton"' in IRIS_HTML
    assert 'iris-conversation.md' in IRIS_HTML
    assert 'iris-conversation.json' in IRIS_HTML


def test_iris_html_advanced_panel_validates_and_protects_key():
    assert 'id="apiKeyToggle"' in IRIS_HTML
    assert "This key is saved only in this browser's localStorage" in IRIS_HTML
    assert 'validateAdvancedSettings' in IRIS_HTML


def test_worker_is_a_small_anthropic_proxy_without_logging():
    assert 'https://api.anthropic.com/v1/messages' in WORKER
    assert 'ANTHROPIC_API_KEY' in WORKER
    assert 'x-api-key' in WORKER
    assert 'console.' not in WORKER


def test_readme_starts_with_talk_to_iris_line():
    assert README.startswith('<a href="./iris.html">Talk to Iris</a> — open in your browser, no account or install needed.')
