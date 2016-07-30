SET tc=15
FOR %%C IN (jcn wup) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (5,5,150) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250 20
)





