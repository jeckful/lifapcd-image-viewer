#include "Pixel.h"



        
Pixel::Pixel(){
    r = g = b = 0;
};

Pixel::Pixel(unsigned char red, unsigned char green, unsigned char blue){
    r = red;
    g = green;
    b = blue;
};

unsigned char Pixel::getRed() const {
    return r;
}

unsigned char Pixel::getGreen() const {
    return g;
}

unsigned char Pixel::getBlue() const {
    return b;
}

