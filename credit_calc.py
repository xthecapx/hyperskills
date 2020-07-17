import argparse
from math import log, ceil

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=int)

args = parser.parse_args()
commands = list(filter(
    None, [args.type, args.principal, args.periods, args.payment, args.interest]))

if not args.type in ('annuity', 'diff') or args.type == None or len(commands) < 4:
    print('Incorrect parameters')
elif args.interest == None:
    print('Incorrect parameters')
elif args.periods == None:
    interest = args.interest / (100 * 12)
    periods = ceil(
        log(args.payment / (args.payment - (interest * args.principal)), 1 + interest))
    years = periods // 12
    months = periods - years * 12
    message = ''

    if months % 12 == 0:
        message = f'{years} years'

    elif months < 12 and years == 0:
        message = f'{months} months'
    else:
        message = f'{years} years and {months} months'

    overpayment = args.payment * periods - args.principal

    print(f"You need {message} to repay this credit!")
    print(f"Overpayment = {overpayment}")
elif args.principal == None:
    interest = args.interest / (12 * 100)
    calc = (1 + interest) ** args.periods
    principal = ceil(args.payment / (interest * calc / (calc - 1)))
    overpayment = args.payment * args.periods - principal

    print(f"Your credit principal = {principal}!")
    print(f"Overpayment = {overpayment}")
elif args.payment == None:
    interest = args.interest / (12 * 100)

    if args.type == 'diff':
        all_payments = 0

        for i in range(1, args.periods + 1):
            diff_pay = ceil(
                args.principal / args.periods + interest *
                (args.principal - args.principal * (i - 1) / args.periods)
            )
            all_payments += diff_pay
            print(f"Month {i}: paid out {diff_pay}")

        overpayment = all_payments - args.principal

        print(f"Overpayment = {overpayment}")
    else:
        calc = (1 + interest) ** args.periods
        annuity = ceil(args.principal * (interest * calc) / (calc - 1))
        overpayment = annuity * args.periods - args.principal
        
        print(f'Your annuity payment = {annuity}!')
        print(f"Overpayment = {overpayment}")
