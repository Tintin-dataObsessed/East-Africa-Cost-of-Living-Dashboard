import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_city(city_name):
    formatted_city = city_name.replace(" ", "-")
    url = f"https://www.numbeo.com/cost-of-living/in/{formatted_city}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="data_wide_table new_bar_table")
    if not table:
        print(f"No data table found for {city_name}")
        return None

    rows = table.find_all("tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 3:
            item = cols[0].text.strip()
            price_range = cols[1].text.strip()
            average = cols[2].text.strip()
            data.append([item, price_range, average])

    df = pd.DataFrame(data, columns=["Item", "Price Range", "Average Price"])
    df["City"] = city_name
    return df


if __name__ == "__main__":
    cities = ["Kampala", "Dar Es Salaam", "Nairobi"]  # The Cities

    all_data = []

    for city in cities:
        print(f"🔎 Scraping {city}...")
        df = scrape_city(city)
        if df is not None:
            all_data.append(df)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("cost_of_living_cities.csv", index=False)
        print(" Data saved to cost_of_living_cities.csv")
    else:
        print(" No data scraped.")


