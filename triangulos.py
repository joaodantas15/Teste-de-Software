a = float(input("Digite o lado A do triângulo"))
b = float(input("Digite o lado B do triângulo"))
c = float(input("Digite o lado C do triângulo"))

if a + b > c and a + c > b and b + c > a: 
    if a == b == c:
        print("Triângulo equilátero")
    elif a == b or a == c or b == c:
        print("Tirângulo isósceles")
    else:
        print("Triângulo escaleno")

else:
    print("medidas erradas")