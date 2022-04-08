import seaborn as sns

def create_heatmap(data):
    print(data)
    heatmap = sns.heatmap( data, square=True, vmin=0, vmax=100 )
    heatmap.axis('off')
    return heatmap

def save_heatmap_to_img(data, filename):
    fig = create_heatmap(data).get_figure()
    fig.savefig(filename)