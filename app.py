import streamlit as st
from supabase import create_client
from cryptography.fernet import Fernet
import hashlib
import base64
import time

# --- CONFIGURATION TTU-MC3 ---
def generate_ttu_k_factor(shared_code):
    """Génère la constante de courbure K pour stabiliser le tunnel"""
    # On utilise un sel pour éviter les attaques par dictionnaire
    ttu_salt = "K_FACTOR_TTU_MC3_GABON_2026"
    combined = shared_code + ttu_salt
    k_hash = hashlib.sha256(combined.encode()).digest()
    return base64.urlsafe_b64encode(k_hash)

# --- INTERFACE DE MESSAGERIE ---
def messages_page():
    st.title("🌌 Tunnel de Messagerie TTU-MC³")
    st.caption("Système de communication par stabilisation d'états fantômes")

    # 1. Contrôle de la Courbure K (Le Code Partagé)
    with st.sidebar:
        st.header("⚙️ Paramètres du Tunnel")
        shared_k = st.text_input("Code de Courbure K", type="password", help="Code secret partagé avec votre interlocuteur")
        
        if shared_k:
            st.success("✅ État de phase : Cohérent (ΦC)")
            k_key = generate_ttu_k_factor(shared_k)
            cipher = Fernet(k_key)
        else:
            st.warning("⚠️ État de phase : Dissipatif (ΦD)")
            st.info("Le tunnel est en 'État Fantôme'. Entrez un code K pour voir les messages.")
            st.stop()

    # 2. Sélecteur de Contact (Simulation pour l'exemple)
    contact = st.selectbox("Vers quel attracteur (contact) ?", ["Inconnu_01", "Inconnu_02", "Groupe TTU"])

    # 3. Zone d'affichage des messages
    st.markdown("---")
    
    # Simulation de messages récupérés (Normalement depuis Supabase)
    # Les messages arrivent sous forme d'états fantômes (chiffrés)
    ghost_messages = [
        {"sender": "Inconnu_01", "content": "gAAAAABl...", "time": "12:00"}, # Ex: gAAAAABl...
    ]

    for msg in ghost_messages:
        with st.chat_message("assistant"):
            try:
                # Tentative de stabilisation (Déchiffrement)
                decrypted_content = cipher.decrypt(msg["content"].encode()).decode()
                st.write(f"**{msg['sender']}** : {decrypted_content}")
                st.caption(f"Stabilisé à {msg['time']}")
            except:
                # Échec de la courbure : le message reste fantôme
                st.error("💠 Instabilité Δk/k : Message bloqué en état fantôme (Code K invalide)")

    # 4. Projection d'un nouveau message
    st.markdown("---")
    new_msg = st.chat_input("Projeter un message dans le tunnel...")
    
    if new_msg:
        # Chiffrement par courbure K avant envoi
        encrypted_msg = cipher.encrypt(new_msg.encode()).decode()
        
        # Logique d'envoi Supabase
        # supabase.table("messages").insert({"content": encrypted_msg, "sender": st.session_state.user_id}).execute()
        
        st.success("Message dissipé dans le tunnel et projeté vers le destinataire.")
        st.info(f"Aperçu de l'état fantôme envoyé : `{encrypted_msg[:20]}...`")

# Lancement de l'app
if __name__ == "__main__":
    messages_page()
