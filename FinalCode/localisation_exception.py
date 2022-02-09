

class UntrustworthyLocalisationError(Exception):

    def __init__(self, erreur) -> None:
        super().__init__()
        self.erreur = erreur

    def __repr__(self):
        return "La localisation est de mauvaise facture, l'erreur est de " + str(self.erreur)


class MatchingError(Exception):
    def __repr__(self):
        return "Le matching n'a pas bien fonctionne"