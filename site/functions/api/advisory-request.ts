// POST /api/advisory-request
// Tier-3 endpoint. Five fields. Stub: validate + log.
// Real fulfillment (Calendly handoff or founder inbox) is out of scope for first deploy.

interface Env {}

const json = (status: number, body: unknown): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });

const isShort = (s: unknown, min = 2, max = 160): s is string =>
  typeof s === "string" && s.trim().length >= min && s.length <= max;

const isMaturity = (s: unknown): s is string =>
  typeof s === "string" && /^(0[1-9]|1[01])$/.test(s);

const isChallenge = (s: unknown): s is string =>
  typeof s === "string" && s.trim().length >= 8 && s.length <= 280;

export const onRequestPost: PagesFunction<Env> = async ({ request }) => {
  const body = (await request.json().catch(() => null)) as
    | {
        name?: unknown;
        role?: unknown;
        company?: unknown;
        maturity?: unknown;
        challenge?: unknown;
      }
    | null;

  if (!body) return json(400, { ok: false, error: "invalid_payload" });
  if (!isShort(body.name)) return json(400, { ok: false, error: "invalid_name" });
  if (!isShort(body.role)) return json(400, { ok: false, error: "invalid_role" });
  if (!isShort(body.company)) return json(400, { ok: false, error: "invalid_company" });
  if (!isMaturity(body.maturity)) return json(400, { ok: false, error: "invalid_maturity" });
  if (!isChallenge(body.challenge)) return json(400, { ok: false, error: "invalid_challenge" });

  console.log(
    JSON.stringify({
      event: "advisory.request",
      name: body.name,
      role: body.role,
      company: body.company,
      maturity: body.maturity,
      challenge_len: (body.challenge as string).length,
      ts: Date.now(),
    })
  );

  return json(200, { ok: true });
};
