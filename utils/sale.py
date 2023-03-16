def calculate_price_with_sale(ty, price):
    if ty == "Популярное":
        return price
    elif ty == "Среднее по популярности":
        return price
    else:
        return price * 0.9
