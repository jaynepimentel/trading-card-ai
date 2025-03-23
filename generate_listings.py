
import random

def generate_listing(card_data):
    title = f"{card_data['year']} {card_data['set']} {card_data['player']} {card_data['parallel']} {card_data['serial']}"
    description = (
        f"This listing is for a {card_data['year']} {card_data['set']} {card_data['player']} "
        f"{card_data['parallel']} trading card, serial numbered {card_data['serial']}. "
        f"Condition is {card_data['condition']}. Ships securely in a top loader and bubble mailer."
    )
    return {
        "title": title,
        "description": description,
        "estimated_price": estimate_price(card_data)
    }

def estimate_price(card_data):
    base_price = 10
    multipliers = {
        "Gold Prizm": 3.5,
        "Silver Prizm": 2.0,
        "Black": 6.0,
        "1/1": 10.0
    }
    factor = multipliers.get(card_data["parallel"], 1.0)
    if "/10" in card_data["serial"]:
        factor += 2.0
    elif "/1" in card_data["serial"]:
        factor += 5.0
    return round(base_price * factor * random.uniform(0.8, 1.2), 2)
