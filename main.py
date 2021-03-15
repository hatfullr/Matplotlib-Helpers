import matplotlib.pyplot as plt

# Here we can test all the helpers we develop for Matplotlib

from ScaleAxes import scale_axes
fig, ax = plt.subplots(nrows=4,ncols=1,sharey=True)
for a in ax:
    a.tick_params(axis='both',which='both',direction='in',top=True,bottom=True,left=True,right=True)
plt.subplots_adjust(wspace=0.1)
old_width = ax[2].get_position().width
scale_axes(ax,(None,0.5,0.5,None))
new_width = ax[2].get_position().width
print(new_width/old_width)
plt.show()