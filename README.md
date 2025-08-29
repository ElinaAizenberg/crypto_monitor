# Telegram Crypto Price Monitor Bot

A Telegram bot that monitors cryptocurrency prices and sends notifications when your target prices are reached.

## Features

- 📊 Monitors 5 cryptocurrencies: BTC, ETH, XRP, SOL, LTC
- 🎯 Dual threshold system: Realistic and Optimistic price targets
- 📱 Real-time Telegram notifications when targets are reached
- 🔄 Automatic price checking every 5 minutes (configurable)
- 📈 Interactive commands to check current status
- 📝 Comprehensive logging

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy your bot token

### 3. Get Your Chat ID

1. Start a chat with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response

### 4. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CHECK_INTERVAL_MINUTES=5
```

### 5. Configure Price Targets

Edit `config.py` to set your price targets:

```python
CRYPTO_CONFIG = {
    "bitcoin": {
        "symbol": "BTC",
        "realistic_price": 50000,  # Your realistic target
        "optimistic_price": 75000, # Your optimistic target
        "coingecko_id": "bitcoin"
    },
    # ... update other coins as needed
}
```

### 6. Run the Bot

```bash
python main.py
```

## Bot Interface

### Commands
- `/start` - Welcome message and activate persistent Status button
- `/status` - Show current prices and progress to targets  
- `/help` - Show available commands and monitored coins

### Persistent Keyboard
- **📊 Status** - Always visible button above your keyboard for instant price checking

The bot features a persistent "Status" button that stays above your keyboard at all times, making it incredibly easy to check cryptocurrency prices with just one tap!

## How It Works

1. **Price Monitoring**: The bot fetches prices from CoinGecko API every 5 minutes
2. **Threshold Detection**: When a price reaches your realistic or optimistic target, you get notified
3. **Smart Notifications**: Each threshold is only triggered once until the price drops below it again
4. **Interactive Commands**: Use Telegram commands to check status anytime

## Example Notifications

When BTC reaches your realistic target:
```
🎯 Realistic Target Reached!

BTC (Bitcoin)
Current Price: $52,000.00
Target Price: $50,000.00
Time: 2024-01-15 14:30:25
```

When ETH reaches your optimistic target:
```
🚀 Optimistic Target Reached!

ETH (Ethereum)
Current Price: $5,200.00
Target Price: $5,000.00
Time: 2024-01-15 16:45:10
```

## Monitored Cryptocurrencies

| Symbol | Name      | Current Realistic | Current Optimistic |
|--------|-----------|-------------------|---------------------|
| BTC    | Bitcoin   | $120,000         | $122,000           |
| ETH    | Ethereum  | $4,700           | $4,800             |
| XRP    | Ripple    | $3.00            | $3.03              |
| SOL    | Solana    | $215             | $216               |
| LTC    | Litecoin  | $115             | $117               |

## Customization

### Adding New Coins

1. Add to `CRYPTO_CONFIG` in `config.py`
2. Use the CoinGecko ID (find at [CoinGecko](https://www.coingecko.com/))

### Changing Check Interval

Update `CHECK_INTERVAL_MINUTES` in your `.env` file (minimum: 1 minute)

### Modifying Price Targets

Update the `realistic_price` and `optimistic_price` values in `config.py`

## Logs

- Console output shows real-time monitoring
- Includes price checks, notifications sent, and any errors

