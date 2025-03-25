#include "Image.h"

/** 
* @file mainPixel.cpp
* @brief Programme principal pour tester la classe Image
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/


int main() {
    Pixel rouge (205, 9, 13);
    Pixel jaune (242, 248, 22);
    Pixel bleu (120, 193, 246);

    // Première image
    Image image1 (64,48);
    image1.effacer(bleu);
    image1.dessinerRectangle(6, 8, 26, 21, rouge);
    image1.setPix(16,14,jaune);
    image1.setPix(46,33,jaune);
    image1.afficherConsole();
    image1.sauver("./data/image1.ppm");

    // Deuxième image
    Image image2;
    image2.ouvrir("./data/image1.ppm");
    image2.dessinerRectangle(23, 18, 37, 28, rouge);
    image2.dessinerRectangle(34, 26, 50, 36, jaune);
    image2.sauver("./data/image2.ppm");

    // Troisième image
    Image image3;
    image3.ouvrir("./data/image2.ppm");
    image3.dessinerRectangle(10, 20, 30, 40, jaune);
    image3.setPix(5, 5, rouge);
    image3.sauver("./data/image3.ppm");

    return 0;
}
