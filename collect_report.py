#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import argparse
import logging

from finance.stock import get_stock, get_plate
from finance.finance.report import create_finance, download_finance_report


logger = logging.getLogger(__name__)


def stock_main(parser):
    args = parser.parse_args()

    level = logging.WARNING - (args.verbose * 10)
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)

    stocks = []
    if args.by_plate:
        for code in args.code:
            plate = get_plate(code)
            if plate:
                stocks += plate.stocks
    elif args.code:
        for code in args.code:
            s = get_stock(code)
            if s:
                stocks.append(s)
    else:
        stocks = get_stock()

    overwrite = not args.update

    mcodes = [stock.mcode for stock in stocks]

    if args.download:
        download_finance_report(mcodes, overwrite=overwrite)
    elif args.create_db:
        create_finance(typ='json')
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stock finance report')
    parser.add_argument('-v', '--verbose', help='verbose help',
                        action='count', default=1)
    parser.add_argument(
        '--update',
        action='store_true',
        help='No overwrite, append'
    )

    download_group = parser.add_argument_group('Download')
    download_group.add_argument(
        '--download',
        action='store_true',
        help='download report'
    )

    download_group.add_argument(
        '--pdf-report',
        action='store_true',
        help='download PDF report',
    )

    download_group.add_argument(
        '--by-plate',
        action='store_true',
        help='download report by THS plate.',
    )

    db_group = parser.add_argument_group('Create Database')
    db_group.add_argument(
        '--create-db',
        action='store_true',
        help='collect finance report and create database'
    )
    parser.add_argument('code',
                        nargs='*', help='stock mcode or plate code')
    stock_main(parser)
