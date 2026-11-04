# Documentation Site Deployment

The documentation at [https://ethereum-wallet-toolkit.modelcontextprotocol.name](https://ethereum-wallet-toolkit.modelcontextprotocol.name) is the static `docs/` folder hosted on Cloudflare Pages.

| Item | Value |
|------|-------|
| Host | Cloudflare Pages, project `ethereum-wallet-toolkit` |
| Production URL | `https://ethereum-wallet-toolkit.modelcontextprotocol.name` |
| Headers | `docs/_headers` (security headers; `.md` files served as readable text) |
| DNS | Proxied CNAME in the `modelcontextprotocol.name` zone to `ethereum-wallet-toolkit.pages.dev` |

## Deploy

Export `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`, then from the repository root:

```bash
npx wrangler@4 pages deploy docs --project-name=ethereum-wallet-toolkit --branch=main
```

Deploys are manual. GitHub Actions is not used for this site.

## Verify

```bash
curl -sI https://ethereum-wallet-toolkit.modelcontextprotocol.name | head -1   # HTTP/2 200
```

## Rollback

Cloudflare dashboard → Workers & Pages → ethereum-wallet-toolkit → Deployments → pick an earlier production deployment → Rollback.
