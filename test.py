import random 
creamImgs = [[0]]*7

for i in range (0, len(creamImgs)):
    for j in range (0, len(creamImgs[i])):
        creamImgs[i][j] = f"{i}{j}"

print(f"first test: {creamImgs}")

imgs = [[], [], []]
imgs[0].append(random.randint(1, 5))

print(f"second test: {imgs}")