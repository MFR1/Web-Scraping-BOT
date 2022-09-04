# IFPI-BOT
A Python Web Automation based Selenium bot to scrape data from the website "https://justnaija.com/music-mp3/"

# Steps
The bot follows the following steps to scrape the website:
1. Open the website
2. Scrape the number of total pages 
3. For each page:
	1. Open it
	2. Scrape URLs of all the results
	3. For each URL:
		1. Open it
		2. Scrape Post Title, Post URL, Download link, and Date Posted
		3. Push the scrapped data into the CSV file (output.csv)

# Console Output
![s1](https://user-images.githubusercontent.com/37844263/188315171-e025aa7d-f943-44be-bbef-187395ef801f.PNG)

# Output CSV
![image](https://user-images.githubusercontent.com/37844263/188315202-57ab5ed7-010c-46a2-8c70-6c3a45d47e2f.png)
