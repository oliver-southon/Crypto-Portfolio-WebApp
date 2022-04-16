# Crypto-Portfolio-WebApp
CURRENT VERSION: V3 - uses Django and CoinGecko API to create an interactive portoflio app with live data and user-based authentication system.

**INSTRUCTIONS TO DEPLOY LOCALLY:**
1. Clone the repo into your desired directory
2. Create a virtual environment and activate it
3. Run _pip install -r requirements.txt_
4. In the same folder as "settings.py", create a file called '.env' 
5. In that file, add the line:
        SECRET_KEY = "12345"
        
        ("12345" is just a placeholder. Put whatever you like)
6. Run _py manage.py migrate_
7. Run _py manage.py runserver_
  
  And that should work!

DEMO VIDEO:
https://drive.google.com/file/d/1quYGwhPcKLkSpPMn36mRcY5vQwJzgTv1/view?usp=sharing
