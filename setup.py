"""
Quick setup script to help configure the job scraper
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    required = ['requests', 'beautifulsoup4', 'schedule', 'lxml']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed!")
        return True

def check_config():
    """Check if config.py is properly configured"""
    try:
        from config import EMAIL_CONFIG
        
        if EMAIL_CONFIG['sender_email'] == 'your_email@gmail.com':
            print("⚠️  Email configuration not set up yet!")
            print("   Please edit config.py and update EMAIL_CONFIG")
            return False
        else:
            print("✅ Email configuration found!")
            return True
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False

def main():
    print("=" * 60)
    print("Job Scraper Setup Check")
    print("=" * 60)
    print()
    
    deps_ok = check_dependencies()
    print()
    config_ok = check_config()
    print()
    
    if deps_ok and config_ok:
        print("=" * 60)
        print("✅ Setup complete! You're ready to run the scraper.")
        print()
        print("Next steps:")
        print("1. Test email: python main.py --test-email")
        print("2. Run scraper: python main.py")
        print("=" * 60)
    else:
        print("=" * 60)
        print("⚠️  Please fix the issues above before running the scraper.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()

