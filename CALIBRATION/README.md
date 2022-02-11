#### Ceci est la partie de travail du pôle Localisation du groupe PGE 2021-2022 de l'Upssitech. 

### Objectif de cette partie 

Localiser une plaque de type bombée dans le repère monde sans modèle 3D.

## Etapes

* [Calibration](https://github.com/Strengthless-Razzia/PGE/tree/Remi2/PLAQUE_BOMBEE/calibration) de la caméra, récupération des paramètres intrinsèques avec [calib.py](https://github.com/Strengthless-Razzia/PGE/blob/Remi2/PLAQUE_BOMBEE/calibration/calib.py).
* Prise de multiple photo 2D de la plaque bombée dans l'optique de faire une reconstruction 3D.
* Estimer la position de la plaque bombée dans le repère monde à partir du modèle 3D et d'une séquence d'image 2D.


## Ressources

* https://docs.opencv.org/3.3.1/dc/d2c/tutorial_real_time_pose.html
* https://www.eecis.udel.edu/~cer/arv/readings/old_mkss.pdf  (An Invitation to 3-D Vision From Images to Models)
* https://cvgl.stanford.edu/teaching/cs231a_winter1415/prev/projects/CS231a-FinalReport-sgmccann.pdf (3D Reconstruction from Multiple Images Shawn McCann)
* https://docs.opencv.org/4.x/d4/d18/tutorial_sfm_scene_reconstruction.html (OpenCV Scene reconstruction)

![Alt text](int.png?raw=true "Paramètres intrinsèques")
![Alt text](ext.png?raw=true "Paramètres extrinsèques")
