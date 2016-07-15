FOR /L %%A IN (4,1,8) DO FOR /L %%B IN (1,1,3) DO python GenSimFileTest.py 1 pp_data %%A b 0 "sim_output/binary/topic%%A%%B"
FOR /L %%A IN (4,1,8) DO FOR /L %%B IN (1,1,3) DO python GenSimFileTest.py 1 pp_data %%A t 0 "sim_output/tfidf/topic%%A%%B"
FOR /L %%A IN (4,1,8) DO FOR /L %%B IN (1,1,3) DO python GenSimFileTest.py 1 pp_data %%A c 0 "sim_output/bow/topic%%A%%B"

python SimilarityTest.py b
python SimilarityTest.py t
python SimilarityTest.py c