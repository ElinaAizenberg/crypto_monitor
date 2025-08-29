"""
Cryptocurrency Price Monitor
Monitors crypto prices and sends Telegram notifications when thresholds are reached.
"""

import os
import time
import logging
import requests
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

from config import CRYPTO_CONFIG, COINGECKO_API_URL, DEFAULT_CHECK_INTERVAL

# Load environment variables
load_dotenv()

# Configure logging (console only)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CryptoPriceMonitor:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', DEFAULT_CHECK_INTERVAL))
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in .env file")
        
        self.bot = Bot(token=self.bot_token)
        self.notified_thresholds = {}  # Track which thresholds have been notified
        
        logger.info("Crypto Price Monitor initialized")
    
    def get_crypto_prices(self) -> Optional[Dict[str, float]]:
        """Fetch current cryptocurrency prices from CoinGecko API"""
        try:
            # Get all coin IDs we're monitoring
            coin_ids = [config['coingecko_id'] for config in CRYPTO_CONFIG.values()]
            coin_ids_str = ','.join(coin_ids)
            
            params = {
                'ids': coin_ids_str,
                'vs_currencies': 'usd'
            }
            
            response = requests.get(COINGECKO_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to our format: {coin_name: price}
            prices = {}
            for coin_name, config in CRYPTO_CONFIG.items():
                coingecko_id = config['coingecko_id']
                if coingecko_id in data and 'usd' in data[coingecko_id]:
                    prices[coin_name] = data[coingecko_id]['usd']
            
            return prices
            
        except requests.RequestException as e:
            logger.error(f"Error fetching prices: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_crypto_prices: {e}")
            return None
    
    def send_notification(self, message: str):
        """Send notification message via Telegram"""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            logger.info(f"Notification sent: {message}")
        except TelegramError as e:
            logger.error(f"Error sending Telegram message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in send_notification: {e}")
    
    def check_price_thresholds(self, prices: Dict[str, float]):
        """Check if any price thresholds have been reached and send notifications"""
        for coin_name, current_price in prices.items():
            if coin_name not in CRYPTO_CONFIG:
                continue
                
            config = CRYPTO_CONFIG[coin_name]
            symbol = config['symbol']
            realistic_price = config['realistic_price']
            optimistic_price = config['optimistic_price']
            
            # Initialize tracking for this coin if not exists
            if coin_name not in self.notified_thresholds:
                self.notified_thresholds[coin_name] = {
                    'realistic': False,
                    'optimistic': False
                }
            
            # Check realistic price threshold
            if (current_price >= realistic_price and 
                not self.notified_thresholds[coin_name]['realistic']):
                
                message = (
                    f"🎯 <b>Realistic Target Reached!</b>\n\n"
                    f"<b>{symbol}</b> ({coin_name.title()})\n"
                    f"Current Price: <b>${current_price:,.2f}</b>\n"
                    f"Target Price: <b>${realistic_price:,.2f}</b>\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                self.send_notification(message)
                self.notified_thresholds[coin_name]['realistic'] = True
            
            # Check optimistic price threshold
            if (current_price >= optimistic_price and 
                not self.notified_thresholds[coin_name]['optimistic']):
                
                message = (
                    f"🚀 <b>Optimistic Target Reached!</b>\n\n"
                    f"<b>{symbol}</b> ({coin_name.title()})\n"
                    f"Current Price: <b>${current_price:,.2f}</b>\n"
                    f"Target Price: <b>${optimistic_price:,.2f}</b>\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                self.send_notification(message)
                self.notified_thresholds[coin_name]['optimistic'] = True
    
    def reset_notifications_if_below_threshold(self, prices: Dict[str, float]):
        """Reset notification flags if price drops below threshold"""
        for coin_name, current_price in prices.items():
            if coin_name not in CRYPTO_CONFIG or coin_name not in self.notified_thresholds:
                continue
                
            config = CRYPTO_CONFIG[coin_name]
            realistic_price = config['realistic_price']
            optimistic_price = config['optimistic_price']
            
            # Reset realistic threshold if price drops below it
            if (current_price < realistic_price and 
                self.notified_thresholds[coin_name]['realistic']):
                self.notified_thresholds[coin_name]['realistic'] = False
                logger.info(f"Reset realistic threshold for {coin_name}")
            
            # Reset optimistic threshold if price drops below it
            if (current_price < optimistic_price and 
                self.notified_thresholds[coin_name]['optimistic']):
                self.notified_thresholds[coin_name]['optimistic'] = False
                logger.info(f"Reset optimistic threshold for {coin_name}")
    
    def monitor_prices(self):
        """Main monitoring function - checks prices and sends notifications"""
        logger.info("Checking cryptocurrency prices...")
        
        prices = self.get_crypto_prices()
        if not prices:
            logger.warning("Could not fetch prices, skipping this check")
            return
        
        # Log current prices
        price_info = []
        for coin_name, price in prices.items():
            symbol = CRYPTO_CONFIG[coin_name]['symbol']
            price_info.append(f"{symbol}: ${price:,.2f}")
        
        logger.info(f"Current prices - {' | '.join(price_info)}")
        
        # Check thresholds and send notifications
        self.check_price_thresholds(prices)
        
        # Reset notifications if prices drop below thresholds
        self.reset_notifications_if_below_threshold(prices)
    
    def send_status_update(self):
        """Send a status update with current prices and thresholds"""
        prices = self.get_crypto_prices()
        if not prices:
            self.send_notification("❌ Could not fetch current prices")
            return
        
        message = "📊 <b>Current Crypto Status</b>\n\n"
        
        for coin_name, current_price in prices.items():
            config = CRYPTO_CONFIG[coin_name]
            symbol = config['symbol']
            realistic_price = config['realistic_price']
            optimistic_price = config['optimistic_price']
            
            # Determine status indicators
            realistic_status = "✅" if current_price >= realistic_price else "⏳"
            optimistic_status = "✅" if current_price >= optimistic_price else "⏳"
            
            message += (
                f"<b>{symbol}</b> - ${current_price:,.2f}\n"
                f"  {realistic_status} Realistic: ${realistic_price:,.2f}\n"
                f"  {optimistic_status} Optimistic: ${optimistic_price:,.2f}\n\n"
            )
        
        message += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.send_notification(message)
    
if __name__ == "__main__":
    try:
        monitor = CryptoPriceMonitor()
        # Send initial status
        monitor.send_notification("🤖 Crypto Price Monitor Started!")
        monitor.send_status_update()
        
        # Simple monitoring loop
        logger.info(f"Starting price monitoring (checking every {monitor.check_interval} minutes)")
        while True:
            monitor.monitor_prices()
            time.sleep(monitor.check_interval * 60)
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set")
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")