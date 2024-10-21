from script import get_price
from config import products
from datetime import datetime
import pandas as pd
from db_setup import save_to_db, get_history, analyze_prices

def main():
    prices_recieved = []

    for url, price_class in products.items():
        price = get_price(url, price_class)
        if price:
            prices_recieved.append(
            {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'marketplace': url.split('.')[1],
                'price': price
            })
        else:
            print(f"Не удалось получить цену с {url.split('.')[1]}")

    if prices_recieved:
        print("Получены следующие цены:")
        for price_data in prices_recieved:
            print(f"{price_data['marketplace']}: {price_data['price']} руб.")
    
        df = pd.DataFrame(prices_recieved)
        save_to_db(df)

        history_df = get_history()
        analyze_prices(history_df)

    else:
        print("Не удалось получить ни одной цены.")


if __name__ == "__main__":
    main() 