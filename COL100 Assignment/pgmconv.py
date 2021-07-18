fin = []
with open('lena.pgm') as f:
    lines = list(f.readlines())
    all = []
    for i in lines:
        all += list(i.split())
    for i in range(512):
        fin.append(all[512*i: 512*(i+1)])
print(len(fin), len(fin[0]), fin[0][0])
with open('finlen.pgm', 'w') as o:
    for i in fin:
        o.write(" ".join(i) + '\n')