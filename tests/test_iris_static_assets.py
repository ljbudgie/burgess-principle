from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IRIS_HTML = (ROOT / "iris.html").read_text(encoding="utf-8")
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


def test_iris_html_keeps_the_exact_system_prompt():
    assert 'You are Iris, the sovereign AI companion for the Burgess Principle (UK Certification Mark UK00004343685).' in IRIS_HTML
    assert 'The core question: was a human member of the team able to personally review the specific facts of my specific situation?' in IRIS_HTML
    assert 'SOVEREIGN (1) if yes. NULL (0) if no.' in IRIS_HTML
    assert 'Never predict legal outcomes.' in IRIS_HTML


def test_iris_html_keeps_default_proxy_for_standard_mode():
    assert 'return sendViaProxy();' in IRIS_HTML
    assert 'fetch(DEFAULT_PROXY_URL' in IRIS_HTML


def test_iris_html_routes_byo_ai_directly_to_selected_provider():
    assert 'https://api.anthropic.com/v1/messages' in IRIS_HTML
    assert 'https://api.openai.com/v1/chat/completions' in IRIS_HTML
    assert 'provider === "openai" ? OPENAI_CHAT_COMPLETIONS_URL : buildChatCompletionsUrl(baseUrl)' in IRIS_HTML
    assert 'baseUrl: providerSelectEl.value === "compatible" ? endpointInputEl.value.trim() : ""' in IRIS_HTML
    assert 'if (normalized.endsWith("/chat/completions")) return normalized;' in IRIS_HTML


def test_worker_is_a_small_anthropic_proxy_without_logging():
    assert 'https://api.anthropic.com/v1/messages' in WORKER
    assert 'ANTHROPIC_API_KEY' in WORKER
    assert 'x-api-key' in WORKER
    assert 'console.' not in WORKER


def test_readme_starts_with_talk_to_iris_line():
    assert README.startswith('<a href="./iris.html">Talk to Iris</a> — open in your browser, no account or install needed.')
