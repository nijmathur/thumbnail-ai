# ThumbnailAI - AI-Powered YouTube Thumbnail Generator

**Automated Business Scout - Priority #1 Implementation**

AI-powered thumbnail generation service with face consistency for personal branding.

---

## Features

- **AI Thumbnail Generation** - FLUX.1 model for high-quality thumbnails
- **Face Consistency** - InsightFace integration for personal branding
- **Text Rendering** - Ideogram API for text-heavy thumbnails
- **A/B Testing** - Generate multiple variations for CTR optimization
- **Bulk Generation** - Create 10-15 concepts per video at $0.19/image

---

## Tech Stack

### Frontend
- Next.js 14 + Tailwind CSS
- Stripe for subscription billing
- Vercel for hosting

### Backend
- Python FastAPI
- Replicate API (FLUX.1)
- InsightFace API (face consistency)
- Supabase (PostgreSQL)
- AWS S3 + CloudFront

---

## Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| Starter | $19/mo | 50 thumbnails, basic templates, 720p |
| Pro | $29/mo | 150 thumbnails, face consistency, 1080p, A/B testing |
| Business | $49/mo | 400 thumbnails, priority generation, 4K, analytics |
| Enterprise | $99/mo | Unlimited, API access, white-label, dedicated support |

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Replicate API key
- Stripe account
- Supabase account

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Add your API keys
npm run dev
```

---

## Project Status

- [x] Project initialization
- [ ] Backend API setup
- [ ] Frontend UI
- [ ] Replicate API integration
- [ ] Face consistency (InsightFace)
- [ ] Stripe billing
- [ ] Deployment

---

## License

MIT

---

**Feasibility Score:** 8.2/10
**Startup Capital:** $78K-138K
**Time to Break-Even:** 6-10 months
**Target Customers:** 50M+ content creators
