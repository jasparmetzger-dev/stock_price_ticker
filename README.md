# 📈 Stock Price Ticker

A full-stack stock portfolio tracker with real-time price fetching, SMS alerts, and user authentication. Built with FastAPI, PostgreSQL, and vanilla HTML/CSS/JS. Deployed on Railway.

## Features

- User registration and login
- Create portfolios with any stock tickers and custom weightings
- Real-time price fetching via yfinance
- SMS alerts when a portfolio hits a target price (Twilio)
- Background scheduler to check prices automatically
- Clean frontend UI with login state management

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Auth:** passlib + bcrypt
- **Prices:** yfinance
- **Alerts:** Twilio SMS, APScheduler
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Deployment:** Railway
- **Local Dev:** Docker + docker-compose

## Project Structure

```
stock_price_ticker/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB connection
│   ├── routers/
│   │   ├── auth.py          # Register, login
│   │   ├── portfolios.py    # Create portfolios
│   │   └── alerts.py        # Create alerts
│   ├── services/
│   │   ├── scheduler.py     # Background price checker
│   │   └── sms.py           # Twilio SMS sender
│   └── static/
│       └── index.html       # Frontend
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create a new user |
| POST | `/login` | Login and get user ID |
| POST | `/portfolio` | Create a portfolio |
| POST | `/portfolio/{id}/alerts` | Set a price alert |

## Local Development

### With Docker (recommended)

```bash
# Clone the repo
git clone https://github.com/yourusername/stock_price_ticker.git
cd stock_price_ticker

# Copy and fill in your env vars
cp .env.example .env

# Start everything
docker-compose up --build
```

App runs at `http://localhost:8000`

### Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

Create a `.env` file in the project root:

```
DB_URL=postgresql://postgres:password@localhost:5432/stock_ticker
SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

## Deployment

Deployed on Railway. Each push to `main` triggers a redeploy.

Environment variables are set in Railway's Variables tab per service.

---

## Roadmap

### JWT Authentication
Currently login returns a `user_id` with no session token. The plan is to add proper JWT tokens so protected routes require a valid token in the `Authorization` header.

```
POST /login → returns { access_token, token_type, user_id, username }
```

All portfolio and alert endpoints will then require:
```
Authorization: Bearer <token>
```

### GET Endpoints + Portfolio Value

Add read endpoints so the frontend can display live data:

```
GET /portfolio/{user_id}         → list user's portfolios
GET /portfolio/{id}/value        → current portfolio value (fetches live prices)
GET /portfolio/{id}/alerts       → list alerts for a portfolio
```

The portfolio value endpoint will:
1. Fetch each holding's current price via yfinance
2. Multiply by weight
3. Return a weighted portfolio value and per-ticker breakdown

### Frontend Updates (after above)
- Portfolio page shows existing portfolios with live values
- Alerts page shows existing alerts with status (active/triggered)
- Auto-refresh portfolio values every 60 seconds