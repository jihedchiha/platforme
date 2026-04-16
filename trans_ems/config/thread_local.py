import threading

# _thread_locals est un objet spécial de Python qui isole les variables par thread.
# Chaque requête HTTP tourne dans son propre thread, donc salle_id sera unique par utilisateur.
_thread_locals = threading.local()

def set_current_salle_id(salle_id):
    """Stocke le salle_id de la requête en cours dans la mémoire du thread."""
    setattr(_thread_locals, 'salle_id', salle_id)

def get_current_salle_id():
    """Récupère le salle_id stocké pour le thread actuel."""
    return getattr(_thread_locals, 'salle_id', None)

def clear_current_salle_id():
    """Supprime le salle_id du thread actuel (pour éviter les fuites de données)."""
    if hasattr(_thread_locals, 'salle_id'):
        delattr(_thread_locals, 'salle_id')
