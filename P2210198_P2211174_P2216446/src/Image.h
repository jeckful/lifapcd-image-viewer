#ifndef _IMAGE_H
#define _IMAGE_H

#include "Pixel.h"
#include <string>


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

        void sauver(const std::string &filename) const;

        void ouvrir(const std::string &filename);

        void afficherConsole();

        const Pixel* getTab() const { return tab; }
        int getDimX() const { return dimx; }
        int getDimY() const { return dimy; }
};

#endif

