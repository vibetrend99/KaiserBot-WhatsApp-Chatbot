# 🚀 KaiserBot WhatsApp Chatbot - Deployment Guide (Render.com)

Mwongozo huu utakuelekeza jinsi ya ku-deploy KaiserBot kwenye **Render.com** ili iweze kufanya kazi 24/7.

---

## Files Zilizojumuishwa

- `app.py` → Main application code (production ready)
- `requirements.txt` → Python libraries
- `Procfile` → Inaeleza Render jinsi ya kuendesha app
- `.env.example` → Template ya environment variables

---

## Hatua za Deployment (Render.com)

### 1. Andaa GitHub Repository

1. Unda akaunti mpya kwenye [GitHub](https://github.com) kama huna
2. Unda repository mpya (public au private)
3. Upload files zifuatazo kwenye repository:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `.env.example` (optional)

### 2. Unda Akaunti kwenye Render.com

- Nenda: [https://render.com](https://render.com)
- Jisajili kwa kutumia GitHub (rahisi zaidi)

### 3. Unda Web Service Mpya

1. Baada ya login, bonyeza **"New +"** → **Web Service**
2. Chagua **"Build and deploy from a Git repository"**
3. Unganisha GitHub account yako
4. Chagua repository uliyotengeneza hapo juu
5. Weka mipangilio ifuatayo:

   - **Name**: `kaiserbot` (au jina lolote unalopenda)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
   - **Plan**: Free (inatosha kuanza)

6. Bonyeza **"Create Web Service"**

### 4. Weka Environment Variables

Baada ya deployment kuanza:

1. Nenda kwenye **"Environment"** tab
2. Bonyeza **"Add Environment Variable"** na uongeze zifuatazo:

   | Key                    | Value                                      |
   |------------------------|--------------------------------------------|
   | `WHATSAPP_TOKEN`       | (Token yako ya Meta)                       |
   | `PHONE_NUMBER_ID`      | (Phone Number ID yako)                     |
   | `VERIFY_TOKEN`         | `kaisertech_verify_2026`                   |
   | `COMPANY_NAME`         | `KaiserTech Solutions`                     |
   | `CONTACT_PHONE`        | `0760 222 636`                             |
   | `CONTACT_EMAIL`        | `kaisertechsolution@outlook.com`           |

3. Bonyeza **Save Changes**

### 5. Subiri Deployment Iishe

- Render itakujengea na kuendesha app yako
- Utapata URL kama: `https://kaiserbot-xxxx.onrender.com`

### 6. Weka Webhook kwenye Meta

1. Copy URL yako ya Render (mfano: `https://kaiserbot.onrender.com`)
2. Nenda kwenye Meta Developers Console → WhatsApp → Configuration
3. Weka:
   - **Callback URL**: `https://kaiserbot-xxxx.onrender.com/webhook`
   - **Verify Token**: `kaisertech_verify_2026`
4. Bonyeza **Verify and Save**

---

## Jinsi ya Kujaribu

1. Nenda kwenye WhatsApp
2. Tuma ujumbe kwenye namba yako ya WhatsApp Business / Test number
3. Bot inapaswa kujibu kiotomatiki

Mfano wa ujumbe wa kujaribu:
- `Habari`
- `Unatoa huduma gani?`
- `Bei ni kiasi gani?`

---

## Vidokezo Muhimu

- **Free tier** ya Render inaweza kulala baada ya muda wa kutotumika. Unaweza kuupgrade baadaye.
- Kila unapofanya mabadiliko kwenye GitHub, Render ita-deploy upya kiotomatiki.
- Unaweza kuona logs kwenye Render dashboard ili uone kama kuna makosa.

---

## Unahitaji Msaada?

Kama unapata shida wakati wa deployment, niambie:
- Error unayoiona
- Hatua uliyokwama

Tutakutatua pamoja.

---
**Iliyotengenezwa na KaiserTech Solutions** | 2026