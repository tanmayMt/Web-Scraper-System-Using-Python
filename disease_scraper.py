
import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin

def fetch_disease_urls(base_url):

    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        disease_urls = {}
        
        disease_list_items = soup.find_all('li', class_='disease-list-item')
        for item in disease_list_items:
            disease_name = item.text.strip()
            disease_url = urljoin(base_url, item.a['href'])
            disease_urls[disease_name] = disease_url

        return disease_urls
    else:
        print(f"Failed to fetch disease URLs. Status code: {response.status_code}")
        return None

def fetch_disease_details(disease_urls):
    diseases_data = []

    for disease_name, disease_url in disease_urls.items():
        response = requests.get(disease_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            overview = soup.find('section', id='overview').text.strip() if soup.find('section', id='overview') else ''
            key_facts = soup.find('section', id='key-facts').text.strip() if soup.find('section', id='key-facts') else ''
            symptoms = soup.find('section', id='symptoms').text.strip() if soup.find('section', id='symptoms') else ''
            causes = soup.find('section', id='causes').text.strip() if soup.find('section', id='causes') else ''
            types = soup.find('section', id='types').text.strip() if soup.find('section', id='types') else ''
            risk_factors = soup.find('section', id='risk-factors').text.strip() if soup.find('section', id='risk-factors') else ''
            diagnosis = soup.find('section', id='diagnosis').text.strip() if soup.find('section', id='diagnosis') else ''
            prevention = soup.find('section', id='prevention').text.strip() if soup.find('section', id='prevention') else ''
            specialist_to_visit = soup.find('section', id='specialist').text.strip() if soup.find('section', id='specialist') else ''
            treatment = soup.find('section', id='treatment').text.strip() if soup.find('section', id='treatment') else ''
            home_care = soup.find('section', id='home-care').text.strip() if soup.find('section', id='home-care') else ''
            alternatives_therapies = soup.find('section', id='alternatives').text.strip() if soup.find('section', id='alternatives') else ''
            living_with = soup.find('section', id='living-with').text.strip() if soup.find('section', id='living-with') else ''

            # FAQs
            faqs = []
            faq_sections = soup.find_all('section', class_='faq-section')
            for section in faq_sections:
                question = section.find('h3').text.strip()
                answer = section.find('div', class_='faq-answer').text.strip()
                faqs.append({'Question': question, 'Answer': answer})

            references = [a['href'] for a in soup.find_all('a', href=re.compile(r'^https?://'))]

            disease_data = {
                'Disease Name': disease_name,
                'Overview': overview,
                'Key Facts': key_facts,
                'Symptoms': symptoms,
                'Causes': causes,
                'Types': types,
                'Risk factors': risk_factors,
                'Diagnosis': diagnosis,
                'Prevention': prevention,
                'Specialist to visit': specialist_to_visit,
                'Treatment': treatment,
                'Home-care': home_care,
                'Alternatives therapies': alternatives_therapies,
                'Living with': living_with,
                'FAQs': faqs,
                'References': references
            }
            diseases_data.append(disease_data)
        else:
            print(f"Failed to fetch details for {disease_name}. Status code: {response.status_code}")

    return diseases_data

def save_to_csv(data, output_file='diseases_data.csv'):

    keys = data[0].keys() if data else []
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    base_url = 'https://www.1mg.com/all-diseases'

    disease_urls = fetch_disease_urls(base_url)

    if disease_urls:
        diseases_data = fetch_disease_details(disease_urls.values())
        if diseases_data:
            save_to_csv(diseases_data)
    else:
        print("No disease URLs fetched.")
