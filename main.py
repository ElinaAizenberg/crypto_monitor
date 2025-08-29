"""
Main entry point for the Telegram Crypto Price Monitor Bot
Simplified version for cloud deployment
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram.ext import Application

from crypto_monitor import CryptoPriceMonitor
from bot_commands import create_bot_application

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


async def price_monitoring_job(monitor: CryptoPriceMonitor):
    """Async price monitoring job"""
    while True:
        try:
            monitor.monitor_prices()
            # Wait for the specified interval (convert minutes to seconds)
            await asyncio.sleep(monitor.check_interval * 60)
        except Exception as e:
            logger.error(f"Price monitoring error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying


async def main():
    """Main function that runs the Telegram bot with integrated price monitoring"""
    monitor = None
    application = None
    monitor_task = None
    
    try:
        # Create price monitor instance
        monitor = CryptoPriceMonitor()
        
        # Create Telegram bot application
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN must be set in environment variables")
            
        application = create_bot_application(bot_token, monitor)
        
        # Initialize the application
        await application.initialize()
        
        # Send startup notification
        try:
            await application.bot.send_message(
                chat_id=monitor.chat_id, 
                text="🤖 Crypto Price Monitor Started!"
            )
        except Exception as e:
            logger.warning(f"Could not send startup notification: {e}")
        
        # Start price monitoring task
        monitor_task = asyncio.create_task(price_monitoring_job(monitor))
        
        # Start the bot
        logger.info("Starting Telegram bot...")
        async with application:
            await application.start()
            await application.updater.start_polling(drop_pending_updates=True)
            
            # Keep running until interrupted
            try:
                await asyncio.Event().wait()  # Wait indefinitely
            except asyncio.CancelledError:
                pass
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    finally:
        # Cleanup
        if monitor_task:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
        
        if application:
            try:
                await application.shutdown()
            except Exception as e:
                logger.warning(f"Error during shutdown: {e}")


if __name__ == "__main__":
    asyncio.run(main())