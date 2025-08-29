"""
Main entry point for the Telegram Crypto Price Monitor Bot
Simple synchronous version for reliable deployment
"""

import os
import time
import threading
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from crypto_monitor import CryptoPriceMonitor
from bot_commands import TelegramBotCommands

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def price_monitoring_job(monitor: CryptoPriceMonitor):
    """Price monitoring job that runs in background thread"""
    while True:
        try:
            monitor.monitor_prices()
            # Wait for the specified interval (convert minutes to seconds)
            time.sleep(monitor.check_interval * 60)
        except Exception as e:
            logger.error(f"Price monitoring error: {e}")
            time.sleep(60)  # Wait 1 minute before retrying


def main():
    """Main function that runs the Telegram bot with integrated price monitoring"""
    try:
        # Create price monitor instance
        monitor = CryptoPriceMonitor()
        
        # Get bot token
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN must be set in environment variables")
        
        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Create command handlers
        commands = TelegramBotCommands(monitor)
        
        # Add handlers
        application.add_handler(CommandHandler("start", commands.start_command))
        application.add_handler(CommandHandler("status", commands.status_command))
        application.add_handler(CommandHandler("help", commands.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.handle_message))
        
        # Start price monitoring in background thread
        monitor_thread = threading.Thread(target=price_monitoring_job, args=(monitor,), daemon=True)
        monitor_thread.start()
        logger.info("Price monitoring started in background")
        
        # Start the bot
        logger.info("Starting Telegram bot...")
        application.run_polling(drop_pending_updates=True)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()