import aiohttp
import asyncio
import argparse
import json
from datetime import datetime, timedelta
from aiofile import AIOFile

async def fetch_exchange_rate(date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_currency_rates(days):
    today = datetime.today()
    currency_rates = []

    # Set the desired date (December 29, 2023)
    target_date = datetime(2023, 12, 29)

    for i in range(days):
        current_date = target_date - timedelta(days=i)
        formatted_date = current_date.strftime('%d.%m.%Y')

        data = await fetch_exchange_rate(formatted_date)
        if 'exchangeRate' in data:
            exchange_rate = {
                formatted_date: {
                    'EUR': {
                        'sale': data['exchangeRate'][0]['saleRateNB'],
                        'purchase': data['exchangeRate'][0]['purchaseRateNB']
                    },
                    'USD': {
                        'sale': data['exchangeRate'][1]['saleRateNB'],
                        'purchase': data['exchangeRate'][1]['purchaseRateNB']
                    }
                }
            }
            currency_rates.append(exchange_rate)

    return currency_rates

async def save_to_log(command, filename='exchange_log.txt'):
    async with AIOFile(filename, 'a') as afp:
        await afp.write(f"{datetime.now()} - Executed command: {command}\n")

async def main():
    parser = argparse.ArgumentParser(description='Get currency exchange rates.')
    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates for')
    args = parser.parse_args()

    currency_rates = await fetch_currency_rates(args.days)
    print(json.dumps(currency_rates, indent=2))

    await save_to_log(' '.join([arg for arg in vars(args)]))

if __name__ == '__main__':
    asyncio.run(main())
