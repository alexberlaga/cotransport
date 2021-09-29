
au_a = 1000
aw_a = 100
au_b = 900
aw_b = 100
aGAMMA = 1
aX = 2
auap = 100
aubp = 120

antiport_defaults = [au_a, aw_a, au_b, aw_b, aGAMMA, aX, auap, aubp]

paramslist = []
for i in range(12):
    paramslist.append(antiport_defaults.copy())
paramslist[0][7] = 890
paramslist[1][7] = 890
paramslist[2][7] = 890
paramslist[3][7] = 890
paramslist[4][7] = 500
paramslist[5][7] = 500
paramslist[6][7] = 500
paramslist[7][7] = 500
paramslist[8][7] = 120
paramslist[9][7] = 120
paramslist[10][7] = 120
paramslist[11][7] = 120

paramslist[0][5] = 0.5
paramslist[1][5] = 1
paramslist[2][5] = 2
paramslist[3][5] = 5
paramslist[4][5] = 0.5
paramslist[5][5] = 1
paramslist[6][5] = 2
paramslist[7][5] = 5
paramslist[8][5] = 0.5
paramslist[9][5] = 1
paramslist[10][5] = 2
paramslist[11][5] = 5

my_params = paramslist