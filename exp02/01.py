# editor : XiaoHei
# time : 2022/10/12 20:42
import numpy as np


def getTotalTourist(place):
    total = 0
    for dayTourist in place:
        total += dayTourist
    return total


(jzg_data,
 zjj_data,
 hk_data,
 dbhqc_data,
 shdisney_data) = np.loadtxt('tourist_data.csv',
                             skiprows=1,
                             dtype='int',
                             delimiter=',',
                             usecols=(1, 2, 3, 4, 5),
                             unpack=True)

jzg_total = getTotalTourist(jzg_data)
zjj_total = zjj_data.sum()
hk_total = hk_data.sum()
dbhqc_total = dbhqc_data.sum()
shdisney_total = shdisney_data.sum()

print("(numpy)这段时期到九寨沟旅游的总人数是:", jzg_total)
print("(numpy)这段时期到张家界旅游的总人数是:", zjj_total)
print("(numpy)这段时期到香港旅游的总人数是:", hk_total)
print("(numpy)这段时期到东部华侨城旅游的总人数是:", dbhqc_total)
print("(numpy)这段时期到上海迪士尼旅游的总人数是:", shdisney_total)
