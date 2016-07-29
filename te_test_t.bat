SET tc=10
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)

SET tc=10
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250 50
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250 50
)

SET tc=15
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)

SET tc=15
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250 20
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250 20
)

SET tc=20
FOR %%C IN (res lin jcn) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)
FOR %%C IN (lch wup path) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (10,10,250) DO python te_readfile.py %%A %tc% pp_reuters %%C %%B 250
)





