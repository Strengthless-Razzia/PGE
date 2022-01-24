import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from extractHoles import getAllCircles

import numpy as np



def select_points(nb_points, img_path, points_file_path, edges_file_path, step_file_path):
    
    def on_click(event, clicked_points, color_list):

        u, v = event.xdata, event.ydata
        clicked_points.append(([u, v]))

        print("[*] 2D Point {:d}: ({:.2f}, {:.2f})".format(
                len(clicked_points), clicked_points[-1][0], clicked_points[-1][1]))

        if len(color_list) >= len(clicked_points) > 0:
            ax2.scatter(clicked_points[-1][0], clicked_points[-1][1], color=color_list[len(clicked_points) - 1])
        
        else:
            # plot the line
            data = ax2.scatter(clicked_points[-1][0], clicked_points[-1][1])
            color_list.append(data.get_facecolor()[0].copy())

        # show the id of the edge

        ax2.text(clicked_points[-1][0], 
                    clicked_points[-1][1], 
                    str(len(clicked_points)),
                    color=color_list[len(clicked_points) - 1])

        fig2.canvas.draw()

        return True
    
    def on_pick(event, picked_points_Ro, color_list):

        if event.artist in lines:
            ind = lines.index(event.artist)
            
            X = (X1_Ro[ind] + X2_Ro[ind]) / 2
            Y = (Y1_Ro[ind] + Y2_Ro[ind]) / 2
            Z = (Z1_Ro[ind] + Z2_Ro[ind]) / 2

            

            if not (np.equal(np.array([X, Y, Z]), holes_point_3D).all(axis=1).any() and \
                [X, Y, Z] not in picked_points_Ro):
                return True

            picked_points_Ro.append([X, Y, Z])

            if len(color_list) >= len(picked_points_Ro) > 0:
                
                ax1.scatter(X, Y, Z, color=color_list[len(picked_points_Ro) - 1])
        
            else:
            # plot the line
                data = ax1.scatter(X, Y, Z)
                color_list.append(data.get_facecolor()[0].copy())

            lines[ind].set_color(color_list[len(picked_points_Ro) - 1])
            ax1.text(X, Y, Z, str(len(picked_points_Ro)), color=color_list[len(picked_points_Ro) - 1])

            fig1.canvas.draw()
            

            print("[*] 3D Point {:d}: ({:.2f}, {:.2f}, {:.2f})".format(
                len(picked_points_Ro), X, Y, Z))
            

    
    color_list = []
    picked_points_Ro = []
    clicked_points = []

    model_points_3DRo = np.loadtxt(points_file_path, dtype=float)
    model_edges = np.loadtxt(edges_file_path, dtype=int)

    with open(step_file_path) as f:
        file = f.readlines()

    holes_point_3D, diameters = getAllCircles(file, getBothFaces=False)


    XYZ1_Ro = model_points_3DRo[model_edges[:, 0]]
    XYZ2_Ro = model_points_3DRo[model_edges[:, 1]]
    model3D_Ro = np.concatenate([XYZ1_Ro, XYZ2_Ro], axis=1)
    X1_Ro, Y1_Ro, Z1_Ro = XYZ1_Ro[:, 0], XYZ1_Ro[:, 1], XYZ1_Ro[:, 2]
    X2_Ro, Y2_Ro, Z2_Ro = XYZ2_Ro[:, 0], XYZ2_Ro[:, 1], XYZ2_Ro[:, 2]

    image = mpimg.imread(img_path)

    # Plot the model
    fig1 = plt.figure(1)
    ax1, lines = plot_3d_model(model3D_Ro, fig1)
    ax1.set_zlim(-20,20)
    ax1.scatter(holes_point_3D[:,0], holes_point_3D[:,1], holes_point_3D[:,2], color='green', alpha=0.4)
    fig1.canvas.mpl_connect('pick_event', lambda event: on_pick(event, picked_points_Ro, color_list))  # Listen to mouse click event within figure 1
    plt.show(block=False)

    # Plot left image
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    plt.imshow(image)
    fig2.canvas.mpl_connect('button_press_event',  # Listen to mouse click event within figure 2
                            lambda event: on_click(event, clicked_points, color_list))
    plt.show(block=False)

    while not (len(picked_points_Ro) == len(clicked_points) >= nb_points):
        plt.pause(1)
    
    picked_points_Ro = np.array(picked_points_Ro)
    clicked_points = np.array(clicked_points)

    return picked_points_Ro, clicked_points


def plot_3d_model(model, fig):
    ax = Axes3D(fig)

    lines = []
    for idx in range(model.shape[0]):
        lines.append(ax.plot([model[idx, 0], model[idx, 3]],
                                [model[idx, 1], model[idx, 4]],
                                [model[idx, 2], model[idx, 5]],
                                color='k', picker=5)[0])
    ax.scatter(0, 0, 0, color='r', s=30)
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_zlabel('z (mm)')
    ax.set_title('3D model')

    return ax, lines


if __name__ == '__main__':
    picked_points_Ro, clicked_points = select_points(4, "./Data/Plaque1/Cognex/image6.bmp", 
                        "Data/Plaque1/Model/Plaque_1.xyz",
                        "Data/Plaque1/Model/Plaque_1.edges",
                        "Data/Plaque1/Model/Plaque_1.stp")
    

    with open('HoleDetection/Points3D/picked_points_Ro_Cognex6.npy', 'wb') as f:
        np.save(f, picked_points_Ro, allow_pickle=False)

    with open('HoleDetection/Points2D/clicked_points_Cognex6.npy', 'wb') as f:
        np.save(f, clicked_points, allow_pickle=False)

        
    