# ![One AI of a Time](.github\assets\images\headers.webp)

Un script universel et modulaire permettant de créer facilement des modèles d'IA distillés (Textes, Images, Audios) à partir d'un simple objectif en langage naturel.

## 🎯 Objectif du Projet
Simplifier à l'extrême le processus de **Distillation de Modèles (Knowledge Distillation)** par la génération de données synthétiques. Que vous ayez un dataset complet, seulement quelques prompts, ou même *absolument rien* d'autre qu'une idée en tête, ce script orchestre tout le processus jusqu'à la préparation de l'entraînement.

## ✨ Fonctionnalités Prévues
- **Sélection Intelligente** : Si vous ne savez pas quel modèle utiliser, le script interroge un LLM puissant (via Hugging Face) pour vous recommander le meilleur couple "Professeur" (grand modèle) / "Élève" (petit modèle).
- **Génération Automatique de Données** : Création de prompts synthétiques et génération des réponses par le modèle Professeur.
- **Support Multi-Modalités** : Détection automatique de la modalité du modèle Professeur (Génération de Texte, Modèles de Raisonnement "Thinking", Text-to-Image, Text-to-Audio).
- **Prêt pour AutoTrain** : Formatage automatique des données générées et création de la commande exacte pour lancer l'entraînement sur Hugging Face AutoTrain (LLM ou Dreambooth).

## 🚀 Installation & Prérequis

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour la gestion des dépendances.

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-pseudo/One-AI-of-a-time.git
   cd One-AI-of-a-time
   ```

2. **Installer les dépendances via uv**
   ```bash
   uv add huggingface-hub prompt-toolkit datasets python-dotenv
   ```

3. **Configuration**
   Créez un fichier `.env` à la racine du projet et ajoutez votre token Hugging Face (nécessite les permissions *Read* et *Write* ainsi que *Make calls to Inference Providers*) :
   ```env
   HF_TOKEN=votre_token_huggingface
   ```

## 💻 Utilisation (À venir)

*(Le code est en cours de développement, étape par étape !)*

Une fois le point d'entrée principal configuré, vous pourrez lancer l'outil via :
```bash
uv run hello.py # (ou main.py selon votre initialisation)
```
Le script proposera une interface interactive dans le terminal si des arguments manquent.
