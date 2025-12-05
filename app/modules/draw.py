import matplotlib.pyplot as plt

def draw_loss(history):
    """
    Génère la figure des courbes de loss et val_loss
    depuis un historique d'entraînement Keras.

    Parameters
    ----------
    history : keras.callbacks.History
        L'historique retourné par model.fit()

    Returns
    -------
    fig : matplotlib.figure.Figure
        La figure contenant les courbes
    """

    # Préparation des données
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Courbe de loss (training)
    ax.plot(loss, label="Loss (Entraînement)", linewidth=2)

    # Courbe de validation si disponible
    if len(val_loss) > 0:
        ax.plot(val_loss, label="Loss (Validation)", linestyle="--", linewidth=2)

    # Mise en forme du graphique
    ax.set_title("Courbes de Loss et Validation Loss", fontsize=14)
    ax.set_xlabel("Epochs", fontsize=12)
    ax.set_ylabel("Loss", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    # Retourne la figure (pas de plt.show(), car incompatible Docker/API)
    return fig
