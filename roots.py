"""
# This section is for a finite field not congruent to 1 mod 3
p=11
FF=range(p)

rootlist = open("roots.txt","w")

for f in FF:
    for root in FF:
        if (root**3)%p==f:
            rootlist.write("%d^3 = %d\n"%(root,f))
            break

rootlist.close()
"""

p=13
FF=range(p)

rootlist = open("roots.txt","w")

for f in FF:
    current = []
    for root in FF:
        if (root**3)%p==f:
            current.append(root)
    for yes in current:
        rootlist.write("%d^3 = "%(yes))
    if len(current)!=0:
        rootlist.write("%d\n"%(f))

rootlist.close()
