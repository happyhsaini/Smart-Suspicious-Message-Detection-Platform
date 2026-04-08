# 🚀 Quick Start Guide

Get your Fake Message Detection website up and running in 5 minutes!

## Step 1: Install Python Dependencies

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- scikit-learn (machine learning)
- pandas (data handling)
- numpy (numerical computing)

## Step 2: Prepare Your Dataset

You need a CSV file named `combined_data.csv` with two columns:
- **label**: `ham` (real message) or `spam` (fake message)
- **text**: The actual message content

Example format:
```
label,text
ham,Hey what are you doing tonight
spam,Congratulations! You won 50000 rupees Click here now
ham,Can we talk later today
spam,Your bank account is blocked Verify now
```

## Step 3: Train the Model

Run the training script:

```bash
python train_model.py
```

You should see output like:
```
🤖 Fake Message Detection Model Training
...
✅ Training Complete!
```

This creates two files:
- `model.pkl` - The trained AI model
- `vectorizer.pkl` - The text processor

## Step 4: Start the Application

Run:

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5500
```

## Step 5: Open in Browser

Go to: **http://127.0.0.1:5500**

That's it! Your website is live! 🎉

---

## 📋 File Structure

After setup, your folder should look like:

```
your-project/
├── app.py                    # Main Flask application
├── train_model.py            # Model training script
├── requirements.txt          # Python packages
├── combined_data.csv         # Your training data
├── model.pkl                 # Trained model (created)
├── vectorizer.pkl            # Text processor (created)
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
├── static/
│   ├── style.css            # Website styling
│   └── script.js            # Interactive features
└── templates/
    └── index.html           # Website layout
```

---

## 🎯 How to Use the Website

### Check a Single Message
1. Scroll to "Check a Message"
2. Paste your message
3. Click "Analyze Message"
4. See if it's Fake or Real ✓

### Scan Your Gmail Inbox
1. Scroll to "Gmail Tools"
2. Get your Gmail App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Enter your Gmail address and password
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
3. Paste it into the website
4. Click "Connect Gmail"
5. Click "Scan Inbox"
6. Review detected fake messages
7. Delete them all at once!

---

## 🔧 Troubleshooting

### Error: "combined_data.csv not found"
- Make sure your CSV file is in the same folder as app.py
- Check the filename is exactly `combined_data.csv`

### Error: "module not found"
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

### Port already in use
- Change the port in app.py:
  ```python
  app.run(port=5501)  # Use 5501 instead of 5500
  ```

### Gmail login fails
- Use an **App Password**, not your regular password
- Enable 2-factor authentication first
- Create a new App Password

---

## 💡 Tips

✅ **Test with sample messages first** before connecting Gmail
✅ **Use App Password for security** - it can be revoked anytime
✅ **Review results** before deleting messages
✅ **Improve accuracy** by training with more data

---

## 📚 Need More Help?

- Read `README.md` for full documentation
- Check comments in Python files for explanations
- Review the code structure for learning

---

## ⚡ Performance Tips

1. **Larger dataset** = Better accuracy
2. **Clean data** = Better training
3. **Regular retraining** = Up-to-date models

---

**Happy detecting! 🛡️**

Next step: Train your model and open http://127.0.0.1:5500 in your browser!
