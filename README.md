# Crypto-Portfolio-WebApp
CURRENT VERSION: V3 - uses Django and CoinGecko API to create an interactive portoflio app with live data and user-based authentication system.

**YOU CAN ACESS IT HERE**
~~https://web-production-84cd.up.railway.app/portfolio/~~
unavailable due to changes in Railway Hosting

**ALTERNATIVELY, YOU CAN RUN IT LOCALLY LIKE SO**
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



<h2>Demonstration Video:</h2>

https://user-images.githubusercontent.com/50506698/163677829-2366f562-7650-45d8-8e8c-d64d17a9307a.mp4

