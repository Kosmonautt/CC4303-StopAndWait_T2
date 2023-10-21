wea = "hola pirinola"
wea = wea.encode()

for i in range(0, len(wea)+1):
    print(wea[0:i])
    print(wea[i:len(wea)])
    print("////////////////")