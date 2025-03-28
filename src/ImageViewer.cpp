#include "ImageViewer.h"
#include <iostream>
#include <SDL2/SDL.h>

/** 
* @file ImageViewer.cpp
* @brief fichier .cpp de la classe "ImageViewer"
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

/**
 * @brief Constructeur de la classe ImageViewer.
 * Initialise SDL et crée une fenêtre et un renderer.
 */
ImageViewer::ImageViewer() {
    SDL_Init(SDL_INIT_VIDEO); // Initialisation de SDL
    window = SDL_CreateWindow("Image Viewer", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 512, 512, SDL_WINDOW_SHOWN); // Création de la fenêtre SDL
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED); // Création du renderer SDL
}

/**
 * @brief Destructeur de la classe ImageViewer.
 * Libère la mémoire des ressources SDL.
 */
ImageViewer::~ImageViewer() {
    SDL_DestroyTexture(texture); // Libération de la texture SDL
    SDL_DestroyRenderer(renderer); // Libération du renderer SDL
    SDL_DestroyWindow(window); // Libération de la fenêtre SDL
    SDL_Quit(); // Fermeture de SDL
}

/**
 * @brief Affiche une image sur la fenêtre SDL.
 * @param im L'image à afficher.
 */
void ImageViewer::afficher(const Image& im) {
    surface = SDL_CreateRGBSurfaceFrom((void*)im.getTab(), im.getDimX(), im.getDimY(), 24, im.getDimX() * 3,255, 255, 255, 0); // Conversion image en une surface SDL 

    // Initialisation de la zone affichée avec la taille de l'image entière
    zoneAffichee.x = 0;
    zoneAffichee.y = 0;
    zoneAffichee.w = im.getDimX(); // Largeur de l'image
    zoneAffichee.h = im.getDimY(); // Hauteur de l'image

    // Vérification surface
    if (surface == nullptr) {
        // Gestion de l'erreur 
        return;
    }

    // Création de la texture SDL grace à la surface
    texture = SDL_CreateTextureFromSurface(renderer, surface);
    
    // Vérification texture
    if (texture == nullptr) {
        // Gestion de l'erreur 
        SDL_FreeSurface(surface);
        return;
    }

    // Nettoyage du renderer
    SDL_RenderClear(renderer);

    // Copie de la texture sur le renderer
    SDL_RenderCopy(renderer, texture, NULL, NULL);

    // Affichage du renderer
    SDL_RenderPresent(renderer);

    // Boucle pour gérer les events
    bool running = true;
    SDL_Event event;
    bool sizeChanged = false; // Indique si la taille de la zone affichée a été modifiée

    while (running) {
        // Traitement des events
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            } else if (event.type == SDL_KEYDOWN) {
                // switch pour les touches du clavier
                switch (event.key.keysym.sym) {
                    case SDLK_ESCAPE:
                        running = false;
                        break;
                    case SDLK_t:
                        // Zoom avant
                        // Augmenter la taille de la zone affichée
                        zoneAffichee.w += 10;
                        zoneAffichee.h += 10;
                        sizeChanged = true; // Indique que la taille a été modifiée
                        break;
                    case SDLK_g:
                        // Zoom arrière
                        // Diminuer la taille de la zone affichée
                        zoneAffichee.w -= 10;
                        zoneAffichee.h -= 10;
                        sizeChanged = true; // Indique que la taille a été modifiée
                        break;
                    default:
                        break;
                }
            }
        }
    
        if (sizeChanged) {
            SDL_RenderClear(renderer);
            SDL_RenderCopy(renderer, texture, &zoneAffichee, NULL);
            SDL_RenderPresent(renderer);
            sizeChanged = false; // Réinitialise la variable après le rendu
        }

        SDL_Delay(10); // Ajoute une pause de 10 millisecondes pour libérer le processeur
    }

    SDL_FreeSurface(surface);

}
