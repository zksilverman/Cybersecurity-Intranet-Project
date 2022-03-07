"""
Flask app configuration
"""
import requests

DEBUG = True
SC = ";"
TEMPLATES_AUTO_RELOAD = True
DB_FILE = './instance/var/db/test.db'
SECRET_KEY = 'This is not very secret, is it?'
CREDENTIALS_FILE = 'instance/static/passwd'  # Ack! This is web-accessible!
LESSON_CATALOG = {
    "Cross-site Scripting (XSS)": [".cat_coin_stock", "CatCoin stock"],
    "SQL Injection Attack": [".transactions", "Transaction search"],
    "Secure Login": [".login", "Customer login"]
}
display = {}
response = requests.get("https://jreddy1.w3.uvm.edu/cs166/activate/lessons.json")
active = response.json()
for key in active:
    if active[key]:
        display[key] = LESSON_CATALOG[key]



