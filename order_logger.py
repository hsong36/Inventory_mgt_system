# Haena Song, CIS 345, TTH 10:30, Final_Project
import csv


def log_customer(data):
    with open('customers.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(data)
    return None


def log_transaction(data):
    with open('transactions.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(data)
    return None


def format_money(money):
    dollar = f'{money: .2f}'
    return f'$ {dollar}'
