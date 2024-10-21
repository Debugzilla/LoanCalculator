from calendar import month_abbr
import math
import argparse
import sys
def print_titles():
    loan_principal = 'Loan principal: 1000'
    final_output = 'The loan has been repaid!'
    first_month = 'Month 1: repaid 250'
    second_month = 'Month 2: repaid 250'
    third_month = 'Month 3: repaid 500'

    print(loan_principal)
    print(first_month)
    print(second_month)
    print(third_month)
    print(final_output)


# Crear el parser
parser = argparse.ArgumentParser(description="Calculadora de préstamos")
parser.add_argument('--principal', type=int, required=False, help="Deuda total del préstamo")
parser.add_argument('--payment', type=float, required=False, help="Pago mensual del préstamo")
parser.add_argument('--interest', type=float, required=False, help="Tipo de interés del préstamo")
parser.add_argument('--periods', type=int, required=False, help="Mensualidades")
parser.add_argument('--type', type=str, required=False, help="Tipo de préstamo (annuity o diff)")

# Parsear los argumentos
args = parser.parse_args()


# Verificar que se proporcionen todos los argumentos necesarios y que sean válidos
if args.type not in ["annuity", "diff"]:
    print("Incorrect parameters")
    sys.exit(1)

if args.type == "diff" and args.payment is not None:
    print("Incorrect parameters")
    sys.exit(1)

if args.interest is None:
    print("Incorrect parameters")
    sys.exit(1)

if args.principal is not None and args.principal < 0:
    print("Incorrect parameters")
    sys.exit(1)

if args.payment is not None and args.payment < 0:
    print("Incorrect parameters")
    sys.exit(1)

if args.periods is not None and args.periods < 0:
    print("Incorrect parameters")
    sys.exit(1)

if args.interest < 0:
    print("Incorrect parameters")
    sys.exit(1)



# Verificar el número de argumentos, deben ser al menos 4
if len(sys.argv) < 4:
    print("Incorrect parameters")
    sys.exit(1)

# Verificar que el tipo de préstamo sea válido
if args.type not in ["annuity", "diff"]:
    print("Incorrect parameters")
    sys.exit(1)

# Convertir la tasa de interés anual a la tasa mensual
i = args.interest / (12 * 100)

# Caso 1: Calcular el número de pagos para un préstamo de tipo "annuity"
if args.principal and args.payment and args.interest and args.type == "annuity":
    # Calcular el número de pagos
    nPays = math.ceil(math.log(args.payment / (args.payment - i * args.principal), 1 + i))

    years = nPays // 12
    months = nPays % 12

    if years == 0:
        print(f"{months} months to repay the loan")
    elif months == 0:
        print(f"{years} years to repay the loan")
    else:
        print(f"{years} years and {months} months to repay the loan")

    total_pagado = args.payment * nPays
    overpayment = total_pagado - args.principal
    print(f"Overpayment = {math.ceil(overpayment)}")

# Caso 2: Calcular el pago mensual para un préstamo de tipo "annuity"
elif args.principal and args.interest and args.periods and args.type == "annuity":
    payment = math.ceil(args.principal * i / (1 - math.pow(1 + i, -args.periods)))
    print(f"Your annuity payment = {payment}!")

    total_pagado = payment * args.periods
    overpayment = total_pagado - args.principal
    print(f"Overpayment = {math.ceil(overpayment)}")

# Caso 3: Calcular pagos diferenciados para un préstamo de tipo "diff"
elif args.principal and args.periods and args.interest and args.type == "diff":
    m = 1
    total_pagado = 0

    while m <= args.periods:
        dm = (args.principal / args.periods) + i * (args.principal - (args.principal * (m - 1)) / args.periods)
        total_pagado += math.ceil(dm)
        print(f"Month {m}: payment is {math.ceil(dm)}")
        m += 1

    overpayment = total_pagado - args.principal
    print(f"Overpayment = {math.ceil(overpayment)}")

# Caso 4: Calcular el principal del préstamo para un préstamo de tipo "annuity"
elif args.payment and args.interest and args.periods and args.type == "annuity":
    interest = args.interest / 100 / 12
    principal = args.payment * (1 - (1 + interest) ** -args.periods) / interest
    print(f"Your loan principal = {int(principal)}!")

    total_pagado = args.payment * args.periods
    overpayment = total_pagado - principal
    print(f"Overpayment = {math.ceil(overpayment)}")

# Si no se cumple ninguna condición válida
else:
    print("Incorrect parameters")
    sys.exit(1)

# python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6
# Your loan principal = 800018!
# Overpayment = 246622
