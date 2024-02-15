#include <iostream>
#include <cassert>
#include "Image.h"
#include "Pixel.h"
#include <fstream>

/** 
* @file Image.cpp
* @brief Fichier source pour la classe "Image"
* Contient les définitions des membres de la classe Image.
* @author GOSSET Raphaël
* @author LANGE Théo
* @author LAASSIBI Yanis
* @date 2024
*/

/**
 * @brief Constructeur par défaut de la classe Image.
 * Initialise les dimensions à 0 et le tableau de pixels à nullptr.
 */
Image::Image(){
    tab = nullptr;
    dimx = 0; // Initialisation de dimx à 0
    dimy = 0; // Initialisation de dimy à 0
}

/**
 * @brief Constructeur avec dimensions de la classe Image.
 * @param dimensionX La largeur de l'image.
 * @param dimensionY La hauteur de l'image.
 * Initialise un tableau de dimensionX * dimensionY pixels avec une couleur par défaut.
 */
Image::Image(int dimensionX, int dimensionY){
    dimx = dimensionX; // Affectation de dimensionX à dimx
    dimy = dimensionY; // Affectation de dimensionY à dimy
    tab = new Pixel[dimx * dimy]; // Allocation dynamique d'un tableau de pixels
    effacer(Pixel()); // Effacement du tableau avec la couleur par défaut
}

/**
 * @brief Destructeur de la classe Image.
 * Désalloue la mémoire occupée par le tableau de pixels et réinitialise les dimensions.
 */
Image::~Image(){
    if(tab != nullptr) delete[] tab; // Désallocation du tableau de pixels
    dimx = 0; // Réinitialisation de dimx à 0
    dimy = 0; // Réinitialisation de dimy à 0
}

/**
 * @brief Récupère le pixel aux coordonnées spécifiées.
 * @param x Coordonnée x du pixel.
 * @param y Coordonnée y du pixel.
 * @return Le pixel aux coordonnées spécifiées, ou un pixel par défaut si les coordonnées sont invalides.
 */
Pixel Image::getPix(int x, int y)const{
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) return tab[y*dimx+x]; // Vérification des limites et retour du pixel correspondant
    return Pixel(); // Retourne un Pixel par défaut si les paramètres ne sont pas valides
}

/**
 * @brief Récupère un pointeur vers le pixel aux coordonnées spécifiées.
 * @param x Coordonnée x du pixel.
 * @param y Coordonnée y du pixel.
 * @return Un pointeur vers le pixel aux coordonnées spécifiées, ou nullptr si les coordonnées sont invalides.
 */
Pixel * Image::getPix(int x, int y){
    assert(x >= 0 && x < dimx && y >= 0 && y < dimy); // Vérification des limites
    return &tab[y*dimx+x]; // Retourne un pointeur vers le pixel correspondant
}

/**
 * @brief Modifie le pixel aux coordonnées spécifiées.
 * @param x Coordonnée x du pixel.
 * @param y Coordonnée y du pixel.
 * @param couleur La couleur à attribuer au pixel.
 */
void Image::setPix(int x, int y, Pixel couleur){
    if(x >= 0 && x < dimx && y >= 0 && y < dimy) tab[y*dimx+x] = couleur; // Vérification des limites et attribution de la couleur au pixel spécifié
}

/**
 * @brief Applique une couleur à tous les pixels compris entre les coordonnées spécifiées.
 * @param Xmin La coordonnée x minimale.
 * @param Xmax La coordonnée x maximale.
 * @param Ymin La coordonnée y minimale.
 * @param Ymax La coordonnée y maximale.
 * @param couleur La couleur à appliquer aux pixels.
 */
void Image::dessinerRectangle(int Xmin, int Xmax, int Ymin, int Ymax, Pixel couleur){
    for(int i = Xmin; i <= Xmax; i++ ){
        for(int j = Ymin; j <= Ymax; j++ ){
            setPix(i, j, couleur); // Dessine un rectangle en appliquant la couleur spécifiée à tous les pixels compris entre les coordonnées spécifiées
        }
    }
}

/**
 * @brief Applique une couleur à tous les pixels de l'image.
 * @param couleur La couleur à appliquer.
 */
void Image::effacer(Pixel couleur){
    dessinerRectangle(0, dimx, 0, dimy, couleur); // Efface l'image en dessinant un rectangle de la taille de l'image avec la couleur spécifiée
}

/**
 * @brief Méthode de test pour toutes les méthodes de la classe Image.
 * Teste les constructeurs, les méthodes de récupération et de modification de pixels, ainsi que les méthodes de dessin et d'effacement.
 */
void Image::testRegression() {
    using namespace std; // Utilisation de l'espace de noms standard

    Image testImageDefault; // Création d'une image par défaut
    assert(testImageDefault.dimx == 0 && testImageDefault.dimy == 0); // Vérification des dimensions de l'image par défaut
    cout << "Constructeur par défaut OK!" << endl; // Affichage d'un message indiquant que le constructeur par défaut fonctionne correctement

    Image imageTest(3, 4); // Création d'une nouvelle image avec des dimensions spécifiées
    assert(imageTest.dimx == 3 && imageTest.dimy == 4); // Vérification des dimensions de la nouvelle image
    cout << "Constructeur avec dimensions OK!" << endl; // Affichage d'un message indiquant que le constructeur avec dimensions fonctionne correctement

    Pixel* PixelPtr; // Déclaration d'un pointeur de Pixel

    imageTest.effacer(Pixel(255, 0, 0)); // Effacement de l'image avec une couleur spécifiée
    for (int i = 0; i < imageTest.dimx; ++i) {
        for (int j = 0; j < imageTest.dimy; ++j) {
            PixelPtr = imageTest.getPix(i, j); // Récupération du pixel à la position (i, j)
            assert(PixelPtr != nullptr); // Vérification que le pixel n'est pas nul
            Pixel Pixel = *PixelPtr; // Obtention de la valeur du pixel
            assert(Pixel.r == 255 && Pixel.g == 0 && Pixel.b == 0); // Vérification de la couleur du pixel
        }
    }
    cout << "Effacer OK!" << endl; // Affichage d'un message indiquant que la méthode d'effacement fonctionne correctement

    imageTest.dessinerRectangle(1, 2, 1, 2, Pixel(0, 255, 0)); // Dessin d'un rectangle sur l'image avec une couleur spécifiée
    Pixel* pixel1 = imageTest.getPix(1, 1); // Récupération du pixel à la position (1, 1)
    assert(pixel1 != nullptr); // Vérification que le pixel n'est pas nul
    assert(pixel1->r == 0 && pixel1->g == 255 && pixel1->b == 0); // Vérification de la couleur du pixel
    Pixel* pixel2 = imageTest.getPix(2, 2); // Récupération du pixel à la position (2, 2)
    assert(pixel2 != nullptr); // Vérification que le pixel n'est pas nul
    assert(pixel2->r == 255 && pixel2->g == 0 && pixel2->b == 0); // Vérification de la couleur du pixel
    cout << "DessinerRectangle OK!" << endl; // Affichage d'un message indiquant que la méthode de dessin de rectangle fonctionne correctement

    imageTest.setPix(1, 1, Pixel(0, 0, 255)); // Modification du pixel à la position (1, 1) avec une nouvelle couleur
    Pixel* modifiedPixelPtr = imageTest.getPix(1, 1); // Récupération du pixel modifié
    assert(modifiedPixelPtr != nullptr); // Vérification que le pixel n'est pas nul
    Pixel modifiedPixel = *modifiedPixelPtr; // Obtention de la valeur du pixel modifié
    assert(modifiedPixel.r == 0 && modifiedPixel.g == 0 && modifiedPixel.b == 255); // Vérification de la couleur du pixel
    cout << "GetPix et SetPix OK!" << endl; // Affichage d'un message indiquant que les méthodes de récupération et de modification de pixel fonctionnent correctement

    cout << "CA FONCTIONNE !!" << endl; // Affichage d'un message global indiquant que tous les tests ont réussi
}

/**
 * @brief Sauvegarde l'image au format PPM.
 * @param filename Le nom du fichier dans lequel sauvegarder l'image.
 * Écrit l'image dans un fichier au format PPM.
 */
void Image::sauver(const std::string &filename) const
{
    using namespace std; // Utilisation de l'espace de noms standard

    ofstream fichier(filename.c_str()); // Ouverture du fichier en écriture
    assert(fichier.is_open()); // Vérification que le fichier est ouvert avec succès
    fichier << "P3" << endl; // Écriture de l'en-tête du fichier PPM
    fichier << dimx << " " << dimy << endl; // Écriture des dimensions de l'image
    fichier << "255" << endl; // Écriture de la valeur maximale de couleur
    for (unsigned int y = 0; y < dimy; ++y) // Parcours des lignes de l'image
        for (unsigned int x = 0; x < dimx; ++x) // Parcours des colonnes de l'image
        {
            Pixel pix = getPix(x, y); // Obtention du pixel à la position (x, y)
            fichier << +pix.r << " " << +pix.g << " " << +pix.b << " "; // Écriture des valeurs R, G et B du pixel dans le fichier
            ++x; // Incrémentation de x
        }
    cout << "Sauvegarde de l'image " << filename << " ... OK\n"; // Affichage d'un message indiquant que la sauvegarde de l'image s'est déroulée avec succès
    fichier.close(); // Fermeture du fichier
}

/**
 * @brief Charge une image depuis un fichier au format PPM.
 * @param filename Le nom du fichier à charger.
 * Charge l'image à partir d'un fichier au format PPM.
 */
void Image::ouvrir(const std::string &filename)
{
    using namespace std;

    ifstream fichier(filename.c_str()); // Ouverture du fichier en lecture
    assert(fichier.is_open()); // Vérification que le fichier est ouvert avec succès
    int r, g, b; // Variables temporaires pour stocker les composantes RGB
    std::string mot; // Variable temporaire pour stocker les mots lus du fichier
    dimx = dimy = 0; // Réinitialisation des dimensions de l'image
    fichier >> mot >> dimx >> dimy >> mot; // Lecture de l'en-tête du fichier PPM et des dimensions de l'image
    assert(dimx >= 0 && dimy >= 0); // Vérification que les dimensions sont valides
    if (tab != nullptr)
        delete[] tab; // Libération de la mémoire si le tableau existe déjà
    tab = new Pixel[dimx * dimy]; // Allocation d'un nouveau tableau de pixels
    for (unsigned int y = 0; y < dimy; ++y) // Parcours des lignes de l'image
        for (unsigned int x = 0; x < dimx; ++x) // Parcours des colonnes de l'image
        {
            fichier >> r >> b >> g; // Lecture des composantes RGB du pixel
            getPix(x, y)->r = r; // Attribution de la composante R du pixel
            getPix(x, y)->g = g; // Attribution de la composante G du pixel
            getPix(x, y)->b = b; // Attribution de la composante B du pixel
        }
    fichier.close(); // Fermeture du fichier
    cout << "Lecture de l'image " << filename << " ... OK\n"; // Affichage d'un message indiquant que la lecture de l'image s'est déroulée avec succès
}

/**
 * @brief Affiche l'image dans la console.
 * Affiche les valeurs des pixels de l'image dans la console.
 */
void Image::afficherConsole()
{
    using namespace std;
    cout << dimx << " " << dimy << endl; // Affichage des dimensions de l'image
    for (unsigned int y = 0; y < dimy; ++y) // Parcours des lignes de l'image
    {
        for (unsigned int x = 0; x < dimx; ++x) // Parcours des colonnes de l'image
        {
            Pixel* pix = getPix(x, y); // Obtention du pixel à la position (x, y)
            cout << +pix->r << " " << +pix->g << " " << +pix->b << " "; // Affichage des valeurs R, G et B du pixel
        }
        cout << endl; // Saut de ligne à la fin de chaque ligne de pixels
    }
}
