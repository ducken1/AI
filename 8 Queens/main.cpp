#include <iostream>
#include <math.h>
#include <time.h>
#include <vector>
#include <algorithm>

using namespace std;

void matrika(vector<int> kraljice) {
    int N = kraljice.size();

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (kraljice[j] == i) { //npr. kraljice[0] = 2... v 1. stolpcu in 3. vrstici
                cout << "Q ";   // j = stolpec,, i = vrstica - če je ujemanje je tam kraljica
            }
            else {
                cout << "- ";
            }
        }
        cout << endl;
    }
}

int hevristika(vector<int>kraljice, int N) {
    int horizontalna_hevristika = 0;

    for (int i = 0; i < N; i++) {
        for (int j = i + 1; j < N; j++) { // i in j predstavljata stolpce.. kraljica[i ali j] pa vrstico
            if (kraljice[i] == kraljice[j]) {//npr. kraljice[0] je enaka kraljice[1] in kraljice[3] .. hev = 2
                horizontalna_hevristika++; //  kraljica[1] je enaka kraljice[3] .. hev = 1 ... 2 + 1 = 3
            }                           // 2 kraljici v isti vrsti = 1,, 3 kraljice v isti vrsti = 3
        }
    }

    int diagonalna_hevristika = 0;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (i != j) { // ni isti stolpec
                if (abs(kraljice[i] - kraljice[j]) - abs(i - j) == 0) { // ce sta na isti diagonali preverimo z razliko
                    diagonalna_hevristika++;                // med vrsticami ter stolpci teh dveh kraljic
                }        //npr. kraljice[i] .. 2 vrstica - kraljice[j] ... 4 vrstica = 2  ABS
            }            // i = 0 (1. stolpec) - j = 2 (3.stolpec) = 2 ABS
        }               // 2-2 = 0... sta v diagonali
    }

    int koncna_hevristika = horizontalna_hevristika + (diagonalna_hevristika/2);
    return koncna_hevristika;

}



int main()
{
    srand(time(0));

    int N;
    cout << "Vnesite zeljeno velikost sahovnice med 4 in 12: ";
    cin >> N;
    if (N < 4 or N > 12)
        cout << "Napacna velikost sahovnice" << endl;
    cout << endl;

    vector<int> kraljice; // vector uporabljen zaradi dinamične velikosti matrike,, v arrayu bi bilo malenkost tezje int "*array{ new int[length]{} };"
    for (int i = 0; i < N; i++) {
        kraljice.push_back(0); // napolni vse kraljice z 0.. kot np.zeros v pythonu
    }

    for (int i = 0; i < N; i++) {
        kraljice[i] = rand() % N; //generira kraljico v naključni vrstici
    }

    int choice;

    cout << "Izberite zeljen algoritem: " << endl;
    cout << "1) Vzpenjanje na hrib (Hill Climbing) " << endl;
    cout << "2) Simulirano ohlajanje (Simulated annealing) " << endl;
    cout << "Izbira: ";

    cin >> choice;

    switch(choice) {

        case 1: {

            matrika(kraljice);
            vector<int> kraljice2; // nov vektor kraljic, kateri bo uporabljen zacas algoritma

            for (int i = 0; i < kraljice.size(); i++)
                kraljice2.push_back(kraljice[i]); // prekopiram vrednosti iz kraljice v kraljice2


            cout << "Zacetna hevristika: " << hevristika(kraljice, N) << endl;

            int dovoljeni_premiki; //50 za šahovnice do 5x5 in vrednosti 150 ali več za šahovnice večje od 5x5.
            cout << "Vnesite stevilo dovoljenih premikov: ";
            cin >> dovoljeni_premiki;

            int rnd_vrstica;
            int rnd_stolpec;

            do  {
                    int zacetna_hevristika = hevristika(kraljice, N);
                    for (int i = 0; i < dovoljeni_premiki; i++) {

                        rnd_stolpec = rand() % N;
                        rnd_vrstica = rand() % N;

                        if(kraljice2[rnd_stolpec] == rnd_vrstica) // ce je kraljica v isti vrstici kot nam da rnd vrstico
                            kraljice2[rnd_stolpec]--; // jo pomaknemo navzgor..
                        else
                            kraljice2[rnd_stolpec] = rnd_vrstica; //drugace ji podamo vrednost random vrstice

                        if (kraljice2[rnd_stolpec] < 0) //loop okoli.. ce bi slucajno sla ven iz polja gre na konec
                            kraljice2[rnd_stolpec] = N-1;

                        if (hevristika(kraljice2, N) < hevristika(kraljice, N)) // primerjamo hevristiko nove matrike s prejsno
                            kraljice = kraljice2;  //in ce je manjsa.. jo shranimo v original
                    }
                    int koncna_hevristika = hevristika(kraljice, N);
                    if (koncna_hevristika >= zacetna_hevristika) {
                        break;
                    }
                } while (true);

            matrika(kraljice);
            cout <<"Koncna hevristika: " << hevristika(kraljice, N);
            break;
        }

        case 2: {
            matrika(kraljice);

            cout << "Zacetna hevristika: " << hevristika(kraljice, N) << endl;
            cout << "Vnesite zeljeno zacetno temperaturo: ";
            int temperatura;
            cin >> temperatura;

            cout << "Vnesite spremembo temperature (Priporoceno 1): ";
            int sprememba;
            cin >> sprememba;

            vector<int> kraljice2; // nov vektor kraljic, kateri bo uporabljen zacas algoritma

            for (int i = 0; i < kraljice.size(); i++) {
                kraljice2.push_back(kraljice[i]); // prekopiram vrednosti iz kraljice v kraljice2
            }

            int rnd_vrstica;
            int rnd_stolpec;
            do {

                int zacetna_hevristika = hevristika(kraljice, N);

                if (temperatura == 0) {
                    cout << "Zacetna temperature ne sme biti 0" <<endl;
                    break;
                }

                rnd_stolpec = rand() % N;
                rnd_vrstica = rand() % N;

                if(kraljice2[rnd_stolpec] == rnd_vrstica) // ce je kraljica v isti vrstici kot nam da rnd vrstico
                    kraljice2[rnd_stolpec]--; // jo pomaknemo navzgor..
                else
                    kraljice2[rnd_stolpec] = rnd_vrstica; //drugace ji podamo vrednost random vrstice

                if (kraljice2[rnd_stolpec] < 0) //loop okoli.. ce bi slucajno sla ven iz polja gre na konec
                    kraljice2[rnd_stolpec] = N-1;

                int koncna_hevristika = hevristika(kraljice2, N);

                int razlika_hevristik = abs(koncna_hevristika - zacetna_hevristika); //Sprememba hevristik stanj S in X

                if (razlika_hevristik > 0) // ce je vecja od 0,, izvedemo premik matrike kraljice2 v kraljice
                    kraljice = kraljice2;
                else {
                    double eksponent = (double) razlika_hevristik / (double) temperatura;
                    double izracun_eksponenta = 1/exp(eksponent);

                    transform(kraljice2.begin(), kraljice2.end(), kraljice2.begin(), [izracun_eksponenta](int &c){return c * izracun_eksponenta;});
                    kraljice = kraljice2;

                }

                temperatura -= sprememba;
            } while(true);

            matrika(kraljice);
            cout <<"Koncna hevristika: " << hevristika(kraljice, N);
            break;
        }


        default:
            cout << "Vnesli ste napacno izbiro. Izhod iz programa!" << endl << endl;
    }
    return 0;
}