# URL-SHORTENER

A simple and efficient URL shortener built with **Python + Flask**.

---

## Features

- Shorten long URLs
- Redirect using short URLs
- Metrics API for top 3 domains
- Unit tests with `pytest`
- Dockerized for easy deployment

---

## Project Structure

```
url_shortener/
├── app.py                    # Main Flask app
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker setup
├── services/
│   └── url_services.py       # Core business logic
├── tests/
│   └── test_app.py           # Unit tests
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/AjayChouhan-code/URL-SHORTENER.git
cd url-shortener
```

### 2. Create & activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Your API will be available at: `http://localhost:5000`

---

##  API Endpoints

###  POST `/shorten`

**Shorten a long URL.**

- **Request Body:**

```json
{
  "url": "https://youtube.com/watch?v=abc123"
}
```

- **Success Response (200):**

```json
{
  "data": {
    "short_url": "http://localhost:5000/abc123"
  },
  "status": 200,
  "message": "Short URL generated successfully",
  "error": false
}
```

- **Error Response (400):**

```json
{
  "data": {},
  "status": 400,
  "message": "URL is required",
  "error": true
}
```

---

###  GET `/<short_url>`

**Redirects to the original URL.**

- Example: `http://localhost:5000/abc123` → Redirects to original URL

---

###  GET `/metrics`

**Returns the top 3 most shortened domain names.**

- **Success Response:**

```json
{
  "youtube.com": 4,
  "udemy.com": 3,
  "wikipedia.org": 2
}
```

---

##  Running Unit Tests

Ensure you're in the project root folder.

```bash
pytest
```

- This will run all tests in the `tests/` folder using Flask's test client and mock services.
- Expected result:

```bash
tests/test_app.py .....                            [100%]
```

> ✅ Coverage includes: shortener, redirect, error handling, metrics.

---

##  Docker Support

###  Build Docker Image

Ensure you're in the root directory with `Dockerfile` present:

```bash
docker build -t url-shortener .
```

###  Run Docker Container

```bash
docker run -p 5000:5000 url-shortener
```

Now access the app via: `http://localhost:5000`

---