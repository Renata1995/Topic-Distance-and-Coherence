SET tc=5
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO python te_reuters.py %%A %tc% pp_reuters %%C ic 250 
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO python te_reuters.py %%A %tc% pp_reuters %%C no 250 
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)

