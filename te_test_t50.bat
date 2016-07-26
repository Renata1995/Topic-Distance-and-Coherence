FOR %%C IN (path lch wup) DO (
python te_reuters.py t 5 pp_reuters %%C no 250 40
FOR /L %%B IN (10,10,250) DO python te_readfile.py t 5 pp_reuters %%C %%B 250 40
)
FOR %%C IN (res lin jcn) DO (
python te_reuters.py t 5 pp_reuters %%C ic 250 40
FOR /L %%B IN (10,10,250) DO python te_readfile.py t 5 pp_reuters %%C %%B 250 40
)