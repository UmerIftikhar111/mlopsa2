import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import os

# Function to extract data from the article tags
def extract_articles(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all article tags
    articles = soup.find_all('article')
    # Initialize a list to store the extracted data
    data = []
    # Iterate over each article
    for article in articles:
        st = article.find(class_="story__title")
        story_excerpt = article.find(class_='story__excerpt')
        if st:
            title = st.text.strip()
            link = article.find(class_="story__link")['href']
            description = ''
            if story_excerpt:
                description = story_excerpt.text.strip()

            # Append the extracted data to the list
            data.append((title, link, description))

        # print(title)
        # print(link)
        # print(description)
        # print("\n")
    return data

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(['Title', 'Link', 'Description'])
        # Write data rows
        writer.writerows(data)
    print(f'Data saved to {filename}')

# Function to clean data by removing rows with empty descriptions
def clean_data(data):
    return [row for row in data if row[2]]  # Description is at index 2

# URL of the website
url = 'https://www.dawn.com/'
# Extract articles data
articles_data = extract_articles(url)
# Clean data by removing rows with empty descriptions
cleaned_data = clean_data(articles_data)
# Save data to CSV file
csv_filename = 'dawn_articles.csv'
save_to_csv(cleaned_data, csv_filename)
print("Data cleaned and stored")


# Function to push data file to DVC
# Function to push data file to DVC
def push_to_dvc(filename):
    # Add the file to DVC
    subprocess.run(['dvc', 'add', filename])
    # Push the changes to DVC remote storage
    subprocess.run(['dvc', 'push'])
    # Commit the changes to Git
    subprocess.run(['git', 'add', f'{filename}.dvc'])
    subprocess.run(['git', 'commit', '-m', f'Added {filename} to DVC'])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    print("Pushed data file to DVC and committed changes to Git")

# Function to pull data file from DVC
def pull_from_dvc(filename):
    subprocess.run(['dvc', 'pull', filename])

# Function to initialize DVC and set up remote storage
def initialize_dvc(remote_name, url):
    subprocess.run(['dvc', 'init', '-f'])
    subprocess.run(['dvc', 'remote', 'add', '-d', '-f', remote_name, url])

# Assuming csv_filename is defined elsewhere in your code
csv_filename = 'dawn_articles.csv'

remote_name = 'drive'
url = 'gdrive://1lqth0kLlCzkkxE4-mOlp4pqiZdEYPktJ'
initialize_dvc(remote_name, url)

# Push data file to DVC
push_to_dvc(csv_filename)
print("pushed to dvc")

pull_from_dvc(csv_filename)
print("pulled from dvc")