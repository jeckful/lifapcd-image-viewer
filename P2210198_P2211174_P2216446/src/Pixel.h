#ifndef _PIXEL_H
#define _PIXEL_H

/** 
* @file Pixel.h
* @brief fichier .h de la structure "Pixel"
* Ce fichier contient la définition de la structure Pixel, qui représente un pixel avec une couleur RGB.
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

/**
 * @struct Pixel
 *
 * @brief Structure représentant un pixel avec une couleur RGB.
 *
 */
struct Pixel {
    unsigned char r, g, b; ///< Trois composantes de couleur : rouge, vert, bleu.

    /**
    * @brief Constructeur par défaut qui initialise les composantes RGB à 0.
    */
    Pixel() : r(0), g(0), b(0) {}

    /**
    * @brief Constructeur permettant d'initialiser les composantes RGB avec des valeurs spécifiques.
    * @param nr Valeur de la composante rouge.
    * @param ng Valeur de la composante verte.
    * @param nb Valeur de la composante bleue.
    */
    Pixel(unsigned char nr, unsigned char ng, unsigned char nb) : r(nr), g(ng), b(nb) {}
};

#endif // _PIXEL_H

