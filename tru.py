import requests
from bs4 import BeautifulSoup

def get_transcript(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch the webpage")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    transcript_div = soup.find('div', {'id': 'transcript'})
    
    if not transcript_div:
        raise Exception("Transcript not found on the page")
    
    transcript_text = []
    for span in transcript_div.find_all('span', class_='transcript-segment'):
        transcript_text.append(span.get_text(strip=True))
    
    return ' '.join(transcript_text)

