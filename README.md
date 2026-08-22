# hafididrissi.github.io

CV et portfolio de **Hafid Idrissi** — ingénieur logiciel Full-Stack & Cloud.
En ligne : **[hafididrissi.github.io](https://hafididrissi.github.io/)**

## Principe

Le contenu du site est dérivé d'un **CV master audité** (`cv_master_Hafid_IDRISSI.json`, hors dépôt) dont
chaque entrée porte un statut de validation. Règle de fond, reprise du CV master :

> Ne jamais inventer, extrapoler ou renforcer un fait absent du fichier source.
> Ne reprendre un chiffre que s'il figure explicitement dans un élément validé, et conserver son contexte.

Les expériences confrontées à une source primaire — dépôt de code, rapport de stage, contrat, diplôme —
portent la mention **Vérifié** sur le site, avec la source en infobulle.

Conformément aux règles du CV master, le site présente **une seule section « Expériences »** : les projets
personnels, entrepreneuriaux, académiques et de recherche y figurent avec un libellé de type explicite,
jamais présentés comme des emplois salariés.

## Structure

```
index.html            page unique — CSS et JS intégrés, aucune dépendance hors Google Fonts
data/cv-site.json     source de vérité du contenu (expériences, dépôts, filtres)
tools/build_site.py   rend data/cv-site.json en HTML statique dans index.html
assets/pdf/           CV téléchargeable
assets/*.svg          bannières animées du README de profil GitHub

github-profile-README.md          copie de travail du README de github.com/HafidIdrissi/HafidIdrissi
github-profile-snake-workflow.yml copie de travail de .github/workflows/snake.yml du même dépôt
```

## Modifier le contenu

1. Éditer `data/cv-site.json`.
2. Régénérer la page :

   ```bash
   python tools/build_site.py
   ```

3. Vérifier localement :

   ```bash
   python -m http.server 8777
   # http://127.0.0.1:8777/
   ```

Le rendu est **statique** : le contenu du CV est présent dans le HTML servi, donc lisible par les moteurs
de recherche, les outils de recrutement et à l'impression. Le JavaScript ne gère que le filtrage des
expériences, la bascule de thème, les révélations au scroll et le rafraîchissement facultatif du nombre
d'étoiles GitHub — la page reste complète sans lui.

## Choix techniques

- Page unique, sans framework ni build front-end : rien à installer pour servir le site.
- Thème clair/sombre suivant les préférences système, avec bascule mémorisée en `localStorage`.
- Filtres d'expériences par nature — sélection, entreprise, produits, recherche, académique.
- `prefers-reduced-motion` respecté ; repli `<noscript>` qui affiche tout le contenu.

## Licence

Le code de la page est réutilisable ; le contenu du CV, les documents et les visuels personnels ne le sont pas.
