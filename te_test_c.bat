SET tc=5
FOR %%C IN (path) DO (
FOR %%A in (t b c) DO FOR %%B IN (0) DO python te_read_sep.py %%A %tc% pp_reuters %%C 5 250 %%B
)