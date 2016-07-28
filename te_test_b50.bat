SET tc=15
SET startw=20
FOR %%C IN (path lch wup) DO (
python te_reuters.py c %tc% pp_reuters %%C no 250 %startw%
FOR /L %%B IN (10,10,250) DO python te_readfile.py c %tc% pp_reuters %%C %%B 250 %startw%
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py c %tc% pp_reuters %%C ic 250 %startw%
FOR /L %%B IN (10,10,250) DO python te_readfile.py c %tc% pp_reuters %%C %%B 250 %startw%
)

FOR %%C IN (path lch wup) DO (
python te_reuters.py t %tc% pp_reuters %%C no 250 %startw%
FOR /L %%B IN (10,10,250) DO python te_readfile.py c %tc% pp_reuters %%C %%B 250 %startw%
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py t %tc% pp_reuters %%C ic 250 %startw%
FOR /L %%B IN (10,10,250) DO python te_readfile.py c %tc% pp_reuters %%C %%B 250 %startw%
)

FOR %%C IN (res lin jcn) DO (
python te_reuters.py b %tc% pp_reuters %%C ic 250 %startw%
FOR /L %%B IN (10,10,250) DO python te_readfile.py c %tc% pp_reuters %%C %%B 250 %startw%
)


