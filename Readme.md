# Scalable URL Shortener Service

## **Overview**
This project is a **scalable URL shortener service** built with Python and Flask, similar to Bitly or TinyURL. It allows users to:
- Shorten long URLs into short aliases.
- Retrieve the original URL from a shortened alias.
- Track usage statistics for each shortened URL.
- Set an optional expiration time for shortened URLs.
- Expose these functionalities via a REST API.

---
## **High-Level Design**
### **Architecture Overview**
The application follows a **RESTful architecture** with the following key components:

- **Flask API**: Handles HTTP requests for URL shortening, expansion, and statistics.
- **SQLite Database**: Stores mappings of shortened URLs to original URLs, along with access statistics.
- **Docker Containerization**: Enables easy deployment and scalability.
- **Logging & Monitoring**: Basic logging implemented for debugging and tracking API calls.

### **Database Schema**
The application uses an SQLite database with the following schema:

| Column       | Type     | Description                                    |
|-------------|---------|------------------------------------------------|
| `short`     | TEXT    | Unique short alias for the URL (Primary Key)  |
| `long`      | TEXT    | Original long URL                              |
| `created_at`| INTEGER | Timestamp when the URL was created            |
| `expires_at`| INTEGER | Optional expiration timestamp                  |
| `access_count` | INTEGER | Number of times the short URL was accessed |

---
## **Setup Instructions**

### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### **2. Create a Virtual Environment & Install Dependencies**
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```

### **3. Initialize the Database**
Run the following Python script to set up the database:
```sh
python init_db.py
```

### **4. Start the Flask Application**
```sh
python app.py
```
**Expected Output:**
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

---
## **API Guide**
### **1. Shorten a URL**
**Endpoint:** `POST /shorten`
```sh
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"long_url": "https://example.com"}'
```
**Response:**
```json
{"short_url": "abc123", "expires_at": null}
```

### **2. Expand a Shortened URL**
**Endpoint:** `GET /expand/<short_code>`
```sh
curl -X GET http://127.0.0.1:5000/expand/abc123
```
**Response:**
```json
{"long_url": "https://example.com"}
```

### **3. Get URL Usage Statistics**
**Endpoint:** `GET /stats/<short_code>`
```sh
curl -X GET http://127.0.0.1:5000/stats/abc123
```
**Response:**
```json
{"short_url": "abc123", "long_url": "https://example.com", "access_count": 5}
```

---
## **Deployment Instructions**
### **1. Build the Docker Image**
```sh
docker build -t url-shortener .
```

### **2. Run the Docker Container**
```sh
docker run -p 5000:5000 url-shortener
```

### **3. Verify API is Running**
Check if the API is accessible via cURL:
```sh
curl -X GET http://127.0.0.1:5000/health
```
If everything is running correctly, you should receive:
```json
{"status": "ok"}
```

---
## **Testing**
Run unit tests using **pytest**:
```sh
pytest -v test_url_shortener.py
```

---
## **Future Improvements**
- **Switch to PostgreSQL or MySQL** for better scalability.
- **Add Redis caching** for faster lookups.
- **Integrate authentication** to track user-specific URLs.
- **Rate limiting** to prevent abuse.

