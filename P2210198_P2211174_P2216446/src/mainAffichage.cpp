#include "Image.h"
#include "ImageViewer.h"


int main (int argc, char** argv) {
 Image image (512,512);
 image.ouvrir("./data/image3.ppm");

 ImageViewer imview;
 imview.afficher(image);
 return 0;
}
