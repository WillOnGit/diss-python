"""
# for writing out squares
p=7
FF=range(p)

out = open("h-w.txt","w")

for f in FF:
    out.write("%d^2 = %d\n"%(f,(f**2)%p))

out.close()
"""

"""
# for writing out x^3 + x + 1

p=7
FF=range(p)

out = open("h-w.txt","w")

for f in FF:
    out.write("%d^3 + %d + 1 = %d\n"%(f,f,(f**3 + f + 1)%p))

out.close()
"""

# for writing out points

p=7
FF=range(p)

out = open("h-w.txt","w")

for x in FF:
    for y in FF:
        if (y**2)%p == (x**3 + x + 1)%p:
            out.write("(%d,%d)\n"%(x,y))

out.close()
