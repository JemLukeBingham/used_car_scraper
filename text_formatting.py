import logging

def format_mileage(mileage):
    """
    Formats mileage text data from automart. Returns int in kilometres.
    """
    if mileage is None:
        return mileage
    try:
        return int(mileage.replace(" ", "").replace("km",""))
    except (ValueError, TypeError):
        logging.warning("Could not convert mileage data to int: %s" % mileage)
        return mileage

def format_year(year):
    """
    Formats year text data from automart. Returns int.
    """
    if year is None:
        return year
    try:
        return int(year)
    except (ValueError, TypeError):
        logging.warning("Could not convert year data to int: %r" % year)
        return year

def format_price(price):
    if price is None:
        return price
    try:
        return float(price.replace(" ", "").replace(",","").replace("R",""))
    except (ValueError, TypeError):
        logging.warning("Could not convert price data to float: %s" % price)
        return price
