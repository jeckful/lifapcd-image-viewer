#ifndef _PIXEL_H
#define _PIXEL_H

/** 
* @file Pixel.h
* fichier .h de la classe "pixel"
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

/**
 * @class Pixel
 *
 * @brief elle génére un pixel avec une couleur
 *
 */


struct Pixel{
    



        unsigned char r, g, b; ///< 3 unsigned char nommé r, g et b pour faire varier la couleur du pixel. Utilisation de unsigned char car valeur limité à 256 valeurs.
    
    
        
        /**
        * Constructeur par défaut,
        * @brief Initialise red, green et blue à 0.
        * */
        Pixel() : r(0), g(0), b(0) {}

        Pixel(unsigned char nr, unsigned char ng, unsigned char nb) : r(nr), g(ng), b(nb) {}



    

};


#endif
