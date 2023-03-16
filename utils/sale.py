def calculate_price_with_sale(ty, price):
    match ty:
        case "Популярное":
            return price
        case "Среднее по популярности":
            return price * 0.9
        case "Непопулярное":
            return price * 0.8