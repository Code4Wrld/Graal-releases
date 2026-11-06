# Graal – IPTV Player

*Votre quête s'arrête ici.*

Les versions publiées de Graal – IPTV Player, pour Fire TV, Android TV, téléphones et tablettes Android, Windows et Mac. Les applis installées consultent ce dépôt pour se mettre à jour toutes seules.

## Télécharger

Dans [Releases](https://github.com/Code4Wrld/Graal-releases/releases/latest) :

| Appareil | Fichier |
|---|---|
| Fire TV, Android TV, téléphone, tablette | `Graal-x.y.z.apk` |
| PC Windows | `Graal-x.y.z-Windows.zip` (décompresser, lancer `Graal.exe`) |
| Mac (puce Apple) | `Graal-x.y.z-macOS-arm64.dmg` |
| Mac (Intel) | `Graal-x.y.z-macOS-x64.dmg` |

## Contenu du dépôt

- `.github/workflows/graal.yml` : construit et publie chaque version (APK, Windows, Mac).
- `.github/workflows/joueurs.yml` : met à jour les photos des joueurs des pages Sports après chaque mercato.
- `data/joueurs/` : ces photos, par championnat (servies par GitHub Pages).
- `admin/` : la console des journaux de diagnostic.

## Sécurité et confidentialité

- **Votre abonnement IPTV reste sur votre appareil** : serveur, identifiant et mot de passe ne sont jamais envoyés à Graal.
- **Rien en clair sur le serveur Graal** : adresse e-mail du compte Premium, code et nom de chaque appareil sont chiffrés en **AES-256-GCM** (un vecteur aléatoire par donnée) et retrouvés par une empreinte **HMAC-SHA256 poivrée** (clé secrète gardée hors de la base) ; le code de vérification reçu par e-mail n'est stocké que sous forme d'empreinte.
- **Synchronisation chiffrée sur la box** avant l'envoi : le serveur ne voit ni les titres regardés ni l'abonnement.
- **Clés hors de la base**, tables fermées à tout accès direct, console d'administration protégée par mot de passe et double authentification, tout en HTTPS.
- **Ménage automatique** : les journaux de diagnostic sont effacés au bout de 7 jours.
- **Paiements** sur la page sécurisée du prestataire de paiement : Graal ne voit jamais votre carte.

## Signaler un problème ou demander un retrait

Ouvrez une [issue](https://github.com/Code4Wrld/Graal-releases/issues). Les logos, noms et photos affichés dans l'appli appartiennent à leurs titulaires ; une demande de retrait est traitée rapidement.
