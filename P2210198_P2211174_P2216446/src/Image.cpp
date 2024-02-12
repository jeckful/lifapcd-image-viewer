#include <iostream>
#include <cassert>
#include "Image.h"
#include "Pixel.h"


/**
 * Constructeur par défaut,
 * Initialise les dimensions à 0.
 * */
Image::Image(){
    dimx = 0;
    dimy = 0;
}

/**
 * Constructeur avec Dimensions
 * @param dimensionX la largeur de l'image
 * @param dimensionY la longueur de l'image
 * Et on initialise un tableau de dimensionX * dimensionY pixel*/

Image::Image(int dimensionX, int dimensionY){
    dimx = dimensionX;
    dimy = dimensionY;
    tab = new Pixel[dimx * dimy];
    effacer(Pixel());
}

/**
 * Destructeur par défaut
 * Désallocation du tableau et mise à 0 des dimensions
 * */

Image::~Image(){
    delete[] tab;
    dimx = 0;
    dimy = 0;
}

/**
 * Récupère les valeurs du pixel de coordonnées x,y
 * si les paramètres sont valides sinon renvoie un Pixel par défaut
 * @param x y des entiers*/

Pixel Image::getPix(int x, int y)const{
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) return tab[y*dimx+x];
    return Pixel::Pixel();
    
}

/**
 * Récupère le pointeur du pixel de coordonnées x,y
 * si les paramètres sont valides sinon renvoie un pointeur null
 * @param x y des entiers*/

Pixel * Image::getPix(int x, int y){
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) return &tab[y*dimx+x];
    return nullptr;

}

/**
 * Modifie le pixel de coordonnées x,y par le Pixel couleur passé en paramètre
 * @param Couleur Un pixel
 * @param x un entier
 * @param y un entier
 * */

void Image::setPix(int x, int y, Pixel couleur){
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) tab[y*dimx+x] = couleur;
}

/**
 * Applique la couleur à tous les pixels compris
 * entre @param Xmin, @param YMin et @param XMax, @param YMax
 * */

void Image::dessinerRectangle(int Xmin, int Xmax, int Ymin, int Ymax, Pixel couleur){
    for(int i = Xmin; i < Xmax; i++ ){
        for(int j = Ymin; j < Ymax; j++ ){
            setPix(i, j, couleur);
        }
    }
}

/**
 * Applique la @param couleur à tous les pixels de l'image
 * */

void Image::effacer(Pixel couleur){
    dessinerRectangle(0, dimx, 0, dimy, couleur);
}

/**
 * Test de toutes les instances précédentes
 * */

void Image::testRegression() {
    
    Image testImageDefault;
    assert(testImageDefault.dimx == 0 && testImageDefault.dimy == 0);
    std::cout << "constructeur par default OK!" << std::endl;

    
    Image imageTest(3, 4);

    assert(imageTest.dimx == 3 && imageTest.dimy == 4);
    std::cout << "constructeur OK!." << std::endl;

    imageTest.effacer(Pixel(255, 0, 0));  
    for (int i = 0; i < imageTest.dimx; ++i) {
        for (int j = 0; j < imageTest.dimy; ++j) {
            assert(imageTest.getPix(i, j) == Pixel(255, 0, 0));
        }
    }
    std::cout << "effacer OK!" << std::endl;

    imageTest.dessinerRectangle(1, 2, 1, 2, Pixel(0, 255, 0)); 
    assert(imageTest.getPix(0, 0) == Pixel(255, 0, 0));
    assert(imageTest.getPix(1, 1) == Pixel(0, 255, 0));
    assert(imageTest.getPix(2, 2) == Pixel(255, 0, 0));
    std::cout << "dessinerRectangle OK!" << std::endl;

    imageTest.setPix(1, 1, Pixel(0, 0, 255));  
    assert(imageTest.getPix(1, 1) == Pixel(0, 0, 255));
    std::cout << "getPix et setPix OK!" << std::endl;


    std::cout << " CA FONCTIONNE !!" << std::endl;
}
