#ifndef _PIXEL_H
#define _PIXEL_H

class Pixel{
    private: 

        unsigned char r, g, b;
    
    public:
        
        Pixel();
        Pixel(unsigned char red, unsigned char green, unsigned char blue);

        unsigned char getRed() const;
        unsigned char getGreen() const;
        unsigned char getBlue() const;

        bool operator==(const Pixel& other) const {
        return (r == other.r) && (g == other.g) && (b == other.b);
    }

};


#endif
