SET tc=20
FOR %%C IN (jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (5,5,150) DO python te_readfile.py %%A %tc% pp_brown %%C %%B 150
)



