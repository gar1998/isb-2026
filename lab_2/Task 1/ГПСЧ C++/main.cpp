#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main()
{
    srand(time(nullptr));

    ofstream outfile("C:\\Users\\Адель\\Desktop\\Лаб 2\\isb-2026\\lab_2\\ГПСЧ C++\\C++_sequence.txt");

    if (outfile.is_open())
    {
        for (int i = 0; i < 128; ++i)
        {
            outfile << (rand() % 2);
        }
        outfile.close();
        cout << "Последовательность C++ сохранена в sequence_cpp.txt" << "\n";
    }
    else
    {
        cerr << "Ошибка открытия файла!" << "\n";
    }

    return 0;
}