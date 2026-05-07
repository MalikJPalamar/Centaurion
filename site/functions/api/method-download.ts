// POST /api/method-download
// Tier-2 endpoint. Email + role + company gate. Stub: validate + log.

interface Env {}

const json = (status: number, body: unknown): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });

const isEmail = (s: unknown): s is string =>
  typeof s === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s) && s.length <= 254;

const isShort = (s: unknown, max = 160): s is string =>
  typeof s === "string" && s.trim().length >= 1 && s.length <= max;

export const onRequestPost: PagesFunction<Env> = async ({ request }) => {
  const contentType = request.headers.get("content-type") ?? "";
  let email: unknown, role: unknown, company: unknown;

  if (contentType.includes("application/json")) {
    const body = (await request.json().catch(() => null)) as
      | { email?: unknown; role?: unknown; company?: unknown }
      | null;
    email = body?.email;
    role = body?.role;
    company = body?.company;
  } else {
    const form = await request.formData();
    email = form.get("email");
    role = form.get("role");
    company = form.get("company");
  }

  if (!isEmail(email)) return json(400, { ok: false, error: "invalid_email" });
  if (!isShort(role)) return json(400, { ok: false, error: "invalid_role" });
  if (!isShort(company)) return json(400, { ok: false, error: "invalid_company" });

  console.log(
    JSON.stringify({ event: "method.download", email, role, company, ts: Date.now() })
  );

  if (contentType.includes("application/json")) return json(200, { ok: true });
  return Response.redirect(new URL("/method?delivered=1", request.url).toString(), 303);
};
