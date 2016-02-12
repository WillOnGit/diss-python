FF = range(0,11)

sol = []

for x in FF:
	for y in FF:
		for z in FF:
			# print (x,y,z)
			if x == 0 and y == 0 and z == 0:
				pass
			elif (x + y + z)%11 == 0:
				sol = sol + [(x,y,z)]

# print sol

newsol = []
nFF = [2,3,4,5,6,7,8,9,10]

for oldsol in sol:
	flag = 0
	for test in newsol:
		for scalar in nFF:
			multiple = tuple([(i * scalar)%11 for i in oldsol])
			if multiple==test:
				flag = 1
	if flag == 0:
		newsol = newsol + [oldsol]

print "There were %i solutions found for x + y + z = 0:"%(len(newsol))
print newsol

# copied code to modify for cubic equation

csol = []

for x in FF:
	for y in FF:
		for z in FF:
			# print (x,y,z)
			if x == 0 and y == 0 and z == 0:
				pass
			elif (x**3 + y**3 + z**3)%11 == 0:
				csol = csol + [(x,y,z)]

# print csol

cnewsol = []
nFF = [2,3,4,5,6,7,8,9,10]

for oldsol in csol:
	flag = 0
	for test in cnewsol:
		for scalar in nFF:
			multiple = tuple([(i * scalar)%11 for i in oldsol])
			if multiple==test:
				flag = 1
	if flag == 0:
		cnewsol = cnewsol + [oldsol]

print "There were %i solutions found for x^3 + y^3 + z^3 = 0:"%(len(cnewsol))
print cnewsol

# END OF copied code to modify for cubic equation

"""
for x in FF:
	print "%i cubed is %i"%(x,(x**3)%11)
"""

cubednewsol=[]

for x in newsol:
	cubednewsol = cubednewsol + [tuple([(i ** 3)%11 for i in x])]

# print cubednewsol

for cubed in cubednewsol:
	print (cubed[0] + cubed[1] + cubed[2])%11
