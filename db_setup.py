import sqlite3
import pandas as pd

def save_to_db(data):
    """Сохраняет данные в SQLite базу данных."""
    conn = sqlite3.connect('prices.db')
    data.to_sql('prices', conn, if_exists='append', index=False)
    conn.close()

def get_history():
    """Получает историю цен из базы данных."""
    conn = sqlite3.connect('prices.db')
    df = pd.read_sql_query("SELECT * FROM prices", conn)
    conn.close()
    return df

def convert_to_number(s):
    if s.isdigit():
        return int(s)
    else:
        return s


def analyze_prices(df):

    if df.empty:
        print("Нет данных для анализа.")
        return

    latest_prices = df.groupby('marketplace').last().reset_index()

    print("\nРезультаты анализа:")
    print("1.Актуальные цены:")
    for _, row in latest_prices.iterrows():
        print(f"   {row['marketplace']}: {row['price']} руб.")

    if not latest_prices.empty:
        cheapest = latest_prices.loc[latest_prices['price'].idxmin()]
        print(f"\n2. Самая низкая цена: {cheapest['price']} руб. на {cheapest['marketplace']}")
    else:
        print("\n2. Невозможно определить самую низкую цену: нет данных.")

    print("\n3. Изменение цен:")
    for marketplace in df['marketplace'].unique():
        marketplace_data = df[df['marketplace'] == marketplace].sort_values('date')
        if len(marketplace_data) >= 2:
            first_price = convert_to_number(marketplace_data['price'].iloc[0])
            last_price = convert_to_number(marketplace_data['price'].iloc[-1])
            if last_price > first_price:
                trend = f"Растет по сравнению с {marketplace_data['date'].iloc[-1]}"
            elif last_price < first_price:
                trend = f"Падает по сравнению с {marketplace_data['date'].iloc[-1]}"
            else:
                trend = f"Стабильна по сравнению с {marketplace_data['date'].iloc[-1]}"
        else:
            trend = "Недостаточно данных"
        print(f"   {marketplace}: {trend}")