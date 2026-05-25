# 🔗 URL Shortener API

A production-ready URL Shortener built using Flask, PostgreSQL, Redis, Docker, and Render deployment.

## 🚀 Live Demo

https://urlshortner-t31v.onrender.com

---

# ✨ Features

- Shorten long URLs
- Base62 encoded short links
- PostgreSQL database integration
- Redis caching for faster redirects
- Click analytics
- REST API architecture
- Docker support
- Cloud deployment using Render
- Environment variable support

---

# 🛠️ Tech Stack

- Python
- Flask
- PostgreSQL
- Redis
- SQLAlchemy
- Docker
- Render

---

# 📂 Project Structure

```bash
url-shortener/
│
├── app.py
├── models.py
├── redis_client.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
└── routes/
    └── __init__.py
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/XxGtocxX/urlShortner.git
cd urlShortner
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🐘 PostgreSQL Setup

Create database:

```sql
CREATE DATABASE url_shortener;
```

Environment variable:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener
```

---

# 🔴 Redis Setup

Run Redis locally using Docker:

```bash
docker run -p 6379:6379 redis
```

---

# ▶️ Run Application

```bash
python app.py
```

Application runs on:

```txt
http://127.0.0.1:5000
```

---

# 🐳 Docker Setup

## Build Docker Image

```bash
docker build -t url-shortener .
```

## Run Docker Container

```bash
docker run -p 5000:5000 url-shortener
```

---

# 📡 API Endpoints

## 🔹 Shorten URL

### POST `/shorten`

### Request

```json
{
    "long_url": "https://youtube.com"
}
```

### Response

```json
{
    "short_url": "https://urlshortner-t31v.onrender.com/b"
}
```

---

## 🔹 Redirect URL

### GET `/<short_code>`

Example:

```txt
https://urlshortner-t31v.onrender.com/b
```

Redirects to original URL.

---

## 🔹 Analytics

### GET `/stats/<short_code>`

Example:

```txt
https://urlshortner-t31v.onrender.com/stats/b
```

### Response

```json
{
    "long_url": "https://youtube.com",
    "short_code": "b",
    "clicks": 5
}
```

---

# ☁️ Deployment

Deployed on Render using:

- Render Web Service
- Render PostgreSQL
- Environment Variables

---

# 📈 Future Improvements

- Custom aliases
- Link expiration
- QR code generation
- JWT authentication
- Rate limiting
- User dashboard
- Swagger documentation

---

# 👨‍💻 Author

Debanuj Kumar De

GitHub:
https://github.com/XxGtocxX
