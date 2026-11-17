from db import connexion, inserer, maintenant

# Un seuil par grandeur : (minimum, maximum). None = pas de limite.
SEUILS = {
    "temperature": (5, 40),     # °C
    "humidite":    (20, 80),    # %
    "eau":         (None, 0),   # 1 = eau detectee -> alerte
    "bruit":       (None, 0),   # 1 = bruit detecte -> alerte
}


def init_alertes():
    conn = connexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capteur TEXT NOT NULL,
            type_mesure TEXT NOT NULL,
            valeur REAL NOT NULL,
            message TEXT NOT NULL,
            horodatage TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_alertes_heure ON alertes (horodatage)"
    )
    conn.commit()
    conn.close()


def verifier(capteur, type_mesure, valeur):
    """Retourne un message si la valeur depasse le seuil, sinon None."""
    if type_mesure not in SEUILS:
        return None
    mini, maxi = SEUILS[type_mesure]
    if mini is not None and valeur < mini:
        return f"{type_mesure} trop basse : {valeur} (min {mini})"
    if maxi is not None and valeur > maxi:
        return f"{type_mesure} trop haute : {valeur} (max {maxi})"
    return None


def enregistrer(capteur, type_mesure, valeur, unite):
    """Stocke la mesure ET cree une alerte si besoin."""
    inserer(capteur, type_mesure, valeur, unite)
    message = verifier(capteur, type_mesure, valeur)
    if message:
        conn = connexion()
        conn.execute(
            "INSERT INTO alertes (capteur, type_mesure, valeur, message, horodatage) "
            "VALUES (?, ?, ?, ?, ?)",
            (capteur, type_mesure, valeur, message, maintenant()),
        )
        conn.commit()
        conn.close()
        print("ALERTE :", message)
    return message


if __name__ == "__main__":
    init_alertes()
    print(verifier("capteur1", "temperature", 45))  # doit afficher une alerte
    print(verifier("capteur1", "temperature", 22))  # doit afficher None