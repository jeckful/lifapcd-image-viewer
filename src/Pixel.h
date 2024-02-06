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


class Pixel{
    private: 



        unsigned char r, g, b; ///< 3 unsigned char nommé r, g et b pour faire varier la couleur du pixel. Utilisation de unsigned char car valeur limité à 256 valeurs.
    
    public:
        
        /**
        * Constructeur par défaut,
        * Initialise red, green et blue à 0.
        * */
        Pixel();

        /**
        * Constructeur avec Dimensions
        * @param red la tonalité de rouge
        * @param green la tonalité de vert
        * @param blue la tonalité de bleu
        * Et on initialise la couleur du pixel*/

        Pixel(unsigned char red, unsigned char green, unsigned char blue);

        /**
        * fonctions qui retournent les tonalités RGB d'un pixel, elles prennent aucun paramètre.
        */

        unsigned char getRed() const; ///<fonctions qui retournent les tonalités rouge d'un pixel, elles prennent aucun paramètre.
        unsigned char getGreen() const; ///<fonctions qui retournent les tonalités verte d'un pixel, elles prennent aucun paramètre.
        unsigned char getBlue() const; ///<fonctions qui retournent les tonalités bleu d'un pixel, elles prennent aucun paramètre.

        /**
        * fonction operator == pour gérer les égalités entre pixel pour la static void
        * @param other un objet 'Pixel' avec lequel on compare l'objet 'Pixel' actuel
        * on retourne true ou false */

        bool operator==(const Pixel& other) const {
        return (r == other.r) && (g == other.g) && (b == other.b);
    }

};


#endif
