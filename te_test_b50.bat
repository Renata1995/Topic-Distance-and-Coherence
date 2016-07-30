SET tc=5
SET startw=0
FOR %%C IN (path) DO (python te_reuters.py b %tc% pp_reuters %%C no 250 %startw%)
