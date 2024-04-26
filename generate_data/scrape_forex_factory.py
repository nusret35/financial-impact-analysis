import time
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from model.schemas import Entry
import numpy as np
import pandas as pd

def read_urls_from_file(file_path):
    urls = []
    with open(file_path, "r") as file:
        for line in file:
            urls.append(line.strip())
    return urls

urls = read_urls_from_file("./generated_urls.txt")

chrome_options = Options()

driver = Driver(uc=True,headless=True)


def get_currencies():
    currencies = []
    tds = driver.find_elements(By.XPATH,"//td[@class='calendar__cell calendar__currency']")
    for td in tds:
        span = td.find_element(By.CSS_SELECTOR,"span")
        currencies.append(span.text)
    return np.array(currencies)

def get_impacts():
    impacts = []
    tds = driver.find_elements(By.XPATH,"//td[@class='calendar__cell calendar__impact']")
    for td in tds:
        span = td.find_element(By.CSS_SELECTOR,"span")
        impacts.append(span.get_attribute("title"))
    return np.array(impacts)

def get_events():
    events = []
    spans = driver.find_elements(By.XPATH,"//span[@class='calendar__event-title']")
    for span in spans:
        events.append(span.text)
    return np.array(events)

def get_previouses():
    previouses = []
    tds = driver.find_elements(By.XPATH,"//td[@class='calendar__cell calendar__previous']")
    for td in tds:
        span = td.find_element(By.CSS_SELECTOR,"span")
        previouses.append(span.text)
    return np.array(previouses)

def get_forecasts():
    forecasts = []
    tds = driver.find_elements(By.XPATH,"//td[@class='calendar__cell calendar__forecast']")
    for td in tds:
        span = td.find_element(By.CSS_SELECTOR,"span")
        forecasts.append(span.text)
    return np.array(forecasts)

def get_actuals():
    actuals = []
    tds = driver.find_elements(By.XPATH,"//td[@class='calendar__cell calendar__actual']")
    for td in tds:
        span = td.find_element(By.CSS_SELECTOR,"span")
        actuals.append(span.text)
    return np.array(actuals)

def get_entries():
    currencies = get_currencies()
    impacts = get_impacts()
    events = get_events()
    previouses = get_previouses()
    forecasts = get_forecasts()
    actuals = get_actuals()
    data = {"currency":currencies,
            "event":events,
            "impact":impacts,
            "previous_value":previouses,
            "forecast_value":forecasts,
            "actual_value":actuals}
    return pd.DataFrame(data=data)


def main():
    df = pd.DataFrame(columns=["currency",
                               "event",
                               "impact",
                               "previous_value",
                               "forecast_value",
                               "actual_value"])
    try:
        for url in urls:
            driver.get(url)
            time.sleep(1)
            new_entries = get_entries()
            df = pd.concat([df,new_entries],ignore_index=True)
        print("SUCCESS: Data extraction completed.")
    except Exception as error:
        print(f"ERROR: {error}")
    finally:
        df.to_csv("forex_factory_dataset.csv")
        print("Dataset is saved as forex_factory_dataset.csv")
        print(df.info)
        driver.quit()

if __name__ == "__main__":
    main()

