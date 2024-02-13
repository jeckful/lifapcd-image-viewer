#include "ImageViewer.h"
#include <iostream>

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

void ImageViewer::afficher(const Image& im) { // Définition de la méthode pour afficher l'image
    surface = SDL_CreateRGBSurfaceFrom((void*)im.getData(), im.getWidth(), im.getHeight(), 24, im.getWidth() * 3, 0, 0, 0, 0); // Conversion de l'image en une surface SDL

    texture = SDL_CreateTextureFromSurface(renderer, surface); // Création d'une texture SDL à partir de la surface

    SDL_RenderClear(renderer); // Nettoyage du renderer
    SDL_RenderCopy(renderer, texture, NULL, NULL); // Copie de la texture sur le renderer
    SDL_RenderPresent(renderer); // Affichage du renderer

    bool running = true; // Variable pour gérer l'exécution de la boucle d'événements
    SDL_Event event; // Déclaration d'une structure d'événement SDL
    while (running) { // Boucle principale pour gérer les événements
        while (SDL_PollEvent(&event)) { // Boucle pour traiter tous les événements en attente
            if (event.type == SDL_QUIT) { // Si l'utilisateur a demandé à quitter
                running = false; // Met fin à la boucle principale
            } else if (event.type == SDL_KEYDOWN) { // Si une touche du clavier a été enfoncée
                if (event.key.keysym.sym == SDLK_ESCAPE) { // Si la touche ESCAPE a été enfoncée
                    running = false; // Met fin à la boucle principale
                } else if (event.key.keysym.sym == SDLK_t) { // Si la touche T a été enfoncée
                    // Zoom avant (à implémenter)
                } else if (event.key.keysym.sym == SDLK_g) { // Si la touche G a été enfoncée
                    // Zoom arrière (à implémenter)
                }
            }
        }
    }

    SDL_FreeSurface(surface); // Libération de la surface SDL
}
