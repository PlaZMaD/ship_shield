import matplotlib as plt
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import pickle
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
data = None
with open ('../db.pkl', 'rb') as f:
    data = pickle.load(f)
data2=[]
for key in data.keys():
    loc_x = json.loads(key)
    loc_y = data[key]
    # print(loc_y)
    data2.append((loc_x+[loc_y]))
mycols = np.array(['Z_{}'.format(i) for i in range(1,9)])
mainpart = np.ravel([['dX_in_{}'.format(i), 'dX_out_{}'.format(i), 'dY_in_{}'.format(i), 'dY_out_{}'.format(i), 'gap_in_{}'.format(i), 'gap_out_{}'.format(i)] for i in range(1,9) ])
mycols = np.append(mycols, mainpart)
mycols = np.append(mycols, 'score')
pd_data = pd.DataFrame(data2, columns=mycols)
pd_data['L']=pd_data[[m for m in mycols if "Z_" in m]].sum(axis=1)

print("We have {} events".format(len(pd_data.index)))
plt.plot(pd_data.index, pd_data['score'])
plt.xlabel("iteration")
plt.ylabel("FCN")
plt.yscale('log')
plt.savefig("updated_plot.png")
plt.cla()
print(pd_data['dX_in_6'])
plt.scatter(pd_data['dX_in_6'], pd_data['score'])
plt.xlabel("dX_5 in")
plt.ylabel('FCN')
plt.savefig("x-z.png")


plt.cla()
plt.scatter(pd_data['L'], pd_data['score'])
plt.xlabel('Length')
plt.ylabel('FCN')
plt.savefig('length.png')

plt.cla()
plt.scatter(pd_data.index, pd_data['L'])
plt.xlabel('i')
plt.ylabel('Length')
plt.savefig('iter_length.png')

print(", ".join(pd_data[pd_data['score']==pd_data['score'].min()].to_numpy().astype(int)))
