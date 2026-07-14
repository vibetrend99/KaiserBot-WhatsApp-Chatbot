"""
KaiserBot WhatsApp Chatbot - Production Ready
KaiserTech Solutions

This version is optimized for deployment on Render.com / Railway / similar platforms.
"""

import os
import logging
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==================== CONFIGURATION ====================
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "kaisertech_verify_2026")

COMPANY_NAME = os.getenv("COMPANY_NAME", "KaiserTech Solutions")
CONTACT_PHONE = os.getenv("CONTACT_PHONE", "0760 222 636")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "kaisertechsolution@outlook.com")

if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
    logger.warning("⚠️ WHATSAPP_TOKEN or PHONE_NUMBER_ID not set. Bot will not be able to send messages.")


# ==================== KNOWLEDGE BASE / BOT LOGIC ====================
def get_bot_response(message_text: str) -> str:
    """Returns appropriate reply based on user message"""
    text = message_text.lower().strip()

    # Greetings
    if any(word in text for word in ['habari', 'hello', 'hi', 'mambo', 'salama', 'vipi', 'hey']):
        return f"Habari! 👋 Karibu {COMPANY_NAME}. Mimi ni KaiserBot. Unahitaji msaada gani leo?"

    # Services
    if any(word in text for word in ['huduma', 'service', 'unafanya', 'services']):
        return f"""Tunatoa huduma bora za kidijitali:

✅ Website Development
✅ Mobile App Development (Android & iOS)
✅ AI Solutions & Automation
✅ UI/UX Design
✅ Business Systems (ERP, POS, LMS)
✅ IT Consulting

Unataka kujua zaidi kuhusu huduma gani?"""

    # Website
    if any(word in text for word in ['website', 'tovuti', 'web']):
        return "Ndiyo! Tunatengeneza tovuti za kisasa, zenye kasi na responsive. Bei inaanza kutoka TZS 800,000+. Unataka quote au maelezo zaidi?"

    # AI / Chatbot
    if any(word in text for word in ['ai', 'chatbot', 'akili', 'automation', 'bot']):
        return "AI ni moja ya nguvu zetu! Tunaweza kukutengenezea chatbot smart, automation ya biashara, au mifumo inayotumia AI. Hii inaweza kuwa Kaiser AI yako! 🚀 Unataka kujadili project yako?"

    # Mobile App
    if any(word in text for word in ['app', 'mobile', 'simu', 'android', 'ios']):
        return "Tunatengeneza mobile apps za Android na iOS zenye utendaji wa hali ya juu. Unataka maelezo zaidi kuhusu gharama na mchakato?"

    # Price
    if any(word in text for word in ['bei', 'price', 'gharama', 'cost']):
        return f"""Bei inategemea na ukubwa wa project.

• Website: Kuanzia TZS 800,000
• Mobile App: Kuanzia TZS 2,500,000
• AI/Chatbot: Kuanzia TZS 1,200,000

Tunatoa flexible payment plans. Piga {CONTACT_PHONE} au tuma maelezo ya project yako ili tupate quote sahihi."""

    # Contact
    if any(word in text for word in ['wasiliana', 'contact', 'namba', 'simu', 'email']):
        return f"""Tuko hapa kukusaidia!

📞 WhatsApp / Simu: {CONTACT_PHONE}
✉️ Email: {CONTACT_EMAIL}

Unaweza pia kutuandikia hapa moja kwa moja. Tutakujibu haraka!"""

    # Thank you
    if any(word in text for word in ['asante', 'thank', 'shukrani']):
        return "Asante sana! Tunafurahi kukusaidia. Kama una swali lingine au unataka kuanza project, niambie tu. 🚀"

    # Default
    return """Samahani, sijaelewa vizuri. 

Unaweza kuuliza:
• "Unatoa huduma gani?"
• "Bei ni kiasi gani?"
• "Wasiliana nasi"

Au andika swali lako moja kwa moja."""


# ==================== SEND WHATSAPP MESSAGE ====================
def send_whatsapp_message(to_number: str, message: str):
    """Send message via WhatsApp Cloud API"""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        logger.error("Missing WhatsApp credentials")
        return None

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        logger.info(f"Message sent to {to_number}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None


# ==================== WEBHOOK ====================
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Verification (GET)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("✅ Webhook verified successfully!")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed")
            return "Verification failed", 403

    # Incoming messages (POST)
    if request.method == 'POST':
        data = request.get_json()
        logger.info(f"Incoming webhook data received")

        try:
            if 'entry' in data:
                for entry in data['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if change.get('field') == 'messages':
                                value = change.get('value', {})
                                messages = value.get('messages', [])

                                for msg in messages:
                                    from_number = msg.get('from')
                                    message_type = msg.get('type')

                                    if message_type == 'text' and from_number:
                                        user_message = msg['text']['body']
                                        logger.info(f"Message from {from_number}: {user_message}")

                                        # Get reply
                                        reply = get_bot_response(user_message)

                                        # Send reply
                                        send_whatsapp_message(from_number, reply)

        except Exception as e:
            logger.error(f"Error processing message: {e}")

        return jsonify({"status": "ok"}), 200

    return "Method not allowed", 405


@app.route('/')
def home():
    return f"""
    <h1>🚀 {COMPANY_NAME} - KaiserBot</h1>
    <p>Status: <strong>Running on Render</strong></p>
    <p>WhatsApp Chatbot is active.</p>
    """


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting KaiserBot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)