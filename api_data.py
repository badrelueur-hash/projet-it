"""Fonctions pour P4 (site Flask). Tout est retourne en dictionnaires / listes JSON."""
from datetime import datetime, timedelta
from db import connexion

PERIODES = {
    "heure":   timedelta(hours=1),
    "jour":    timedelta(days=1),
    "semaine": timedelta(weeks=1),
}


def _dict(ligne):
    return {
        "capteur": ligne[0],
        "type": ligne[1],
        "valeur": ligne[2],
        "unite": ligne[3],
        "horodatage": ligne[4],
    }


def derniere_valeur(type_mesure):
    conn = connexion()
    ligne = conn.execute(
        "SELECT capteur, type_mesure, valeur, unite, horodatage FROM mesures "
        "WHERE type_mesure = ? ORDER BY id DESC LIMIT 1",
        (type_mesure,),
    ).fetchone()
    conn.close()
    return _dict(ligne) if ligne else None


def historique(type_mesure, periode="heure"):
    """periode : 'heure', 'jour' ou 'semaine'."""
    debut = (datetime.now() - PERIODES[periode]).isoformat(timespec="seconds")
    conn = connexion()
    lignes = conn.execute(
        "SELECT capteur, type_mesure, valeur, unite, horodatage FROM mesures "
        "WHERE type_mesure = ? AND horodatage >= ? ORDER BY horodatage",
        (type_mesure, debut),
    ).fetchall()
    conn.close()
    return [_dict(l) for l in lignes]


def resume(type_mesure, periode="jour"):
    """Pour la carte d'un capteur : valeur actuelle, min, max."""
    debut = (datetime.now() - PERIODES[periode]).isoformat(timespec="seconds")
    conn = connexion()
    mini, maxi = conn.execute(
        "SELECT MIN(valeur), MAX(valeur) FROM mesures "
        "WHERE type_mesure = ? AND horodatage >= ?",
        (type_mesure, debut),
    ).fetchone()
    conn.close()
    actuelle = derniere_valeur(type_mesure)
    return {
        "type": type_mesure,
        "actuelle": actuelle["valeur"] if actuelle else None,
        "unite": actuelle["unite"] if actuelle else None,
        "min": mini,
        "max": maxi,
    }


def alertes_recentes(n=20):
    conn = connexion()
    lignes = conn.execute(
        "SELECT capteur, type_mesure, valeur, message, horodatage "
        "FROM alertes ORDER BY id DESC LIMIT ?",
        (n,),
    ).fetchall()
    conn.close()
    return [
        {"capteur": l[0], "type": l[1], "valeur": l[2],
         "message": l[3], "horodatage": l[4]}
        for l in lignes
    ]


if __name__ == "__main__":
    import json
    print(json.dumps(resume("temperature"), indent=2))
    print(json.dumps(historique("temperature", "heure")[:3], indent=2))