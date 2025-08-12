import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests
from bs4 import BeautifulSoup

def send_email(subject, body):
    message = Mail(
        from_email='hitlerkiller11@gmail.com',
        to_emails='suhasmaggevenugopal@gmail.com',
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(os.environ.get('API_KEY'))
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")

url = "https://www.ozbargain.com.au/deals"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
deals = []

for node in soup.select(".node-ozbdeal"):
    title = node.select_one(".title a").text.strip()
    deal_link = "https://www.ozbargain.com.au" + node.select_one(".title a")["href"]
    votes = int(node.select_one(".voteup").text.strip())

    if votes > 25:
        deals.append({"title": title, "link": deal_link, "votes": votes})

if deals:
    email_body = "\n".join(
        f"Title: {deal['title']}\nLink: {deal['link']}\nVotes: {deal['votes']}\n"
        for deal in deals
    )
else:
    email_body = "No deals found"

send_email("Top Ozbargain Deals", email_body)
