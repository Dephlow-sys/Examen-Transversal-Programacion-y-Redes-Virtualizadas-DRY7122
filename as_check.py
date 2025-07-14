# as_check.py
as_number = int(input("Ingrese el número de Sistema Autónomo (AS): "))

# Rangos privados según IANA
private_ranges = [
    range(64512, 65535 + 1),
    range(4200000000, 4294967294 + 1)
]

es_privado = any(as_number in r for r in private_ranges)

if es_privado:
    print(f"El AS {as_number} es un Sistema Autónomo PRIVADO.")
else:
    print(f"El AS {as_number} es un Sistema Autónomo PÚBLICO.")

