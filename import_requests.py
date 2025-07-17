import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_category(city_name, category_name, url_suffix, table_class):
    formatted_city = city_name.replace(" ", "-")
    url = f"https://www.numbeo.com/{url_suffix}/in/{formatted_city}"
    headers = {"User-Agent": "Mozilla/5.0"}  

    print(f" Fetching: {url}")  

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f" Error fetching {category_name} in {city_name}: HTTP {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_=table_class)
    if not table:
        print(f" No table found for {category_name} in {city_name}")
        return None

    rows = table.find_all("tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 3:
            item = cols[0].text.strip()
            price_range = cols[1].text.strip()
            average = cols[2].text.strip()
            data.append([item, price_range, average, city_name, category_name])

    df = pd.DataFrame(data, columns=["Item", "Price Range", "Average Price", "City", "Category"])
    return df

# --- Main script ---
if __name__ == "__main__":
    cities = ["Kampala", "Dar Es Salaam", "Nairobi", "Kigali", "Addis Ababa", "Mombasa"]
    all_data = []

    for city in cities:
        print(f"\n📍 Scraping {city}...")

        # 1. Main cost of living
        col_df = scrape_category(city, "Cost of Living", "cost-of-living", "data_wide_table new_bar_table")
        if col_df is not None:
            all_data.append(col_df)

        # 2. Groceries
        grocery_df = scrape_category(city, "Groceries", "food-prices", "data_wide_table")
        if grocery_df is not None:
            all_data.append(grocery_df)

        # 3. Rent
        rent_df = scrape_category(city, "Rent", "property-investment", "data_wide_table")
        if rent_df is not None:
            all_data.append(rent_df)

    # Combine and save
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("east_africa_cost_of_living_combined.csv", index=False)
        print("\n All data saved to east_africa_cost_of_living_combined.csv")
    else:
        print("\n No data was scraped.")
