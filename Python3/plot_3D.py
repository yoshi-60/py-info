# matplotlib

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Figureと3DAxeS
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(111, projection='3d')

# 軸ラベルを設定
ax.set_xlabel("tx", size = 16)
ax.set_ylabel("ty", size = 16)
ax.set_zlabel("tz", size = 16)

# 円周率の定義
pi = np.pi

# (x,y)データを作成
tx =  np.linspace(-8, 8, 41)
ty =  np.linspace(-8, 8, 41)

# 格子点を作成
x, y = np.meshgrid(tx, ty)

# 高度の計算式
eps = 2.2204*np.exp(-16)
r = np.sqrt(x**2 + y**2) + eps
z = np.sin(r) / r

# 曲面を描画
#ax.plot_wireframe(x, y, z, cmap = "summer")
ax.plot_surface(x, y, z, cmap = "viridis")

# 底面に等高線を描画
#ax.contour(X, Y, Z, colors = "black", offset = -1)

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.view_init(elev=20, azim=55)

plt.show()
