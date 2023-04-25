test = "R:hello"

if test.startswith("R:"):
    p1, p2 = test.split(":")

    print(p1)
    print(p2)
else:
    print("no")