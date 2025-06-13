## Instruction de reprise

**Objectif :**

* Mettre en place un service HTTP (FastAPI + Docker) déployé via Coolify pour récupérer les sous-titres de vidéos YouTube en utilisant `youtube-transcript-api` et un proxy ScraperAPI.

**Ce qui a été fait :**

1. Création d'un microservice Python avec FastAPI (`app.py`) et Dockerfile de base.
2. Ajout d'un endpoint `/transcript` pour récupérer un transcript à partir d'une URL YouTube.
3. Packaging dans un conteneur Docker et déploiement initial via Coolify (Dockerfile deployé et service en ligne).
4. Configuration du proxy ScraperAPI :

   * Ajout de variable d'environnement `SCRAPERAPI_KEY` dans Coolify.
   * Mise à jour du code pour utiliser `proxy-server.scraperapi.com:8001`.
5. Installation des outils de diagnostic (`curl`, `ping`, `nslookup`) et des certificats racine (`ca-certificates`) dans l'image Docker.
6. Tentative de résolution DNS et tests avec `nslookup` et `curl` pour `proxy-server.scraperapi.com` (OK).
7. Ajustement du docker-compose pour inclure `dns:` et `expose:`.
8. Déploiement en mode Docker Compose dans Coolify.
9. Vérification de l'endpoint `/version` (fonctionnel).
10. Test de l'endpoint `/transcript` :

    * Erreur rencontrée : `SSLError(cert verify failed)` lors de la connexion à YouTube en HTTPS.

**Problème actuel :**

* Le service renvoie toujours une erreur 500 liée à un échec de vérification SSL (`certificate verify failed`) lors de la requête HTTPS vers `www.youtube.com`. Cela indique que l'image Docker ne parvient pas à valider les certificats SSL de YouTube, malgré l'installation de `ca-certificates`.

**Piste à suivre pour la résolution :**

1. Confirmer que les autorités de certification sont bien installées et mises à jour dans l'image Docker :

   * Vérifier la présence du fichier `/etc/ssl/certs/ca-certificates.crt`.
   * Exécuter `update-ca-certificates` dans le conteneur.
2. Ajouter, si nécessaire, l'installation de paquets supplémentaires :

   * `libssl-dev` ou `openssl` pour compléter la chaîne SSL.
3. Tester une requête HTTPS hors du proxy pour isoler le problème :

   ```bash
   curl -v https://www.youtube.com
   ```
4. Envisager d'utiliser `certifi` dans l'environnement Python :

   ```python
   import certifi, ssl
   ssl_context = ssl.create_default_context(cafile=certifi.where())
   # passer ce contexte à requests si utilisé directement
   ```
5. Si le problème persiste, basculer temporairement sur une requête HTTP via le proxy (si supporté) ou envisager un autre proxy HTTPS.
6. Documenter la configuration finale et valider localement dans un conteneur Docker avant redéploiement.

---

*Fin des instructions de reprise.*
