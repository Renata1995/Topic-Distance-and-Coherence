SET startw=25
FOR %%C IN (path lch wup) DO (
python te_reuters.py b 5 pp_reuters %%C no 250 startw
FOR /L %%B IN (10,10,250) DO python te_readfile.py b 5 pp_reuters %%C %%B 250 startw
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py b 5 pp_reuters %%C ic 250 starw
FOR /L %%B IN (10,10,250) DO python te_readfile.py b 5 pp_reuters %%C %%B 250 startw
)

FOR %%C IN (path lch wup) DO (
python te_reuters.py c 5 pp_reuters %%C no 250 startw
FOR /L %%B IN (10,10,250) DO python te_readfile.py c 5 pp_reuters %%C %%B 250 startw
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py c 5 pp_reuters %%C ic 250 40
FOR /L %%B IN (10,10,250) DO python te_readfile.py c 5 pp_reuters %%C %%B 250 startw
)