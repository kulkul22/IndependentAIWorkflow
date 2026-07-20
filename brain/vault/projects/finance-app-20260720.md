# FinanceApp

Hybrid workflow run `run_20260720_110326` built a Vietnamese local-first personal finance MVP at `D:\Projects\FinanceApp`.

Architecture: React 19 + Vite frontend, Hono API, SQLite/better-sqlite3 with Drizzle ORM, Zod validation. Key guarantees include integer minor-unit money, foreign-key integrity, serialized writes, atomic backup restore, localhost CORS, rate limiting, and security headers.

Final gates: ESLint pass, TypeScript pass, 65/65 tests pass, production web/server build pass. Playwright smoke coverage requires a running app and `E2E_BASE_URL`.

Important audit lesson: mocked repository backup tests hid a missing production replacement implementation. The final audit caught this and the restore path was changed to one SQLite transaction.
