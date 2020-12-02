def find_sum(data, target):
    high = len(data)-1
    low = 0
    while high >= low:
        high_val = data[high]
        low_val = data[low]
        total = high_val + low_val
        if total == target:
            return high_val, low_val
        elif total < target:
            # Need to increase the total
            # Because every low number can pair with exactly one high number,
            # if the value is too low then there is no matching high number
            low += 1
        else:
            # Need to decrease the total
            # Similarly, if the value is too high then there is no matching
            #  low number. Use the next high to see how it fairs
            high -= 1
    raise Exception("Target was not found")


with open('./data.txt', 'r') as fp:
    data = sorted(int(line) for line in fp.readlines())

high, low = find_sum(data, 2020)
print(high * low)
