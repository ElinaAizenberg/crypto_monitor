"""
Setup script for easy bot configuration
"""

import os
import sys


def create_env_file():
    """Interactive setup for .env file"""
    print("🤖 Telegram Crypto Bot Setup")
    print("=" * 30)
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 You'll need:")
    print("1. Telegram Bot Token (from @BotFather)")
    print("2. Your Telegram Chat ID")
    print("\n🔗 Getting your Chat ID:")
    print("   - Start a chat with your bot")
    print("   - Send any message")
    print("   - Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("   - Find 'chat':{'id': YOUR_CHAT_ID}")
    
    print("\n" + "=" * 50)
    
    # Get bot token
    bot_token = input("\n🔑 Enter your Telegram Bot Token: ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        return
    
    # Get chat ID
    chat_id = input("💬 Enter your Telegram Chat ID: ").strip()
    if not chat_id:
        print("❌ Chat ID is required!")
        return
    
    # Get check interval
    interval = input("⏱️  Check interval in minutes (default: 5): ").strip()
    if not interval:
        interval = "5"
    
    # Create .env file
    env_content = f"""# Telegram Bot Token from @BotFather
TELEGRAM_BOT_TOKEN={bot_token}

# Your Telegram User ID (to receive notifications)
TELEGRAM_CHAT_ID={chat_id}

# Price check interval in minutes (default: 5)
CHECK_INTERVAL_MINUTES={interval}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    print("\n📝 Next steps:")
    print("1. Review price targets in config.py")
    print("2. Run: python main.py")
    print("3. Test with /status command in Telegram")


def show_current_config():
    """Show current cryptocurrency configuration"""
    try:
        from config import CRYPTO_CONFIG
        
        print("\n📊 Current Cryptocurrency Configuration:")
        print("=" * 50)
        
        for coin_name, config in CRYPTO_CONFIG.items():
            symbol = config['symbol']
            realistic = config['realistic_price']
            optimistic = config['optimistic_price']
            
            print(f"{symbol:6} | Realistic: ${realistic:>8,.0f} | Optimistic: ${optimistic:>8,.0f}")
        
        print("\n💡 Edit config.py to change these targets")
        
    except ImportError:
        print("❌ Could not load configuration")


def main():
    """Main setup function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            show_current_config()
            return
        elif sys.argv[1] == "env":
            create_env_file()
            return
    
    print("🤖 Telegram Crypto Bot Setup")
    print("=" * 30)
    print("\nOptions:")
    print("1. Configure .env file")
    print("2. Show current price targets")
    print("3. Exit")
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            create_env_file()
            break
        elif choice == "2":
            show_current_config()
            break
        elif choice == "3":
            print("Setup cancelled.")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()