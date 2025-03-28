#ifndef IMAGEVIEWER_H
#define IMAGEVIEWER_H

#include <SDL2/SDL.h>
#include "Image.h"

/** 
* @file ImageViewer.h
* @brief fichier .h de la classe "ImageViewer"
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

class ImageViewer {
private:
    SDL_Window* window; // Pointeur vers la fenêtre SDL
    SDL_Renderer* renderer; // Pointeur vers le renderer SDL
    SDL_Texture* texture; // Pointeur vers la texture SDL
    SDL_Surface* surface; // Pointeur vers la surface SDL (pour stocker l'image)
    SDL_Rect zoneAffichee;

public:
    // Constructeur qui initialise tout SDL2 et crée la fenêtre et le renderer
    ImageViewer();
    // Détruit et ferme SDL2
    ~ImageViewer();
    // Affiche l’image passée en paramètre et permet le (dé)zoom
    void afficher(const Image& im);
};

#endif // IMAGEVIEWER_H
