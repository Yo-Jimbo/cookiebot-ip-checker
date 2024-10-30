from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    # Configura le informazioni del server SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    from_email = secrets["address"]
    password = secrets["password"]
    if ", " in secrets["receivers"]:
        to_email = secrets["receivers"].split(", ")
    else:
        to_email = secrets["receivers"]

    # Crea il messaggio email
    msg = MIMEMultipart()
    msg['From'] = from_email
    if ", " in secrets["receivers"]:
        msg['To'] = ", ".join(to_email)
    else:
        msg['To'] = to_email
    msg['Subject'] = subject

    # Aggiungi il corpo del messaggio
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connetti al server SMTP e invia l'email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")

#apre della pagina del sito di Cookiebot per lo scraping
url = "https://support.cookiebot.com/hc/en-us/articles/360003824153-Whitelisting-the-Cookiebot-scanner"

driver = webdriver.Chrome()

driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()

article_body = soup.find("div", class_='article-body')

ul = article_body.findChild("ul", recursive=False)

li_items = ul.find_all('li')

#crea la regex che comprende gli indirizzi ip trovati nella pagina
ip_regex_list = ""

for li in li_items:
    ip_regex = li.text.replace(".", "\.") + "|"
    ip_regex_list = ip_regex_list + ip_regex

ip_regex_list = ip_regex_list[:-1]

# corpo del messaggio

with open('secrets.json', 'r') as file:
    secrets = json.load(file)
sites_list_link = secrets["sites_list_link"]

subject = 'La lista di indirizzi IP di Cookiebot è cambiata'
body = """
Ciao,
<br><br>
ho eseguito uno scan della lista degli IP di Cookiebot e ho trovato dei nuovi indirizzi IP! Di seguito puoi trovare la regex che comprende tutti gli attuali indirizzi IP di CookieBot:
<br><br>
""" + ip_regex_list + """
<br><br>
Clicca <a href="
""" + sites_list_link + """
">QUI</a> per vedere la lista dei tuoi siti che utilizzano Cookiebot.
<br><br>
Al prossimo aggiornamento!"""


try:
    f = open("last_ip_regex.txt", "r+")
    if f.read() != ip_regex_list:
        f.seek(0)
        f.write(ip_regex_list)
        f.truncate()
        f.close()
        send_email(subject, body)
    else:
        pass
except FileNotFoundError:
    f = open("last_ip_regex.txt", "w")
    f.write(ip_regex_list)
    f.close()
    send_email(subject, body)