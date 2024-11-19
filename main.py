import requests
import webbrowser
import customtkinter as ctk

class GitHubSearchTool:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("GitHub Search Tool")
        self.root.geometry("600x400")

        self.entry_label = ctk.CTkLabel(self.root, text="Entrez un mot-clé :")
        self.entry_label.pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.root, width=400)
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self.root, text="Rechercher", command=self.search_github)
        self.search_button.pack(pady=10)

        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def search_github(self):
        query = self.search_entry.get()
        if not query:
            return
        
        url = f"https://api.github.com/search/repositories?q={query}"
        headers = {"Accept": "application/vnd.github+json"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.display_results(data.get("items", []))
        else:
            self.display_error("Erreur lors de la recherche sur GitHub.")

    def display_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not results:
            ctk.CTkLabel(self.results_frame, text="Aucun résultat trouvé.").pack(pady=10)
            return

        for repo in results[:10]:
            name = repo["full_name"]
            html_url = repo["html_url"]
            link = ctk.CTkButton(self.results_frame, text=name, command=lambda url=html_url: webbrowser.open(url))
            link.pack(pady=5)

    def display_error(self, message):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text=message, text_color="red").pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GitHubSearchTool()
    app.run()
