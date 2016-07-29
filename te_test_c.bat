SET tc=5
FOR %%C IN (jcn lin res path wup lch) DO (
FOR %%A in (t b c) DO FOR /L %%B IN (5,5,150) DO python te_read_sep.py %%A %tc% pp_reuters %%C 5 250 %%B
)