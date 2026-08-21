// POST /api/subscribe
// Tier-1 endpoint. Email-only capture. Stub: validate + log.
// Real fulfillment (mailing list integration) is out of scope for the first deploy.

interface Env {
  // Bind a KV / external API here later (e.g. CONVERTKIT_TOKEN).
}

const json = (status: number, body: unknown): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });

const isEmail = (s: unknown): s is string =>
  typeof s === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s) && s.length <= 254;

export const onRequestPost: PagesFunction<Env> = async ({ request }) => {
  let email: unknown;
  const contentType = request.headers.get("content-type") ?? "";

  if (contentType.includes("application/json")) {
    const body = (await request.json().catch(() => null)) as { email?: unknown } | null;
    email = body?.email;
  } else {
    const form = await request.formData();
    email = form.get("email");
  }

  if (!isEmail(email)) return json(400, { ok: false, error: "invalid_email" });

  console.log(JSON.stringify({ event: "brief.subscribe", email, ts: Date.now() }));

  if (contentType.includes("application/json")) return json(200, { ok: true });
  return Response.redirect(new URL("/?subscribed=1", request.url).toString(), 303);
};
