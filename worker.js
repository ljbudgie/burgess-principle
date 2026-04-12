const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json"
    }
  });
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS
      });
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Only POST is allowed." }, 405);
    }

    if (!env.ANTHROPIC_API_KEY) {
      return jsonResponse({ error: "ANTHROPIC_API_KEY is not configured." }, 503);
    }

    let body = "";
    try {
      body = await request.text();
    } catch {
      return jsonResponse({ error: "Request body could not be read." }, 400);
    }

    if (!body) {
      return jsonResponse({ error: "Request body is required." }, 400);
    }

    const upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": env.ANTHROPIC_API_KEY
      },
      body
    });

    return new Response(upstream.body, {
      status: upstream.status,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": upstream.headers.get("Content-Type") || "application/json"
      }
    });
  }
};
