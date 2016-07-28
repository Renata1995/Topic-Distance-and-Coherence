SET tc=15
FOR %%C IN (wup) DO (
python te_reuters.py b %tc% pp_reuters %%C no 250 20
FOR /L %%B IN (10,10,250) DO python te_readfile.py b %tc% pp_reuters %%C %%B 250 20
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py b %tc% pp_reuters %%C ic 250 20
FOR /L %%B IN (10,10,250) DO python te_readfile.py b %tc% pp_reuters %%C %%B 250 20
)