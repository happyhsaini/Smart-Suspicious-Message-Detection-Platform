# ✅ Setup Checklist & Verification Guide

Use this checklist to ensure everything is properly configured before running the application.

---

## 🔧 Prerequisites Check

- [ ] **Python Installed**
  ```bash
  python --version  # Should be 3.8+
  ```

- [ ] **pip Available**
  ```bash
  pip --version
  ```

- [ ] **Git (Optional but recommended)**
  ```bash
  git --version
  ```

- [ ] **Internet Connection** (for Gmail features)

---

## 📁 File Structure Verification

In your project directory, verify these files exist:

### Root Directory Files
- [ ] `app.py` - Flask application
- [ ] `train_model.py` - Model training script
- [ ] `requirements.txt` - Python dependencies
- [ ] `combined_data.csv` - Training data (required)
- [ ] `README.md` - Full documentation
- [ ] `QUICKSTART.md` - Quick setup guide
- [ ] `CONFIG.md` - Configuration options
- [ ] `PROJECT_SUMMARY.md` - Project overview
- [ ] `ARCHITECTURE.md` - System architecture
- [ ] `SETUP_CHECKLIST.md` - This file

### Templates Directory
- [ ] `templates/` - Folder exists
- [ ] `templates/index.html` - Web interface

### Static Directory
- [ ] `static/` - Folder exists
- [ ] `static/style.css` - Styling
- [ ] `static/script.js` - JavaScript logic

### Generated Files (Created During Setup)
- [ ] `model.pkl` - Will be created
- [ ] `vectorizer.pkl` - Will be created

**Verification Command:**
```bash
# Windows
dir /s

# Linux/Mac
ls -la
find . -type f -name "*.py" -o -name "*.html" -o -name "*.css" -o -name "*.js"
```

---

## 📦 Dependencies Installation

### Step 1: Install Requirements
- [ ] Run: `pip install -r requirements.txt`
- [ ] Should see successful installation messages
- [ ] No errors reported

### Step 2: Verify Installation
```bash
pip list
# Verify these are installed:
# - Flask
# - scikit-learn
# - pandas
# - numpy
```

### Step 3: Test Imports (Optional)
```bash
python -c "import flask; import sklearn; import pandas; print('All imports successful!')"
```

---

## 📊 Training Data Setup

### Step 1: Prepare CSV File
- [ ] File named `combined_data.csv` exists
- [ ] Located in project root directory
- [ ] Contains at least 2 columns:
  - [ ] `label` column (values: `ham` or `spam`)
  - [ ] `text` or `message` column (actual message content)

### Step 2: Verify CSV Format
```bash
# Windows
type combined_data.csv | head

# Linux/Mac
head combined_data.csv
```

Should show header row and sample data like:
```
label,text
ham,Hello how are you
spam,Congratulations you won
```

### Step 3: CSV Requirements
- [ ] At least 50 messages (minimum)
- [ ] Recommended 500+ for better accuracy
- [ ] Good balance between ham and spam
- [ ] Encoding: UTF-8 or Latin-1
- [ ] No special characters breaking the format

### Step 4: Data Quality Check
```python
import pandas as pd
df = pd.read_csv("combined_data.csv")
print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"Null values:\n{df.isnull().sum()}")
print(f"Unique labels: {df['label'].unique()}")
```

---

## 🤖 Model Training

### Step 1: Run Training
- [ ] Execute: `python train_model.py`
- [ ] Watch for output messages
- [ ] See training progress

### Step 2: Training Completion
Check for successful completion messages:
- [ ] "✓ Dataset loaded: XXX messages"
- [ ] "✓ Vectorization complete"
- [ ] "Model training complete"
- [ ] "✅ Training Complete!"

### Step 3: Verify Model Files
- [ ] `model.pkl` created (check file size > 1MB)
- [ ] `vectorizer.pkl` created (check file size > 1MB)

**Verification Command:**
```bash
# Windows
dir model.pkl vectorizer.pkl

# Linux/Mac
ls -lh model.pkl vectorizer.pkl
```

### Step 4: Test Model Manually (Optional)
```python
import pickle
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
test_msg = "Congratulations you won money"
vec = vectorizer.transform([test_msg])
pred = model.predict(vec)
print(f"Prediction: {pred[0]}")  # Should be 1 (fake)
```

---

## 🌐 Flask Application Test

### Step 1: Start Application
- [ ] Execute: `python app.py`
- [ ] See: "Running on http://127.0.0.1:5500"
- [ ] No error messages

### Step 2: Check Console Output
Should see:
```
* Running on http://127.0.0.1:5500
* Debug mode: on
* WARNING: This is a development server...
```

### Step 3: Application Running
- [ ] Terminal shows running status
- [ ] No errors in console
- [ ] Can stop with Ctrl+C

---

## 🌍 Browser Access

### Step 1: Open Website
- [ ] Open browser (Chrome, Firefox, Safari, Edge)
- [ ] Go to: `http://127.0.0.1:5500`
- [ ] Page loads without errors

### Step 2: Verify UI Elements
- [ ] Logo "SpamGuard" visible
- [ ] Navigation menu works
- [ ] Hero section displays
- [ ] Statistics cards show 0s
- [ ] "Check a Message" section visible
- [ ] "Gmail Tools" section visible

### Step 3: Test Message Analysis
- [ ] Type test message: "Congratulations you won 1000 rupees click now"
- [ ] Click "Analyze Message"
- [ ] Get result (should say "Fake Message")

### Step 4: Verify Styling
- [ ] Dark theme applied
- [ ] Colors visible (blue, pink)
- [ ] Smooth animations work
- [ ] Mobile responsive (resize browser)

---

## 🔐 Gmail Integration Test (Optional)

### Step 1: Enable 2-Factor Authentication
- [ ] Go to: https://myaccount.google.com/security
- [ ] Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
- [ ] Go to: https://myaccount.google.com/apppasswords
- [ ] Select "Mail" and "Windows Computer"
- [ ] Google generates 16-character password
- [ ] Copy the password

### Step 3: Test Gmail Connection
- [ ] In website, go to "Gmail Tools" section
- [ ] Enter your Gmail address
- [ ] Paste the App Password
- [ ] Click "Connect Gmail"
- [ ] Should see "Gmail connected successfully!"

### Step 4: Test Inbox Scan
- [ ] Click "Scan Inbox"
- [ ] Watch progress bar move
- [ ] See messages appear in list
- [ ] Check statistics update
- [ ] Delete button becomes enabled if fake messages found

### Step 5: Test Message Deletion (CAREFULLY!)
- [ ] Select one fake message checkbox
- [ ] Click "Delete Fake Messages"
- [ ] Confirm deletion
- [ ] Should see success message
- [ ] Check Gmail account to verify deletion

---

## ⚡ Performance Verification

### Single Message Analysis
- [ ] Response time < 2 seconds
- [ ] Confidence score displayed
- [ ] Result colored appropriately

### Gmail Scanning
- [ ] Progress bar updates smoothly
- [ ] Processes 50 emails in < 60 seconds
- [ ] Statistics update in real-time
- [ ] No crashes during scanning

### Browser Performance
- [ ] No console errors (F12 > Console tab)
- [ ] Smooth animations
- [ ] Responsive to clicks
- [ ] No memory leaks (Task Manager)

---

## 🔍 Error Checking

### Console Errors
- [ ] Press F12 (Developer Tools)
- [ ] Go to Console tab
- [ ] Should be empty (no red errors)
- [ ] Only informational messages OK

### Network Tab
- [ ] Press F12 > Network tab
- [ ] Make a request
- [ ] Status should be 200 (not 404, 500)
- [ ] Response time reasonable

### Python Errors
- [ ] Terminal should have no red text
- [ ] Only informational output
- [ ] No exceptions or tracebacks

---

## 🔒 Security Verification

### Session Security
- [ ] Credentials not printed in console
- [ ] No passwords in JavaScript
- [ ] Local storage empty (F12 > Application)

### IMAP Connection
- [ ] Uses SSL/TLS (secure connection)
- [ ] Gmail accepts connection
- [ ] No warnings about certificates

### Data Validation
- [ ] Empty inputs rejected
- [ ] Special characters handled safely
- [ ] Form validates before submission

---

## 📝 Configuration Verification

### Flask Settings (in app.py)
- [ ] Secret key set (not 'default')
- [ ] Debug mode can be toggled
- [ ] Port is available (5500)
- [ ] Host set correctly (127.0.0.1)

### Model Settings (in train_model.py)
- [ ] Max iterations: 1000
- [ ] Vectorizer max_features: 5000
- [ ] Proper label mapping: ham→0, spam→1

### HTML Configuration (in templates/index.html)
- [ ] Static file paths correct
- [ ] All JavaScript loaded
- [ ] All CSS applied

---

## 📊 Testing Checklist

### Unit Tests (Manual)
- [ ] Single message analysis works
- [ ] Gmail login succeeds
- [ ] Model prediction returns 0 or 1
- [ ] Confidence score is 0-100%

### Integration Tests
- [ ] Form submission → API → Response → Display
- [ ] Gmail scan → Progress → Results → Stats
- [ ] Message selection → Deletion → Confirmation

### User Acceptance Tests
- [ ] Website is visually appealing
- [ ] Features work as described
- [ ] Error messages are helpful
- [ ] No confusing UI elements

---

## 🚀 Pre-Launch Checklist

Before showing others or deploying:

### Code Quality
- [ ] No hardcoded passwords
- [ ] No debug print statements (if desired)
- [ ] Comments explain complex code
- [ ] File structure is organized

### Documentation
- [ ] README.md is complete
- [ ] All features documented
- [ ] Instructions are clear
- [ ] Examples provided

### Testing
- [ ] Tested with different messages
- [ ] Tested with different browsers
- [ ] Tested on mobile
- [ ] No unhandled errors

### Deployment Ready
- [ ] requirements.txt includes all packages
- [ ] .gitignore set up (if using Git)
- [ ] Environment variables documented
- [ ] Scalability considered

---

## 🐛 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Port 5500 in use | Change port in app.py or kill process |
| Model not found | Run `python train_model.py` first |
| CSV not found | Check filename is `combined_data.csv` |
| Gmail login fails | Use App Password, not regular password |
| No CSS/JS loaded | Clear browser cache (Ctrl+Shift+Delete) |
| Slow scanning | Check internet connection |
| Model prediction wrong | Retrain with more data |

---

## 📞 Getting Help

If something doesn't work:

1. **Check Documentation**
   - [ ] Read relevant section in README.md
   - [ ] Check QUICKSTART.md for quick fixes
   - [ ] Review CONFIG.md for customization

2. **Review Logs**
   - [ ] Check terminal output
   - [ ] Check browser console (F12)
   - [ ] Check error messages carefully

3. **Verify Setup**
   - [ ] Run through this checklist again
   - [ ] Check all files exist
   - [ ] Verify all dependencies installed

4. **Common Issues**
   - See "Troubleshooting" section in README.md
   - Check ARCHITECTURE.md for system understanding
   - Review code comments for implementation details

---

## ✅ Final Verification

When you reach this point, check all boxes below:

- [ ] All files in place ✓
- [ ] Dependencies installed ✓
- [ ] Model trained ✓
- [ ] Flask app runs ✓
- [ ] Website loads ✓
- [ ] Single message analysis works ✓
- [ ] Gmail integration ready (optional) ✓
- [ ] No errors in console ✓
- [ ] Performance acceptable ✓
- [ ] Ready for use ✓

---

## 🎉 You're All Set!

Congratulations! Your SpamGuard application is fully configured and ready to use.

### Next Steps:
1. **Start using it!** Analyze messages with confidence
2. **Share with others** (with instructions)
3. **Retrain regularly** with new data for better accuracy
4. **Customize** using CONFIG.md for your needs
5. **Deploy** to production when ready

---

**Questions? Check the documentation files or review the code comments!**

**Enjoy your spam-free inbox! 🛡️**
