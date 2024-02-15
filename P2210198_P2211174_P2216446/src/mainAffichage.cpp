#include "Image.h"
#include "ImageViewer.h"

/** 
* @file mainAffichage.cpp
* @brief Programme principal pour afficher une image à l'aide de la classe ImageViewer
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/


int main (int argc, char** argv) {
 Image image (1000,1000);
 image.ouvrir("./data/image3.ppm");

 ImageViewer imview;
 imview.afficher(image);
 return 0;
}
