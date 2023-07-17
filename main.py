#
#
import numpy as np
import pyrender
import trimesh
import matplotlib.pyplot as plt





def main(model_path, image_path):
    ## firts part: load and process the model 
    # load model

    model = trimesh.load(  model_path )

    # Create a Pyrender scene
    scene = pyrender.Scene()

    # Add the mesh to the scene

    if isinstance(model, trimesh.Trimesh):
        # Add the mesh to the scene
        mesh = pyrender.Mesh.from_trimesh(model)
        scene.add(mesh)
    elif isinstance(model, trimesh.Scene):
        # Add all the meshes in the scene to the Pyrender scene
        for name, mesh in model.geometry.items():
            mesh = pyrender.Mesh.from_trimesh(mesh)
            scene.add(mesh)

    # Set up the camera -- choose one of the two options
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 2.0, aspectRatio=1.0)
    camera_pose = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
    ])
    #camera = pyrender.OrthographicCamera(xmag=1.0, ymag=1.0)
    #camera_pose = np.eye(4)

    scene.add(camera, pose=camera_pose)

    # Set up the light -- choose one of the two options
    light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
                            innerConeAngle=np.pi/16.0,
                            outerConeAngle=np.pi/6.0)
    light_pose = np.copy(camera_pose)
    light_pose[2, 3] = 2.5
    # light = pyrender.PointLight(color=np.ones(3), intensity=10.0)
    # light_pose = np.array([
    #    [1, 0, 0, 1],
    #    [0, 1, 0, 1],
    #    [0, 0, 1, 2],
    #    [0, 0, 0, 1]
    # ])

    scene.add(light, pose=light_pose)

    # Render the scene
    r = pyrender.OffscreenRenderer(512,512)
    color, depth = r.render(scene)

    # Display the rendered image

    plt.figure()
    plt.imshow(color)
    plt.show()


    print("finished! ")


if __name__ == '__main__':
    model_path = "11/models/11.obj"
    image_path = "../11/11.jpg"
    main( model_path, image_path )
