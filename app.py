from flask import Flask, render_template, request, jsonify, session
import pickle
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = "fake_message_detection_secret_key"

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Gmail stats storage
gmail_stats = {
    "total_messages": 0,
    "fake_messages": 0,
    "real_messages": 0,
    "processing": False,
    "progress": 0,
    "messages_data": []
}


def decode_email_subject(subject):
    if not subject:
        return "No Subject"

    decoded_parts = []
    for part, encoding in decode_header(subject):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or "utf-8", errors="ignore"))
        else:
            decoded_parts.append(str(part))
    return "".join(decoded_parts)


def get_email_body(msg):
    body = ""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors="ignore")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode(errors="ignore")
    except Exception as e:
        print(f"Error extracting email body: {e}")

    return body.strip()


def predict_message(message_text):
    try:
        if not message_text or len(message_text.strip()) == 0:
            return None, [0.5, 0.5]

        data = vectorizer.transform([message_text])

        # Convert NumPy values into Python values
        prediction = int(model.predict(data)[0])

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(data)[0]
            probability = [float(proba[0]), float(proba[1])]
        else:
            probability = [0.5, 0.5]

        return prediction, probability

    except Exception as e:
        print(f"Prediction error: {e}")
        return None, [0.0, 0.0]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        message = request.form.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message"}), 400

        prediction, probability = predict_message(message)

        if prediction is None:
            return jsonify({"error": "Could not process message"}), 400

        result = "Fake Message" if prediction == 1 else "Real Message"
        confidence = float(probability[prediction]) * 100
        is_fake = bool(prediction == 1)

        return jsonify({
            "result": result,
            "confidence": f"{confidence:.2f}%",
            "is_fake": is_fake
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/gmail-login", methods=["POST"])
def gmail_login():
    try:
        data = request.get_json(silent=True) or {}

        email_address = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not email_address or not password:
            return jsonify({"error": "Email and App Password required"}), 400

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.logout()

        session["gmail_email"] = email_address
        session["gmail_password"] = password

        return jsonify({
            "success": True,
            "message": "Gmail authenticated successfully"
        })

    except imaplib.IMAP4.error:
        return jsonify({"error": "Invalid Gmail credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/check-gmail", methods=["POST"])
def check_gmail():
    try:
        email_address = session.get("gmail_email")
        password = session.get("gmail_password")

        if not email_address or not password:
            return jsonify({"error": "Please login to Gmail first"}), 401

        thread = threading.Thread(
            target=process_gmail_messages,
            args=(email_address, password),
            daemon=True
        )
        thread.start()

        return jsonify({
            "success": True,
            "message": "Gmail analysis started"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_gmail_messages(email_address, password):
    global gmail_stats

    try:
        gmail_stats["total_messages"] = 0
        gmail_stats["fake_messages"] = 0
        gmail_stats["real_messages"] = 0
        gmail_stats["processing"] = True
        gmail_stats["progress"] = 0
        gmail_stats["messages_data"] = []

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("INBOX")

        status, messages = mail.search(None, "ALL")
        if status != "OK":
            gmail_stats["processing"] = False
            return

        mail_ids = messages[0].split()
        gmail_stats["total_messages"] = int(len(mail_ids))

        latest_ids = mail_ids[-50:]
        total_to_process = len(latest_ids)

        if total_to_process == 0:
            gmail_stats["processing"] = False
            mail.close()
            mail.logout()
            return

        for idx, mail_id in enumerate(latest_ids):
            try:
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                if status != "OK":
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = decode_email_subject(msg.get("Subject", "No Subject"))
                from_addr = msg.get("From", "Unknown")
                body = get_email_body(msg)

                combined_text = f"{subject} {body}".strip()

                prediction, probability = predict_message(combined_text)

                if prediction is not None:
                    is_fake = bool(prediction == 1)
                    confidence = float(probability[prediction]) * 100

                    message_info = {
                        "id": mail_id.decode() if isinstance(mail_id, bytes) else str(mail_id),
                        "from": str(from_addr),
                        "subject": str(subject),
                        "preview": body[:150] + ("..." if len(body) > 150 else ""),
                        "is_fake": is_fake,
                        "confidence": f"{confidence:.2f}%",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    gmail_stats["messages_data"].append(message_info)

                    if is_fake:
                        gmail_stats["fake_messages"] += 1
                    else:
                        gmail_stats["real_messages"] += 1

                gmail_stats["progress"] = int(((idx + 1) / total_to_process) * 100)

            except Exception as e:
                print(f"Error processing one email: {e}")
                continue

        mail.close()
        mail.logout()
        gmail_stats["processing"] = False

    except Exception as e:
        print(f"Gmail processing error: {e}")
        gmail_stats["processing"] = False


@app.route("/gmail-stats", methods=["GET"])
def gmail_stats_route():
    return jsonify({
        "total_messages": int(gmail_stats["total_messages"]),
        "fake_messages": int(gmail_stats["fake_messages"]),
        "real_messages": int(gmail_stats["real_messages"]),
        "processing": bool(gmail_stats["processing"]),
        "progress": int(gmail_stats["progress"]),
        "messages_data": gmail_stats["messages_data"]
    })


@app.route("/delete-fake-messages", methods=["POST"])
def delete_fake_messages():
    try:
        email_address = session.get("gmail_email")
        password = session.get("gmail_password")

        if not email_address or not password:
            return jsonify({"error": "Please login to Gmail first"}), 401

        data = request.get_json(silent=True) or {}
        message_ids = data.get("message_ids", [])

        if not message_ids:
            return jsonify({"error": "No fake messages selected"}), 400

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("INBOX")

        deleted_count = 0

        for msg_id in message_ids:
            try:
                mail.store(str(msg_id), "+FLAGS", "\\Deleted")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting message {msg_id}: {e}")

        mail.expunge()
        mail.close()
        mail.logout()

        return jsonify({
            "success": True,
            "deleted_count": int(deleted_count),
            "message": f"Successfully deleted {deleted_count} fake messages"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)