#ifndef _IMAGE_H
#define _IMAGE_H

#include "Pixel.h"
#include <string>

/** 
* @file Image.h
* @brief fichier .h de la classe "Image"
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

/**
 * @class Image
 * @brief Représente une image composée de pixels.
 */
class Image{
    
    private:
        Pixel* tab; /**< Tableau de pixels représentant l'image */
        int dimx, dimy; /**< Dimensions de l'image */

    public: 
        
        /**
         * @brief Constructeur par défaut.
         * Initialise les dimensions à 0.
         */
        Image();

        /**
         * @brief Constructeur avec dimensions.
         * @param dimensionX La largeur de l'image.
         * @param dimensionY La hauteur de l'image.
         * Initialise un tableau de dimensionX * dimensionY pixels.
         */
        Image(int dimensionX, int dimensionY);

        /**
         * @brief Destructeur par défaut.
         * Désalloue la mémoire du tableau de pixels et met les dimensions à 0.
         */
        ~Image();

        /**
         * @brief Récupère le pixel aux coordonnées spécifiées.
         * @param x La coordonnée en x du pixel.
         * @param y La coordonnée en y du pixel.
         * @return Le pixel aux coordonnées (x, y).
         */
        Pixel getPix(int x, int y) const;

        /**
         * @brief Récupère le pointeur du pixel aux coordonnées spécifiées.
         * @param x La coordonnée en x du pixel.
         * @param y La coordonnée en y du pixel.
         * @return Un pointeur vers le pixel aux coordonnées (x, y).
         */
        Pixel * getPix(int x, int y);

        /**
         * @brief Modifie le pixel aux coordonnées spécifiées par la couleur spécifiée.
         * @param x La coordonnée en x du pixel.
         * @param y La coordonnée en y du pixel.
         * @param couleur Le pixel représentant la couleur à assigner.
         */
        void setPix(int x, int y, Pixel couleur);

        /**
         * @brief Dessine un rectangle avec la couleur spécifiée aux coordonnées spécifiées.
         * @param Xmin La coordonnée minimale en x du rectangle.
         * @param Xmax La coordonnée maximale en x du rectangle.
         * @param Ymin La coordonnée minimale en y du rectangle.
         * @param Ymax La coordonnée maximale en y du rectangle.
         * @param couleur La couleur à appliquer au rectangle.
         */
        void dessinerRectangle(int Xmin, int Xmax, int Ymin, int Ymax, Pixel couleur);

        /**
         * @brief Efface l'image en appliquant la couleur spécifiée à tous les pixels.
         * @param couleur La couleur à appliquer pour effacer l'image.
         */
        void effacer(Pixel couleur);

        /**
         * @brief Effectue une série de tests pour vérifier le bon fonctionnement de la classe.
         */
        static void testRegression();

        /**
         * @brief Sauvegarde l'image au format PPM.
         * @param filename Le nom du fichier dans lequel sauvegarder l'image.
         * Écrit l'image dans un fichier au format PPM.
         */
        void sauver(const std::string &filename) const;

        /**
         * @brief Charge une image depuis un fichier au format PPM.
         * @param filename Le nom du fichier à charger.
         * Charge l'image à partir d'un fichier au format PPM.
         */
        void ouvrir(const std::string &filename);

        /**
         * @brief Affiche l'image dans la console.
         * Affiche les valeurs des pixels de l'image dans la console.
         */
        void afficherConsole();

        /**
         * @brief Obtient le tableau de pixels de l'image.
         * @return Un pointeur constant vers le tableau de pixels.
         */
        const Pixel* getTab() const { return tab; }

        /**
         * @brief Obtient la dimension en x de l'image.
         * @return La dimension en x de l'image.
         */
        int getDimX() const { return dimx; }

        /**
         * @brief Obtient la dimension en y de l'image.
         * @return La dimension en y de l'image.
         */
        int getDimY() const { return dimy; }
};

#endif
