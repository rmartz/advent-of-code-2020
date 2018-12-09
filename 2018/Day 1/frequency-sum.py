with open('data.txt', 'r') as fp:
    print(sum(int(row) for row in fp))
