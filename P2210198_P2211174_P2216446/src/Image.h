#ifndef _IMAGE_H
#define _IMAGE_H

#include "Pixel.h"
#include <string>
using namespace std;

class Image{
    private:
        Pixel* tab;
        int dimx, dimy;

    public: 
        
        Image();

        Image(int dimensionX, int dimensionY);

        ~Image();

        Pixel getPix(int x, int y) const;

        Pixel * getPix(int x, int y);

        void setPix(int x, int y, Pixel couleur);

        void dessinerRectangle(int Xmin, int Xmax, int Ymin, int Ymax, Pixel couleur);

        void effacer(Pixel couleur);

        static void testRegression();

        void sauver(string &filename) const;

        void ouvrir(const string &filename);

        void afficherConsole();
};

#endif

