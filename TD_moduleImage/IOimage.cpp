
void Image::sauver(const string &filename) const
{
    ofstream fichier(filename.c_str());
    assert(fichier.is_open());
    fichier << "P3" << endl;
    fichier << dimx << " " << dimy << endl;
    fichier << "255" << endl;
    for (unsigned int y = 0; y < dimy; ++y)
        for (unsigned int x = 0; x < dimx; ++x)
        {
            Pixel &pix = getPix(x++, y);
            fichier << +pix.r << " " << +pix.g << " " << +pix.b << " ";
        }
    cout << "Sauvegarde de l'image " << filename << " ... OK\n";
    fichier.close();
}

void Image::ouvrir(const string &filename)
{
    ifstream fichier(filename.c_str());
    assert(fichier.is_open());
    char r, g, b;
    string mot;
    dimx = dimy = 0;
    fichier >> mot >> dimx >> dimy >> mot;
    assert(dimx > 0 && dimy > 0);
    if (tab != nullptr)
        delete[] tab;
    tab = new Pixel[dimx * dimy];
    for (unsigned int y = 0; y < dimy; ++y)
        for (unsigned int x = 0; x < dimx; ++x)
        {
            fichier >> r >> b >> g;
            getPix(x, y).r = r;
            getPix(x, y).g = g;
            getPix(x, y).b = b;
        }
    fichier.close();
    cout << "Lecture de l'image " << filename << " ... OK\n";
}

void Image::afficherConsole()
{
    cout << dimx << " " << dimy << endl;
    for (unsigned int y = 0; y < dimy; ++y)
    {
        for (unsigned int x = 0; x < dimx; ++x)
        {
            Pixel &pix = getPix(x, y);
            cout << +pix.r << " " << +pix.g << " " << +pix.b << " ";
        }
        cout << endl;
    }
}
