FOR %%B IN (5 10 15 20) DO FOR %%A in (t b c) DO python te_reuters.py %%A %%B pp_reuters jcn ic 250
FOR %%A in (t b c) DO python te_reuters.py %%A 5 pp_reuters jcn ic 250 25
FOR %%A in (t b c) DO python te_reuters.py %%A 10 pp_reuters jcn ic 250 50
FOR %%A in (t b c) DO python te_reuters.py %%A 15 pp_reuters jcn ic 250 20

