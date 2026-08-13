# SupplyMind V1 deployment

Production needs four external resources: managed PostgreSQL, Pinecone, OpenAI, and a public backend/frontend host.

Recommended simple graduation setup:
- Backend: Render/Railway/Fly.io using `Dockerfile.api`
- PostgreSQL: managed PostgreSQL from the same provider
- Frontend: Vercel from `apps/web`
- Vector DB: Pinecone

Backend environment: copy `.env.e2e.example` values into the host's secret manager. Never upload `.env`.
Set `CORS_ORIGINS` to the deployed frontend URL.

Frontend environment:
`VITE_API_BASE_URL=https://supplymind-ai.onrender.com/api`

Release checks:
1. `alembic upgrade head`
2. `/health` returns 200
3. `/api/health` shows PostgreSQL connected and champion model loaded
4. create one parcel prediction
5. verify Dashboard updates
6. ask assistant about that shipment
7. verify Event Monitor and Semantic Search
8. run `npm run build`
