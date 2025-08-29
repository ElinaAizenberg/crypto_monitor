"""
Telegram bot command handlers for interactive features
"""

import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from crypto_monitor import CryptoPriceMonitor


class TelegramBotCommands:
    def __init__(self, monitor: CryptoPriceMonitor):
        self.monitor = monitor
        
        # Create persistent keyboard with Status button
        self.reply_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📊 Status")]],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "🤖 <b>Crypto Price Monitor Bot</b>\n\n"
            "I'll notify you when your cryptocurrency targets are reached!\n\n"
            "<b>Available commands:</b>\n"
            "/help - Show this help message\n\n"
            "Use the <b>📊 Status</b> button below to check current prices anytime!\n"
            "The bot automatically checks prices every few minutes."
        )
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='HTML', 
            reply_markup=self.reply_keyboard
        )
    
    async def get_status_message(self):
        """Generate status message with current prices"""
        prices = self.monitor.get_crypto_prices()
        if not prices:
            return "❌ Could not fetch current prices. Please try again later."
        
        message = "📊 <b>Current Crypto Status</b>\n\n"
        
        for coin_name, current_price in prices.items():
            from config import CRYPTO_CONFIG
            config = CRYPTO_CONFIG[coin_name]
            symbol = config['symbol']
            realistic_price = config['realistic_price']
            optimistic_price = config['optimistic_price']
            
            # Calculate percentage to targets
            realistic_pct = ((current_price - realistic_price) / realistic_price * 100)
            optimistic_pct = ((current_price - optimistic_price) / optimistic_price * 100)
            
            # Status indicators
            realistic_status = "✅" if current_price >= realistic_price else f"📈 {realistic_pct:+.1f}%"
            optimistic_status = "✅" if current_price >= optimistic_price else f"📈 {optimistic_pct:+.1f}%"
            
            message += (
                f"<b>{symbol}</b> - ${current_price:,.2f}\n"
                f"  Realistic (${realistic_price:,.2f}): {realistic_status}\n"
                f"  Optimistic (${optimistic_price:,.2f}): {optimistic_status}\n\n"
            )
        
        from datetime import datetime
        message += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command and Status button"""
        message = await self.get_status_message()
        await update.message.reply_text(message, parse_mode='HTML', reply_markup=self.reply_keyboard)
    
    async def get_help_message(self):
        """Generate help message"""
        help_message = (
            "🤖 <b>Crypto Price Monitor Bot Help</b>\n\n"
            "<b>What I do:</b>\n"
            "• Monitor cryptocurrency prices continuously\n"
            "• Send notifications when your target prices are reached\n"
            "• Track both realistic and optimistic price targets\n\n"
            "<b>Commands:</b>\n"
            "/start - Welcome message and bot info\n"
            "/status - Show current prices and progress to targets\n"
            "/help - Show this help message\n\n"
            "<b>Monitored Coins:</b>\n"
        )
        
        from config import CRYPTO_CONFIG
        for coin_name, config in CRYPTO_CONFIG.items():
            symbol = config['symbol']
            realistic = config['realistic_price']
            optimistic = config['optimistic_price']
            help_message += f"• {symbol}: ${realistic:,.0f} / ${optimistic:,.0f}\n"
        
        return help_message

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = await self.get_help_message()
        await update.message.reply_text(help_message, parse_mode='HTML', reply_markup=self.reply_keyboard)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (including Status button presses)"""
        text = update.message.text
        
        if text == "📊 Status":
            # Handle Status button press
            message = await self.get_status_message()
            await update.message.reply_text(message, parse_mode='HTML', reply_markup=self.reply_keyboard)
        else:
            # Handle unknown messages
            await update.message.reply_text(
                "I don't understand that command. Use the 📊 Status button or /help for available options.",
                reply_markup=self.reply_keyboard
            )


def create_bot_application(bot_token: str, monitor: CryptoPriceMonitor) -> Application:
    """Create and configure the Telegram bot application"""
    application = Application.builder().token(bot_token).build()
    
    commands = TelegramBotCommands(monitor)
    
    # Add command handlers
    application.add_handler(CommandHandler("start", commands.start_command))
    application.add_handler(CommandHandler("status", commands.status_command))
    application.add_handler(CommandHandler("help", commands.help_command))
    
    # Add message handler for Status button and other text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.handle_message))
    
    return application