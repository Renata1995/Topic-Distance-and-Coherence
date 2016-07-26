SET tc=15
FOR %%C IN (path lch wup) DO (
python te_reuters.py b %tc% pp_reuters %%C no 250 
FOR /L %%B IN (10,10,250) DO python te_readfile.py b %tc% pp_reuters %%C %%B 250
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py b %tc% pp_reuters %%C ic 250
FOR /L %%B IN (10,10,250) DO python te_readfile.py b %tc% pp_reuters %%C %%B 250
)