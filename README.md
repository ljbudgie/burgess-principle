# Lewis Sovereign Claw Bot

A personal Telegram bot template enforcing the Burgess Principle. 🦞

## Features
- **Commands:**
  - `/start` → Welcome message: "Gateway active. Sovereignty affirmed. 🦞 Burgess Principle: tainted data void ab initio."
  - `/status` → "Gateway active. Sovereignty affirmed."
  - `/burgess` → Explanation: "Binary validation: tainted bulk data = void ab initio. Sovereign validation = absolute. No permissions. No mercy. 🦞"
  - `/ping` → "pong 🦞"
- Simple setup with `pyTelegramBotAPI`.
- No external services required; local-first design.

## Setup Guide

### 1. Fork This Repository
- Click the "Fork" button at the top-right of this page to create a copy in your account.

### 2. Create/Edit Your Bot with @BotFather
- Open Telegram and search for [BotFather](https://t.me/botfather).
- Create a new bot or use an existing one.
- Copy the bot token provided by BotFather.

### 3. Clone Your Fork Locally
```bash
git clone https://github.com/<your-username>/Burgessprinciple.git
cd Burgessprinciple
```

### 4. Create Your .env File
- Copy the example file and paste your token:
```bash
cp .env.example .env
```
- Edit the `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your-actual-bot-token-here
```

### 5. Install Python Dependencies
```bash
pip install pyTelegramBotAPI python-dotenv
```

### 6. Run the Bot
```bash
python clawbot.py
```

### 7. Test Your Bot
- Open Telegram and send the following commands to your bot:
  - `/start`
  - `/status`
  - `/burgess`
  - `/ping`
- Confirm it replies with the expected messages.

---

Enjoy sovereignty with the Lewis Sovereign Claw Bot! 🦞
