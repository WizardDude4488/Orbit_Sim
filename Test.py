import math

def calculation(number1, number2):
    apple = number1 * 2 - number2 * 2
    number1 = 2 - apple
    number2 = apple + 2
    print(number1, number2)
    return [number1, number2]

def cycle(final_subdivision, number1, number2):
    current_subdivision = 0

    while current_subdivision < final_subdivision:
        banana = calculation(number1, number2)
        number1 = banana[0]
        number2 = banana[1]

        current_subdivision = current_subdivision + 1


    print("\n")
    print(banana)


cycle(500, 5, 6)

