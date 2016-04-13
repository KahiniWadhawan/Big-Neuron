from lightning import Lightning
from numpy import random,
 
lgn = Lightning()
 
x = random.randn(100)
y = random.randn(100)
 
viz = lgn.scatterstreaming(x, y)
 
for _ in range(100):
    x = random.randn(100)
    y = random.randn(100)
    viz.append(x, y)