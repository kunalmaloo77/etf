import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_etf_data(url, scheme_name):
    service = webdriver.ChromeService(log_output=subprocess.STDOUT)

    driver = webdriver.Chrome(service=service)

    driver.get(url)

    wait = WebDriverWait(driver, 15)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ucETFData div.table-responsive table")))

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        values = [col.get_attribute("textContent").strip() for col in cols]
        data.append(values)

    driver.quit()
    
    df = pd.DataFrame(data, columns=["Security Name", "Quantity", "Closing Market Price", "Cost of Shares"])
    df["ETF_Name"] = scheme_name
    return df

etf1 = scrape_etf_data("https://www.sbimf.com/sbimf-scheme-details/sbi-nifty-50-etf-433", "SBI Nifty 50 ETF")
etf2 = scrape_etf_data("https://www.sbimf.com/sbimf-scheme-details/sbi-bse-sensex-etf-294", "SBI BSE Sensex ETF")

combined_df = pd.concat([etf1, etf2], ignore_index=True)

combined_df.to_csv("etf_holdings.csv", index=False)

print("ETF holdings data has been saved to etf_holdings.csv")