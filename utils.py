def escolher_enum(enum_class, titulo):
    print(f"\n{titulo}")

    valores = list(enum_class)

    for i, item in enumerate(valores, start=1):
        print(f"{i} - {item.value}")

    try:
        escolha = int(input("Escolha: "))
        return valores[escolha - 1].value
    except:
        print("Opção inválida")
        return None