from rx import Observable
from time import sleep

stocks = [
    {'TCKR': 'APPL', 'PRICE': 200},
    {'TCKR': 'GOOG', 'PRICE': 90},
    {'TCKR': 'TSLA', 'PRICE': 120},
    {'TCKR': 'MSFT', 'PRICE': 150},
    {'TCKR': 'INTL', 'PRICE': 70},
    {'TCKR': 'ELLT', 'PRICE': 0}
]


def buy_stock_events(observer):
    for stock in stocks:
        if(stock['PRICE'] > 100):
            observer.on_next(stock['TCKR'])
        elif(stock['PRICE'] <= 0):
            observer.on_error(stock['TCKR'])
    observer.on_completed()


source = Observable.create(buy_stock_events)

list_of_numbers = [a for a in range(100)]
generator_func = ({'TCKR': i, 'PRICE': i * 100} for i in list_of_numbers)


if __name__ == '__main__':
    i = 100
    while True:
        source.subscribe(on_next=lambda value: print(value),
                         on_completed=lambda: print("Completed trades"),
                         on_error=lambda e: print(e))
        stocks = []
        stocks.append(next(generator_func))
        i -= 1
        print('a')
        sleep(0.5)
        if i == 0:
            break
