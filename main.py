"""
Main entry point for the Telegram Crypto Price Monitor Bot
Combines price monitoring with interactive Telegram bot commands
"""

import os
import asyncio
import threading
import logging
from dotenv import load_dotenv

from crypto_monitor import CryptoPriceMonitor
from bot_commands import create_bot_application

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def run_price_monitor(monitor):
    """Run price monitoring in a separate thread"""
    try:
        monitor.start_monitoring()
    except Exception as e:
        logger.error(f"Price monitor error: {e}")


async def run_telegram_bot(application):
    """Run Telegram bot with async handlers"""
    try:
        # Initialize the application
        await application.initialize()
        await application.start()
        
        # Start polling for updates
        await application.updater.start_polling()
        
        logger.info("Telegram bot started and polling for messages")
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")
    finally:
        # Cleanup
        await application.stop()


async def main():
    """Main function that runs both price monitoring and Telegram bot"""
    try:
        # Create price monitor instance
        monitor = CryptoPriceMonitor()
        
        # Create Telegram bot application
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        application = create_bot_application(bot_token, monitor)
        
        # Start price monitoring in a separate thread
        monitor_thread = threading.Thread(target=run_price_monitor, args=(monitor,), daemon=True)
        monitor_thread.start()
        
        # Run Telegram bot
        await run_telegram_bot(application)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")


if __name__ == "__main__":
    asyncio.run(main())