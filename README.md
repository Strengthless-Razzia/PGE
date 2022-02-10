WINDOWS user : séquence de commandes à effectuer depuis le dossier projet dans le fichier ```commandes.txt``` (changer le chemin de python2.7 si nécessaire).
La dernière commande lance une démo de PNP et le calcul des angles de Bryant.
Le fichier ```Data\Plaque1\Benchmark\image1.bmp``` est une acquisition d'image par le robot dont les paramètres extrinsèques demandés à l'équipe déplacement robot étaient :
[[1,0,0,0],[0,-1,0,0],[0,0,-1,1000],[0,0,0,1]] (repère plaque par rapport au repère caméra, rotations en radians, distances en mm). Faire tourner PNP pour comparer les résultats obtenus. Les résultats sont affichés dans le terminal. Les angles de Bryant sont affichés à des fins d'utilisation par l'équipe IHM.
Pour tester une autre image, modifier la variable ```image``` du fichier ```HoleDetection\Paths.py```.
Pour changer le modèle de l'objet, modifier la variable ```model```du même fichier.