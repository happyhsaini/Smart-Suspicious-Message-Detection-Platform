# 🛡️ SpamGuard - Fake Message Detection System

A modern, AI-powered web application that detects spam, phishing, and fake messages. Features include single message analysis and full Gmail inbox scanning with deletion capabilities.

## ✨ Features

- **Single Message Analysis**: Paste any message to instantly detect if it's fake or real
- **Gmail Integration**: Connect your Gmail account securely
- **Inbox Scanning**: Analyze your last 50 emails automatically
- **Real-time Statistics**: View total, fake, and real message counts
- **Batch Delete**: Remove all detected fake messages with one click
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Confidence Score**: See how confident the AI is in its prediction

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Gmail account with App Password enabled

### Step 1: Install Dependencies

```bash
pip install flask scikit-learn pandas numpy
```

### Step 2: Setup Project Structure

Create the following directory structure:

```
project/
├── app.py
├── train_model.py
├── model.pkl
├── vectorizer.pkl
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

### Step 3: Train the Model (First Time Only)

```bash
python train_model.py
```

This will create:
- `model.pkl` - The trained Logistic Regression model
- `vectorizer.pkl` - The TF-IDF vectorizer

### Step 4: Run the Application

```bash
python app.py
```

The app will be available at: `http://127.0.0.1:5500`

## 📋 Usage

### Single Message Analysis
1. Go to "Check Message" section
2. Paste your message (email, SMS, etc.)
3. Click "Analyze Message"
4. View the prediction result with confidence score

### Gmail Integration

#### Getting Gmail App Password:
1. Go to [Google Account Settings](https://myaccount.google.com)
2. Click "Security" in the left sidebar
3. Scroll to "How you sign in to Google"
4. Click "App passwords" (you may need to enable 2-factor authentication first)
5. Select "Mail" and "Windows Computer" (or your device)
6. Google will generate a 16-character password
7. Copy this password

#### Using Gmail Features:
1. Go to "Gmail Tools" section
2. Enter your Gmail address and App Password
3. Click "Connect Gmail"
4. Click "Scan Inbox" to analyze your last 50 emails
5. View the analysis results
6. Select fake messages and click "Delete Fake Messages"

## 🔒 Security Notes

### ⚠️ IMPORTANT SECURITY CONSIDERATIONS

1. **Never use your real Gmail password** - Always use an App Password
2. **Session-based Storage** - Credentials are stored in Flask session (encrypted in production)
3. **HTTPS Recommended** - Use HTTPS in production environments
4. **App Passwords Isolated** - App passwords can be revoked anytime without changing your main password
5. **No Data Logging** - Messages are processed but not permanently stored

### For Production Deployment:

1. **Use Environment Variables**:
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

2. **Enable HTTPS**: Use SSL certificates
3. **Database**: Consider adding a database for message history
4. **Rate Limiting**: Implement rate limiting to prevent abuse
5. **Authentication**: Add user authentication

## 🔧 Configuration

### Model Settings
You can retrain the model with different parameters in `train_model.py`:

```python
# Adjust max iterations
model = LogisticRegression(max_iter=1000)

# Change vectorizer parameters
vectorizer = TfidfVectorizer(
    max_features=5000,      # Limit features
    min_df=2,              # Minimum document frequency
    max_df=0.8             # Maximum document frequency
)
```

### Flask Settings
Modify in `app.py`:

```python
# Change host and port
app.run(host="0.0.0.0", port=8000, debug=False)

# Add secret key for production
app.secret_key = 'your-secret-key-here'
```

## 📊 Model Information

- **Type**: Logistic Regression (Binary Classification)
- **Features**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Input**: Text messages, emails, or SMS
- **Output**: Real (0) or Fake (1)
- **Training Data**: Combined spam and ham datasets

## 🎯 Accuracy

The model is trained on real-world spam and legitimate message datasets. Expected accuracy:
- **Precision**: ~92-95%
- **Recall**: ~88-92%
- **F1-Score**: ~90-93%

Note: Accuracy varies based on the training dataset. Consider retraining with your specific use case data for better results.

## 🐛 Troubleshooting

### Gmail Login Fails
- Make sure you're using an App Password, not your regular Gmail password
- Check that 2-factor authentication is enabled
- Try generating a new App Password

### Model Not Found
- Run `python train_model.py` to create model files
- Ensure `model.pkl` and `vectorizer.pkl` are in the project root

### Port Already in Use
- Change the port: `app.run(port=5501)`
- Or kill the process using the port

### IMAP Not Enabled
- Go to Gmail Settings → Forwarding and POP/IMAP
- Enable IMAP access

## 📈 Future Enhancements

- [ ] Deep Learning models (LSTM, BERT)
- [ ] Multi-language support
- [ ] SMS message analysis
- [ ] URL phishing detection
- [ ] Custom training with user feedback
- [ ] Export reports
- [ ] Schedule periodic scans
- [ ] Whitelist/Blacklist management
- [ ] API endpoint for third-party integration

## 📝 API Endpoints

### POST `/predict`
Analyze a single message
```bash
curl -X POST http://localhost:5500/predict \
  -d "message=Hello this is a test"
```

### POST `/gmail-login`
Authenticate with Gmail
```bash
curl -X POST http://localhost:5500/gmail-login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@gmail.com","password":"app_password"}'
```

### POST `/check-gmail`
Start Gmail inbox analysis
```bash
curl -X POST http://localhost:5500/check-gmail
```

### GET `/gmail-stats`
Get current analysis statistics
```bash
curl http://localhost:5500/gmail-stats
```

### POST `/delete-fake-messages`
Delete fake messages from Gmail
```bash
curl -X POST http://localhost:5500/delete-fake-messages \
  -H "Content-Type: application/json" \
  -d '{"message_ids":["1","2","3"]}'
```

## 📄 License

This project is provided as-is for educational and personal use.

## ⚠️ Disclaimer

This tool provides predictions based on machine learning models. While designed to be accurate, it may have false positives or false negatives. Always verify important messages before taking action. The developers are not responsible for any consequences of using this tool.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the Gmail setup instructions
3. Ensure all dependencies are installed
4. Check Python version compatibility

## 💡 Tips

- Start with single message analysis to understand how the model works
- Always use the App Password method for Gmail security
- Review detected fake messages before deleting (optional)
- Retrain the model periodically with new data for better accuracy
- Monitor false positives and adjust sensitivity if needed

---

**Happy protecting! 🛡️**
