#include <iostream>
#include <cassert>
#include "Image.h"
#include "Pixel.h"
#include <fstream>

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
    return Pixel();
    
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
    using namespace std;

    Image testImageDefault;
    assert(testImageDefault.dimx == 0 && testImageDefault.dimy == 0);
    cout << "constructeur par default OK!" << endl;

    
    Image imageTest(3, 4);

    assert(imageTest.dimx == 3 && imageTest.dimy == 4);
    cout << "constructeur OK!." << endl;

    Pixel* PixelPtr;
    
    imageTest.effacer(Pixel(255, 0, 0));  
    for (int i = 0; i < imageTest.dimx; ++i) {
        for (int j = 0; j < imageTest.dimy; ++j) {
            PixelPtr = imageTest.getPix(i, j); 
            assert(PixelPtr != nullptr); 
            Pixel Pixel = *PixelPtr; 
            assert(Pixel.r == 255 && Pixel.g == 0 && Pixel.b == 0);
            
        }
        
    }
    cout << "effacer OK!" << endl;

    

    imageTest.dessinerRectangle(1, 2, 1, 2, Pixel(0, 255, 0)); 
    Pixel* pixel1 = imageTest.getPix(1, 1); 
    assert(pixel1 != nullptr); 
    assert(pixel1->r == 0 && pixel1->g == 255 && pixel1->b == 0); 

    Pixel* pixel2 = imageTest.getPix(2, 2); 
    assert(pixel2 != nullptr); 
    assert(pixel2->r == 255 && pixel2->g == 0 && pixel2->b == 0); 

    cout << "dessinerRectangle OK!" << endl;

    imageTest.setPix(1, 1, Pixel(0, 0, 255));  
    Pixel* modifiedPixelPtr = imageTest.getPix(1, 1); 
    assert(modifiedPixelPtr != nullptr); 
    Pixel modifiedPixel = *modifiedPixelPtr; 
    assert(modifiedPixel.r == 0 && modifiedPixel.g == 0 && modifiedPixel.b == 255);
    cout << "getPix et setPix OK!" << endl;
            
    

    cout << " CA FONCTIONNE !!" << endl;

}

void Image::sauver(string &filename) const
{
    using namespace std;
    ofstream fichier(filename.c_str());
    assert(fichier.is_open());
    fichier << "P3" << endl;
    fichier << dimx << " " << dimy << endl;
    fichier << "255" << endl;
    for (unsigned int y = 0; y < dimy; ++y)
        for (unsigned int x = 0; x < dimx; ++x)
        {
            Pixel pix = getPix(x, y);
            fichier << +pix.r << " " << +pix.g << " " << +pix.b << " ";
            ++x;
        }
    cout << "Sauvegarde de l'image " << filename << " ... OK\n";
    fichier.close();
}

void Image::ouvrir(const string &filename)
{
    ifstream fichier(filename.c_str());
    assert(fichier.is_open());
    char r, g, b;
    string mot;
    dimx = dimy = 0;
    fichier >> mot >> dimx >> dimy >> mot;
    assert(dimx > 0 && dimy > 0);
    if (tab != nullptr)
        delete[] tab;
    tab = new Pixel[dimx * dimy];
    for (unsigned int y = 0; y < dimy; ++y)
        for (unsigned int x = 0; x < dimx; ++x)
        {
            fichier >> r >> b >> g;
            getPix(x, y)->r = r;
            getPix(x, y)->g = g;
            getPix(x, y)->b = b;
        }
    fichier.close();
    cout << "Lecture de l'image " << filename << " ... OK\n";
}

void Image::afficherConsole()
{
    cout << dimx << " " << dimy << endl;
    for (unsigned int y = 0; y < dimy; ++y)
    {
        for (unsigned int x = 0; x < dimx; ++x)
        {
            Pixel* pix = getPix(x, y);
            cout << +pix->r << " " << +pix->g << " " << +pix->b << " ";
        }
        cout << endl;
    }
}
