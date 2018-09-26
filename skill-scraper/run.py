import schedule 
import time 
from scrape_boards import scrape

scrape()

schedule.every().hour.do(scrape)

while True:
    schedule.run_pending()
    time.sleep(1)