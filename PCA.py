import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold, datasets
#Prepare the data

from sklearn import manifold, datasets

X_tsne = manifold.TSNE(n_components=2, init='random', random_state=5, verbose=1).fit_transform(X)
print(X_tsne)