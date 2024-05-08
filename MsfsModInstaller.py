import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import zipfile

def select_community_folder():
    # Affichage du message d'avertissement
    warning_message = ("Installer un mod peut s'avérer dangereux.\n"
                       "Avant de continuer, assurez-vous de :\n"
                       "1. Effectuer une sauvegarde de vos fichiers.\n"
                       "2. Télécharger le mod depuis une source vérifiée pour éviter les virus.")
    continue_install = messagebox.askokcancel("Attention", warning_message)
    if continue_install:
        # Si l'utilisateur choisit de continuer, ouvrir la fenêtre de sélection du dossier Community
        community_folder = filedialog.askdirectory(title="Sélectionner le dossier Community")
        community_folder_entry.delete(0, tk.END)
        community_folder_entry.insert(0, community_folder)

def select_mod_file():
    # Affichage de la fenêtre de sélection du fichier mod
    mod_file = filedialog.askopenfilename(title="Sélectionner le fichier du mod")
    mod_file_entry.delete(0, tk.END)
    mod_file_entry.insert(0, mod_file)

def install_mod():
    def install_thread():
        # Affichage du message "Veuillez patienter, installation en cours..."
        progress_label.config(text="Veuillez patienter, installation en cours...")

        community_folder = community_folder_entry.get()
        mod_file = mod_file_entry.get()

        if not community_folder or not mod_file:
            tk.messagebox.showerror("Erreur", "Veuillez sélectionner le dossier Community et le fichier du mod.")
            progress_label.config(text="")
            return

        try:
            with zipfile.ZipFile(mod_file, 'r') as zip_ref:
                zip_ref.extractall(community_folder)
            tk.messagebox.showinfo("Succès", "Le mod a été installé avec succès dans le dossier Community.")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'installation du mod : {str(e)}")
        finally:
            progress_label.config(text="")
            # Affichage du message d'information pour vérifier les dossiers extraits
            messagebox.showinfo("Information", "Si le mod ne fonctionne pas, veuillez vérifier les dossiers extraits.")

    threading.Thread(target=install_thread).start()

def open_recommended_sites():
    recommended_sites_window = tk.Toplevel(root)
    recommended_sites_window.title("Sites recommandés")
    tk.Button(recommended_sites_window, text="Flightsim", command=lambda: open_website("https://fr.flightsim.to")).pack()
    tk.Button(recommended_sites_window, text="Parallel42", command=lambda: open_website("https://parallel42.com")).pack()

def open_website(url):
    import webbrowser
    webbrowser.open_new(url)

def validate_installation():
    community_folder = community_folder_entry.get()
    mod_file = mod_file_entry.get()

    if not community_folder or not mod_file:
        install_button.config(state=tk.DISABLED)
    else:
        install_button.config(state=tk.NORMAL)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Installeur de mod pour MSFS")

# Bouton pour ouvrir les sites recommandés
tk.Button(root, text="Sites recommandés", command=open_recommended_sites).pack()

# Label et Entry pour sélectionner le dossier Community
tk.Label(root, text="Dossier Community :").pack()
community_folder_entry = tk.Entry(root, width=50)
community_folder_entry.pack()
tk.Button(root, text="Parcourir", command=select_community_folder).pack()

# Label et Entry pour sélectionner le fichier du mod
tk.Label(root, text="Fichier du mod :").pack()
mod_file_entry = tk.Entry(root, width=50)
mod_file_entry.pack()
tk.Button(root, text="Parcourir", command=select_mod_file).pack()

# Bouton pour installer le mod
install_button = tk.Button(root, text="Installer le mod", command=install_mod)
install_button.pack()

# Label pour afficher le message d'état de l'installation
progress_label = tk.Label(root, text="")
progress_label.pack()

# Vérification pour activer/désactiver le bouton "Installer le mod"
root.bind("<ButtonRelease-1>", lambda event: validate_installation())

root.mainloop()
