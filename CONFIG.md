# ⚙️ Configuration Guide

Customize SpamGuard for your specific needs

## 🎨 UI Configuration

### Change Colors
Edit `static/style.css` root variables:

```css
:root {
    --primary-color: #6366f1;        /* Main color */
    --secondary-color: #ec4899;      /* Accent color */
    --danger-color: #ef4444;         /* Danger color */
    --success-color: #10b981;        /* Success color */
    --background: #0f172a;           /* Background */
    --surface: #1e293b;              /* Card background */
}
```

### Change Fonts
Replace font family in `static/style.css`:

```css
body {
    font-family: 'Your Font', Fallback, sans-serif;
}
```

Popular choices:
- `'Poppins'` - Modern, friendly
- `'Roboto'` - Clean, professional
- `'Courier New'` - Monospace, techy

## 🤖 Model Configuration

### Adjust Vectorizer Settings

In `train_model.py`, modify the TfidfVectorizer:

```python
vectorizer = TfidfVectorizer(
    max_features=5000,        # Number of features (higher = more detailed)
    min_df=1,                 # Min document frequency (remove rare words)
    max_df=0.95,              # Max document frequency (remove common words)
    ngram_range=(1, 2),       # Use 1-word and 2-word features
    lowercase=True,           # Convert to lowercase
    stop_words='english',     # Remove common words
    token_pattern=r'\b\w{2,}\b'  # Minimum 2 characters
)
```

### Adjust Model Settings

```python
model = LogisticRegression(
    max_iter=1000,            # Training iterations
    solver='lbfgs',           # Algorithm type
    random_state=42,          # Reproducibility
    C=1.0,                    # Regularization strength (lower = stronger)
    class_weight='balanced'   # Handle imbalanced data
)
```

## 🚀 Flask Configuration

### Change Port and Host

Edit `app.py`:

```python
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",      # 127.0.0.1 = localhost only
                             # 0.0.0.0 = accessible from network
        port=5500,           # Any port 1024-65535
        debug=False          # False for production
    )
```

### Change Secret Key

```python
app.secret_key = 'your-secret-key-here'
```

## 📊 Data Configuration

### Train/Test Split Ratio

In `train_model.py`:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,           # 20% for testing, 80% for training
    random_state=42,
    stratify=y
)
```

### Gmail Scanning Configuration

In `app.py`, modify how many emails to check:

```python
for idx, mail_id in enumerate(mail_ids[-50:]):  # Last 50 emails
    # Processing code
```

Change `50` to any number:
- Smaller (10-20): Faster scanning
- Larger (100+): More thorough

## 🔐 Security Configuration

### For Production:

1. **Enable HTTPS**:
```python
from flask_talisman import Talisman
Talisman(app)
```

2. **Add CORS**:
```python
from flask_cors import CORS
CORS(app)
```

3. **Rate Limiting**:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: 'limit')
@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    pass
```

4. **Content Security Policy**:
```python
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

## 📈 Performance Tuning

### Caching Results

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def predict_message(message_text):
    # Cached predictions
    pass
```

### Batch Processing

Process multiple messages at once:

```python
def batch_predict(messages):
    data = vectorizer.transform(messages)
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)
    return predictions, probabilities
```

## 🎯 Feature Configuration

### Adjust Confidence Threshold

In `static/script.js`:

```javascript
if (confidence < 0.6) {
    // Low confidence
} else if (confidence < 0.8) {
    // Medium confidence
} else {
    // High confidence
}
```

### Change Notification Duration

```javascript
setTimeout(() => {
    notification.remove();
}, 3000);  // 3 seconds
```

## 📱 Responsive Design

Adjust mobile breakpoints in `static/style.css`:

```css
@media (max-width: 1024px) {
    /* Tablet devices */
}

@media (max-width: 768px) {
    /* Mobile devices */
}
```

## 🗄️ Database Integration (Optional)

Add SQLite for message history:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000))
    prediction = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
```

## 📝 Logging Configuration

Add logging for debugging:

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info('Application started')
```

## 🌐 Deployment Configuration

### For Heroku:
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

### For AWS:
1. Use Elastic Beanstalk
2. Configure in `.ebextensions/python.config`

### For Docker:
Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📊 Monitor Performance

Add metrics collection:

```python
from time import time

@app.before_request
def log_request():
    request.start_time = time()

@app.after_request
def log_response(response):
    duration = time() - request.start_time
    print(f"Request took {duration:.2f}s")
    return response
```

## 🔄 Auto-Retraining

Schedule periodic model retraining:

```python
from apscheduler.schedulers.background import BackgroundScheduler

def retrain_model():
    # Run train_model.py periodically
    os.system('python train_model.py')

scheduler = BackgroundScheduler()
scheduler.add_job(func=retrain_model, trigger="interval", days=7)
scheduler.start()
```

---

## 📚 Configuration Examples

### Aggressive Spam Detection
- Lower max_df to remove common words
- Higher min_df to focus on distinguishing words
- Increase max_features for more nuance

### Sensitive Inbox Scanning
- Check all emails: `mail_ids[-1000:]`
- Lower confidence threshold
- More frequent rescans

### Fast Processing
- Reduce max_features: `max_features=2000`
- Limit Gmail emails: `mail_ids[-10:]`
- Disable debug mode

---

**Need help? Check README.md or test locally first!**
