from datetime import datetime, timedelta
from decimal import Decimal
import re


def rhb_get_amount_and_type(amount_string):
    if amount_string.startswith("-"):
        amount = float(amount_string.split()[-1])
        amount_type = "debit"
    else:
        amount = float(amount_string.split()[-1])
        amount_type = "credit"
    return amount, amount_type


def rhb_convert_date(date_str):
    return datetime.strptime(date_str, '%d %B %Y').date()


def may_format_date(date):
    return datetime.strptime(date, "%d %b %Y").date()

def may_format_amount(amount):
    return Decimal(amount.replace('RM', ''))

def hongleong_convert_date(date_st):
    return datetime.strptime(date_st, '%d-%b-%Y').date()

def honglelong_extract_num(text):
    pattern = r"\d+\.\d+"
    match = re.search(pattern, text)
    if match:
        return float(match.group(0))
    else:
        return 0.0