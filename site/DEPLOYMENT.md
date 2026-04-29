# Centaurion.me — Deployment

**Author:** Deployment Engineer (orchestrator)
**Target:** Cloudflare Pages, custom domain `centaurion.me`
**Critical constraint:** The existing Cloudflare Worker that serves
`/strategic-foresight-dashboard*` MUST continue to resolve at the same hostname
after this site goes live.

---

## 1. Cloudflare context

| Field | Value |
|---|---|
| Account ID | `a0f499fdf91c92650c7ad581f7c2b1ba` |
| Zone ID (centaurion.me) | `8758414dab9a8f6e22083cdad485786f` |
| Pages project name (proposed) | `centaurion-site` |
| Production branch | `main` |

## 2. How the routes coexist

Cloudflare evaluates Worker routes BEFORE the Pages handler. So as long as the
existing Worker route pattern stays in place at the zone level, Pages will
serve everything else.

**Required Worker route (already configured — verify, do not recreate):**

```
centaurion.me/strategic-foresight-dashboard*    →    <existing-worker-name>
```

If that route is ever deleted, the Pages site will return its 404 for the
dashboard URL. Verify in Cloudflare Dashboard → Workers & Pages → the existing
Worker → Triggers → Routes.

## 3. First-time deploy (one-time setup)

```bash
# 1. Install Wrangler if not already.
npm i -g wrangler@latest

# 2. Authenticate with the account.
wrangler login

# 3. From the repo root, build the site.
cd site
npm install
npm run build
# Output: site/dist/

# 4. Create the Pages project (one-time).
wrangler pages project create centaurion-site \
  --production-branch main \
  --compatibility-date 2026-04-01

# 5. Deploy to a preview environment first.
wrangler pages deploy dist \
  --project-name centaurion-site \
  --branch preview-$(date +%Y%m%d-%H%M)

# Verify the preview URL renders all four routes correctly.

# 6. Promote to production by deploying to the production branch.
wrangler pages deploy dist \
  --project-name centaurion-site \
  --branch main
```

## 4. Custom domain attachment

In the Cloudflare Dashboard → Pages → centaurion-site → Custom domains:

1. Add `centaurion.me` and `www.centaurion.me`.
2. Cloudflare will auto-configure CNAME records (zone is already on Cloudflare).
3. Wait for "Active" status (~1 minute).
4. **Verify** in a private window:
   - `https://centaurion.me/` → loads Centaurion site
   - `https://centaurion.me/method` → loads
   - `https://centaurion.me/levels` → loads
   - `https://centaurion.me/engage` → loads
   - `https://centaurion.me/strategic-foresight-dashboard` → loads the existing Worker output (not the Pages 404)

If the dashboard route returns the Pages 404, the Worker route was wiped or
never re-bound. Recreate it before announcing the new site.

## 5. Pages Functions

The form endpoints live at `site/functions/api/*.ts`. Cloudflare Pages picks
them up automatically from the `functions/` directory at build time. No extra
config required. Verify post-deploy:

```bash
curl -i -X POST https://centaurion.me/api/subscribe \
  -H "content-type: application/json" \
  -d '{"email":"test@example.com"}'
# expect: HTTP/2 200, body: {"ok":true}
```

The endpoints currently log to the Pages function output (visible in
Dashboard → Pages → centaurion-site → Functions logs). Hook them up to a
mailing list / inbox / CRM in a follow-up.

## 6. Continuous deploys

Connect the Pages project to GitHub once the first deploy is verified:

- Dashboard → Pages → centaurion-site → Settings → Builds & deployments → Connect to Git
- Repository: `MalikJPalamar/Centaurion`
- Production branch: `main`
- Build command: `cd site && npm install && npm run build`
- Build output directory: `site/dist`
- Root directory: `/` (leave default)

Pull-request previews are automatic.

## 7. Performance budget enforcement

CI hook (post-deploy, recommended): run Lighthouse against the preview URL and
fail the deploy if Performance < 95 mobile or Accessibility < 100. Use
`@lhci/cli` with the existing budget defined in this brief (LCP < 1.8s, hero
weight < 250KB).

## 8. Rollback

```bash
# List recent deployments.
wrangler pages deployment list --project-name centaurion-site

# Promote a previous deployment back to production.
wrangler pages deployment tail <deployment-id>
# Or use Dashboard → Pages → Deployments → Rollback.
```

## 9. DNS sanity check (post-deploy)

```bash
dig centaurion.me +short              # Should resolve to Cloudflare IPs
curl -sI https://centaurion.me/ | head -5
curl -sI https://centaurion.me/strategic-foresight-dashboard | head -5
```

If both return 200/304 from the correct origin (Pages for `/`, Worker for the
dashboard), deployment is healthy.
