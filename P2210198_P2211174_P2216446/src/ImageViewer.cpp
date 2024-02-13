#include "ImageViewer.h"
#include <iostream>
#include <SDL2/SDL.h>

ImageViewer::ImageViewer() { // Définition du constructeur
    SDL_Init(SDL_INIT_VIDEO); // Initialisation de SDL
    window = SDL_CreateWindow("Image Viewer", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 200, 200, SDL_WINDOW_SHOWN); // Création de la fenêtre SDL
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED); // Création du renderer SDL
}

ImageViewer::~ImageViewer() { // Définition du destructeur
    SDL_DestroyTexture(texture); // Libération de la texture SDL
    SDL_DestroyRenderer(renderer); // Libération du renderer SDL
    SDL_DestroyWindow(window); // Libération de la fenêtre SDL
    SDL_Quit(); // Fermeture de SDL
}

void ImageViewer::afficher(const Image& im) {
    surface = SDL_CreateRGBSurfaceFrom((void*)im.getTab(), im.getDimX(), im.getDimY(), 24, im.getDimX() * 3, 0, 0, 0, 0); // Conversion image en une surface SDL

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
                        // ZOOM AVANT à implémenter
                        break;
                    case SDLK_g:
                        // ZOOM ARRIERE à implémenter
                        break;
                    default:
                        break;
                }
            }
        }
    }

    // Libération de la texture et de la surface!
    SDL_DestroyTexture(texture);
    SDL_FreeSurface(surface);
}
