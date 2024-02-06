#include <iostream>
#include <cassert>
#include "Image.h"
#include "Pixel.h"

Image::Image(){
    dimx = 0;
    dimy = 0;
}

Image::Image(int dimensionX, int dimensionY){
    dimx = dimensionX;
    dimy = dimensionY;
    tab = new Pixel[dimx * dimy];
    effacer(Pixel());
}

Image::~Image(){
    delete[] tab;
    dimx = 0;
    dimy = 0;
}

Pixel Image::getPix(int x, int y){
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) return tab[y*dimx+x];
    return Pixel::Pixel();
    
}

void Image::setPix(int x, int y, Pixel couleur){
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) tab[y*dimx+x] = couleur;
}

void Image::dessinerRectangle(int Xmin, int Xmax, int Ymin, int Ymax, Pixel couleur){
    for(int i = Xmin; i < Xmax; i++ ){
        for(int j = Ymin; j < Ymax; j++ ){
            setPix(i, j, couleur);
        }
    }
};

void Image::effacer(Pixel couleur){
    dessinerRectangle(0, dimx, 0, dimy, couleur);
}



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
