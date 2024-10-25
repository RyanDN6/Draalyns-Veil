def levels():
    xpLevel = {}
    for i in range(1, 100):
        xpLevel[i] = (i * i * 2) + i * 3
    for k in xpLevel.keys():
        print(f"Level {k}: {xpLevel[k]}")
"""
    for i in range(10, 20):
        xpLevel[i] = (14 * i) + i + 12
    
    for i in range(20, 40):
        xpLevel[i] = (20 * i) + i - 25
"""    

levels()