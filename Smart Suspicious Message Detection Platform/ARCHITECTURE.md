# 🏗️ System Architecture & Data Flow

## 📋 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT SIDE                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Web Browser                        │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         Beautiful Dashboard (HTML)             │  │   │
│  │  │  • Message input form                          │  │   │
│  │  │  • Gmail login section                         │  │   │
│  │  │  • Statistics display                          │  │   │
│  │  │  • Message list view                           │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │    Modern UI Styling (CSS)                     │  │   │
│  │  │  • Dark theme with gradients                   │  │   │
│  │  │  • Responsive layout                           │  │   │
│  │  │  • Smooth animations                           │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Interactive Features (JavaScript)             │  │   │
│  │  │  • Form submission handling                    │  │   │
│  │  │  • API requests                                │  │   │
│  │  │  • Real-time updates                           │  │   │
│  │  │  • Notifications                               │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                    HTTP/HTTPS Requests
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVER SIDE                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Flask Web Framework (app.py)                │   │
│  │                                                      │   │
│  │  Routes:                                            │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ POST /predict                               │   │   │
│  │  │ • Receive message                           │   │   │
│  │  │ • Vectorize text                            │   │   │
│  │  │ • Predict (fake/real)                       │   │   │
│  │  │ • Return JSON result                        │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ POST /gmail-login                           │   │   │
│  │  │ • Authenticate with IMAP                    │   │   │
│  │  │ • Store in session                          │   │   │
│  │  │ • Return success/error                      │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ POST /check-gmail                           │   │   │
│  │  │ • Fetch emails from IMAP                    │   │   │
│  │  │ • Process in background                     │   │   │
│  │  │ • Analyze each email                        │   │   │
│  │  │ • Update statistics                         │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ GET /gmail-stats                            │   │   │
│  │  │ • Return current progress                   │   │   │
│  │  │ • Return message list                       │   │   │
│  │  │ • Return statistics                         │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ POST /delete-fake-messages                  │   │   │
│  │  │ • Delete selected emails from IMAP          │   │   │
│  │  │ • Expunge deleted items                     │   │   │
│  │  │ • Return count of deleted                   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      Machine Learning Models                         │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ TF-IDF Vectorizer (vectorizer.pkl)         │   │   │
│  │  │ • Load text                                 │   │   │
│  │  │ • Extract features                         │   │   │
│  │  │ • Create feature vectors                   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ Logistic Regression (model.pkl)             │   │   │
│  │  │ • Receive feature vectors                   │   │   │
│  │  │ • Compute probability                       │   │   │
│  │  │ • Return prediction (0/1)                   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      External Integrations                           │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ IMAP Gmail Server                           │   │   │
│  │  │ • Connect via IMAP4_SSL                    │   │   │
│  │  │ • Fetch emails                             │   │   │
│  │  │ • Delete emails                            │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagrams

### 1️⃣ Single Message Analysis Flow

```
User Input (Text Message)
    │
    ▼
JavaScript Form Handler
    │
    ▼
POST /predict (Flask Route)
    │
    ├─► Validate input
    │
    ├─► Extract message text
    │
    ├─► TF-IDF Vectorizer
    │   └─► Convert text to feature vector
    │
    ├─► Logistic Regression Model
    │   └─► predict([features])
    │       └─► Returns: 0 (real) or 1 (fake)
    │
    ├─► predict_proba([features])
    │   └─► Returns: [prob_real, prob_fake]
    │
    ├─► Format JSON response
    │   └─► {
    │       result: "Real/Fake",
    │       confidence: "95%",
    │       is_fake: true/false
    │     }
    │
    ▼
Send Response to Browser
    │
    ▼
JavaScript Display Result
    │
    ├─► Color code result
    ├─► Show confidence score
    ├─► Add warning if fake
    └─► Smooth animation
```

### 2️⃣ Gmail Authentication Flow

```
User Credentials (Email + App Password)
    │
    ▼
JavaScript Form Submit
    │
    ▼
POST /gmail-login (Flask Route)
    │
    ├─► Validate inputs
    │
    ├─► IMAP4_SSL("imap.gmail.com")
    │   └─► Create secure connection
    │
    ├─► mail.login(email, password)
    │   └─► Authenticate user
    │
    ├─► Test connection (if successful)
    │   │
    │   ├─► Store in Flask session
    │   │   └─► session['gmail_email']
    │   │   └─► session['gmail_password']
    │   │
    │   └─► Return success response
    │
    └─► Handle errors
        └─► Invalid credentials
        └─► Network error
        └─► IMAP disabled
```

### 3️⃣ Gmail Inbox Scanning Flow

```
User Clicks "Scan Inbox"
    │
    ▼
POST /check-gmail
    │
    ├─► Validate session
    │
    ├─► Start Background Thread
    │   │
    │   └─► process_gmail_messages()
    │       │
    │       ├─► Connect to IMAP
    │       │
    │       ├─► Select "INBOX"
    │       │
    │       ├─► Fetch all message IDs
    │       │
    │       ├─► Loop through last 50 emails
    │       │   │
    │       │   ├─► For each email:
    │       │   │   │
    │       │   │   ├─► Fetch raw email data
    │       │   │   │
    │       │   │   ├─► Parse email headers
    │       │   │   │   └─► Subject
    │       │   │   │   └─► From
    │       │   │   │   └─► Date
    │       │   │   │
    │       │   │   ├─► Extract email body
    │       │   │   │
    │       │   │   ├─► Combine subject + body
    │       │   │   │
    │       │   │   ├─► TF-IDF Vectorize
    │       │   │   │
    │       │   │   ├─► Model Predict
    │       │   │   │   └─► prediction (0/1)
    │       │   │   │   └─► probability
    │       │   │   │
    │       │   │   ├─► Store result:
    │       │   │   │   ├─► message_id
    │       │   │   │   ├─► from_addr
    │       │   │   │   ├─► subject
    │       │   │   │   ├─► is_fake
    │       │   │   │   └─► confidence
    │       │   │   │
    │       │   │   └─► Update progress
    │       │   │       └─► progress = (current/total)*100
    │       │   │
    │       │   └─► Update counters
    │       │       ├─► total_messages++
    │       │       ├─► fake_messages++ (if fake)
    │       │       └─► real_messages++ (if real)
    │       │
    │       ├─► Close IMAP connection
    │       │
    │       └─► Set processing = False
    │
    ▼
Return "Scan Started" Immediately
    │
    ▼
JavaScript Polling Loop
    │
    ├─► GET /gmail-stats (every 500ms)
    │   │
    │   └─► Receive:
    │       ├─► progress: 0-100
    │       ├─► total_messages
    │       ├─► fake_messages
    │       ├─► real_messages
    │       ├─► messages_data: [...]
    │       └─► processing: true/false
    │
    ├─► Update Progress Bar
    ├─► Update Statistics
    ├─► Display Message List
    │
    └─► When processing=False
        ├─► Stop polling
        ├─► Enable delete button
        └─► Show completion message
```

### 4️⃣ Fake Message Deletion Flow

```
User Selects Fake Messages & Clicks Delete
    │
    ▼
JavaScript Confirmation Dialog
    │
    ├─► Show warning: "Delete X message(s)?"
    │
    ▼
User Confirms
    │
    ▼
POST /delete-fake-messages
    │
    ├─► Send message_ids list
    │
    ├─► Validate session
    │
    ├─► Connect to IMAP
    │
    ├─► For each message_id:
    │   │
    │   ├─► mail.store(msg_id, '+FLAGS', '\\Deleted')
    │   │   └─► Mark as deleted
    │   │
    │   └─► deleted_count++
    │
    ├─► mail.expunge()
    │   └─► Permanently delete marked messages
    │
    ├─► Close IMAP connection
    │
    ├─► Return response:
    │   ├─► success: true
    │   ├─► deleted_count: X
    │   └─► message: "Successfully deleted X..."
    │
    ▼
JavaScript Display Result
    │
    ├─► Show success notification
    │
    ├─► Clear selections
    │
    └─► Auto-rescan inbox
```

---

## 🗂️ Component Interaction

```
┌──────────────┐
│   Frontend   │
│   (Browser)  │
└──────────────┘
       │ HTTP/JSON
       │
    ┌──▼──┐
    │Flask│ ◄─────┐
    │ App │       │ Session
    └──┬──┘       │
       │          │
    ┌──▼────────────────┐
    │ AI Models         │
    │ • Vectorizer      │
    │ • Model           │
    └──┬─────────────────┘
       │
       ├──────────┬──────────┐
       │          │          │
    ┌──▼──┐   ┌──▼───┐   ┌──▼────┐
    │IMAP │   │Data  │   │Static │
    │Gmail│   │Files │   │Files  │
    └─────┘   └──────┘   └───────┘
```

---

## 📦 Data Structures

### Message Object
```python
message_info = {
    'id': 'mail_id_123',              # Email ID
    'from': 'sender@example.com',     # Sender address
    'subject': 'Hello World',         # Email subject
    'is_fake': True,                  # Prediction (True/False)
    'confidence': '95.67%',           # Confidence score
    'timestamp': '2024-01-15T10:30Z'  # When analyzed
}
```

### Gmail Stats Object
```python
gmail_stats = {
    'total_messages': 42,             # Processed count
    'fake_messages': 8,               # Detected spam
    'real_messages': 34,              # Legitimate
    'processing': False,              # Scanning status
    'progress': 100,                  # 0-100%
    'messages_data': [...]            # Array of message_info
}
```

### Prediction Response
```json
{
    "result": "Fake Message",
    "confidence": "94.32%",
    "is_fake": true
}
```

---

## 🔐 Security Layers

```
Layer 1: Browser
├─► Input validation
├─► XSS prevention (HTML escaping)
└─► CSRF tokens ready

Layer 2: Flask App
├─► Input sanitization
├─► Session encryption
├─► Error handling
└─► No password logging

Layer 3: IMAP
├─► SSL/TLS encryption
├─► Secure authentication
└─► No credentials in memory
```

---

## ⚡ Performance Optimization

```
Frontend:
├─► CSS animations (GPU accelerated)
├─► Lazy loading
├─► Debounced requests
└─► Caching responses

Backend:
├─► Background threading
├─► Model caching in memory
├─► Vectorizer reuse
└─► Connection pooling ready

Model:
├─► TF-IDF sparse matrices
├─► Vectorizer fitting one-time
└─► Predictions <100ms
```

---

## 🔄 State Management

```
Client State:
├─► Form inputs
├─► Authentication status
├─► Current stats
├─► Message list
└─► Selected items

Server State:
├─► Session data
├─► IMAP connection
├─► Gmail credentials
├─► Processing status
└─► Message queue
```

---

## 🧪 Testing Flow

```
Unit Tests:
├─► Text vectorization
├─► Model prediction
└─► Email parsing

Integration Tests:
├─► Form submission
├─► Gmail authentication
├─► Email deletion
└─► Stats update

End-to-End Tests:
├─► Full workflow
├─► Error scenarios
└─► Performance
```

---

**Architecture designed for scalability, security, and user experience! 🚀**
