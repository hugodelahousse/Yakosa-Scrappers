import sentry_sdk

from utils import promotion_get, promotion_delete
from config import API_URL
from dateutil.parser import parse
from datetime import datetime


def remove_old_promotions():
    promotions = promotion_get(API_URL + 'promotions')
    for promotion in promotions:
        end_date = parse(promotion['endDate'])
        if end_date.date() < datetime.now().date() or float(promotion['price']) - float(promotion['promotion']) < 0:
            print(f'Delete promotion number: {promotion["id"]}')
            promotion_delete(API_URL + 'promotions/' + str(promotion['id']))


def remove_surplus_promotion():
    promotions = promotion_get(API_URL + 'promotions')
    if len(promotions) > 3000:
        promotions_sorted = sorted(promotions, key=lambda promotion: parse(promotion['endDate']))
        for i in range(len(promotions) - 3000):
            print(f'Delete promotion number: {promotions_sorted[i]["id"]}')
            promotion_delete(API_URL + 'promotions/' + str(promotions_sorted[i]['id']))


if __name__ == "__main__":
    sentry_sdk.init("https://97da0dc50f574bf89ef1ee9f668f16ed@sentry.io/1794021")
    print('START db management')
    remove_old_promotions()
    remove_surplus_promotion()
    print('FINISH db management')
