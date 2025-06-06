def process_input(value):
    if value > 0:
        if value % 2 == 0:
            if value > 10:
                if value < 50:
                    if value == 20:
                        return 'Value is exactly 20'
                    else:
                        return 'Value is an even number between 10 and 50'
                else:
                    return 'Value is even and greater than 50'
            else:
                return 'Value is even and less than or equal to 10'
        else:
            if value > 10:
                if value < 50:
                    return 'Value is an odd number between 10 and 50'
                else:
                    return 'Value is odd and greater than 50'
            else:
                return 'Value is odd and less than or equal to 10'
    else:
        return 'Value is zero or negative'

for i in range(25):
    print(process_input(i))
