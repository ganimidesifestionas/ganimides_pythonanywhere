import matplotlib.pyplot as plt
import io
import base64
 
def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates, label='visits')
    plt.xlabel('date')
    plt.ylabel('visits')
    plt.title("visits per day")
    plt.legend()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    #x = np.linspace(0, 2, 100)
    ##plt.plot(x, x, label='linear')
    #plt.plot(x, x**2, label='quadratic')
    #plt.plot(x, x**3, label='cubic')


    plt.show()
    return 'data:image/png;base64,{}'.format(graph_url)