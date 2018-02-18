# 08/02/2018 Solène Duchamp - Charles Jacquet

from programme_1 import *
from programme_2 import *
from programme_3 import *


# Module avec pour seul but de lancer la vérification des trois programmes
# Les 3 fonctions test_programme_X acceptent des jeux de test en entrée pour 
# faire des tests personnalisés


if __name__ == "__main__":
    presentation_1()
    test_programme_1()

    presentation_2()
    test_programme_2()

    presentation_3()
    test_programme_3()


