# ThumbnailAI Setup Guide

## Prerequisites

1. **Replicate API Account** - Sign up at https://replicate.com
2. **Stripe Account** - Sign up at https://stripe.com
3. **Supabase Account** - Sign up at https://supabase.com
4. **AWS Account** - For S3 storage (optional for MVP)

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
```

### Configure .env

```
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxxxx
```

### Run Backend

```bash
uvicorn main:app --reload --port 8000
```

Visit http://localhost:8000/docs for API documentation.

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
```

### Configure .env

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxx
```

### Run Frontend

```bash
npm run dev
```

Visit http://localhost:3000

## First Thumbnail

1. Enter a prompt like: "A shocked person holding a laptop with money flying out"
2. Select a style (YouTube, Gaming, Tutorial, etc.)
3. Click "Generate Thumbnail"
4. Download your AI-generated thumbnail!

## Deployment

### Vercel (Frontend)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

### Railway/Render (Backend)

1. Create new project
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables
6. Deploy

## Next Steps

- [ ] Set up Stripe subscription tiers
- [ ] Implement user authentication (Supabase Auth)
- [ ] Add usage tracking database tables
- [ ] Configure S3 for image storage
- [ ] Set up custom domain
