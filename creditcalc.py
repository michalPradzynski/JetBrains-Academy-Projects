import math
import sys

from argparse import ArgumentParser, Namespace
from typing import List

parser = ArgumentParser(
    description="This program let's you calculate differentiated or annuity loan payments"
)

parser.add_argument(
    "--type",
    type=str,
    choices=["annuity", "diff"],
    help="The type of payment: annuity or differentiated."
)
parser.add_argument(
    "--payment",
    type=int,
    help="The monthly payment amount. Used only in annuity calculations."
)
parser.add_argument(
    "--principal",
    type=int,
    help="The loan principal"
)
parser.add_argument(
    "--periods",
    type=int,
    help="Denotes the number of months needed to repay the loan."
)
parser.add_argument(
    "--interest",
    type=float,
    help="The nominal interest rate. Write without percent sign."
)

args: Namespace = parser.parse_args()


def initial_conditions() -> None:
    if (len(sys.argv) < 5
            or args.type not in ["annuity", "diff"]
            or (args.type == "diff" and args.payment is not None)
            or args.interest is None
            or (args.payment and args.payment < 0
                or args.principal and args.principal < 0
                or args.periods and args.periods < 0
                or args.interest and args.interest < 0)):
        print("Incorrect parameters")
        sys.exit()


def annuity_payments() -> None:
    if args.payment is None:
        # Monthly payment amount
        one_plus_i: float = math.pow(1 + nominal_interest, args.periods)
        annuity_payment_calc: float = args.principal * ((nominal_interest * one_plus_i) / (one_plus_i - 1))
        annuity_payment_calc = math.ceil(annuity_payment_calc)

        print(f"Your monthly payment = {annuity_payment_calc}!")

    elif args.principal is None:
        # Loan principal
        one_plus_i: float = math.pow(1 + nominal_interest, args.periods)
        loan_principal_calc: float = args.payment / ((nominal_interest * one_plus_i) / (one_plus_i - 1))
        loan_principal_calc = math.ceil(loan_principal_calc)

        print(f"Your loan principal = {loan_principal_calc}!")

    elif args.periods is None:
        # Number of months needed to repay the loan
        number_of_months: float = math.log((args.payment / (args.payment - nominal_interest * args.principal)),
                                    (1 + nominal_interest))
        number_of_months = math.ceil(number_of_months)
        years: float = number_of_months // 12
        months: float = number_of_months % 12
        overpayment: int = number_of_months * args.payment - args.principal

        if years == 0:
            print(f"It will take {months} months to repay this loan!")
        elif months == 0:
            print(f"It will take {years} years to repay this loan!")
        elif years > 0 and months > 0:
            print(f"It will take {years} years and {months} months to repay this loan!")

        print(f"Overpayment = {overpayment}")


def differentiated_payments() -> None:
    p_div_n: float = args.principal / args.periods
    monthly_payments: List = [math.ceil(p_div_n + nominal_interest * (args.principal - (p_div_n * (m - 1))))
                              for m in range(1, args.periods + 1)]
    overpayment: int = sum(monthly_payments) - args.principal

    for index, payment in enumerate(monthly_payments):
        print(f"Month {index +1}: payment is {payment}")

    print(f"Overpayment = {overpayment}")


if __name__ == '__main__':
    initial_conditions()
    nominal_interest: int = args.interest / (12 * 100)
    if args.type == "annuity":
        annuity_payments()
    elif args.type == "diff":
        differentiated_payments()
