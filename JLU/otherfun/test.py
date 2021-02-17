mlist=["1","2","3","4","5","6",]
clist=mlist.copy()
for i,v in enumerate(mlist):
    mlist[i]='%s'

mstr=",".join(mlist)
print(mstr)
print(clist)