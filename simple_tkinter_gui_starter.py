import tkinter as tk
from tkinter import ttk, messagebox
from Main import build_ir_system

class PubMedGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PubMed IR System")
        self.geometry("750x550")  # ← زودنا الارتفاع شوية عشان الـ radio buttons

        self.ir_system, self.processor, self.original_documents = build_ir_system()
        self.create_widgets()

    def create_widgets(self):
        # App Title
        title = ttk.Label(self, text="PubMed Search Engine", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Query Input
        lbl_query = ttk.Label(self, text="Enter your query:")
        lbl_query.pack(anchor="w", padx=20)

        self.query_entry = ttk.Entry(self, width=80)
        self.query_entry.pack(padx=20, pady=5)

        # ✅ التعديل الجديد: Search Mode (ضيفيه هنا تحت الـ query entry)
        mode_frame = ttk.Frame(self)
        mode_frame.pack(pady=5)

        ttk.Label(mode_frame, text="Search Mode:").pack(side=tk.LEFT, padx=5)
        self.search_mode = tk.StringVar(value="Vector")
        ttk.Radiobutton(mode_frame, text="Vector (Ranked)", variable=self.search_mode, value="Vector").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Boolean AND", variable=self.search_mode, value="AND").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Boolean OR", variable=self.search_mode, value="OR").pack(side=tk.LEFT)

        # Search Button
        btn_search = ttk.Button(self, text="Search", command=self.search)
        btn_search.pack(pady=10)

        # Results Frame with Scrollbar
        results_frame = ttk.Frame(self)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self.results_box = tk.Text(results_frame, wrap=tk.WORD)
        self.results_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_box.config(yscrollcommand=scrollbar.set)

    # ✅ الـ search method اتغيرت كلها
    def search(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query")
            return

        self.results_box.delete("1.0", tk.END)
        mode = self.search_mode.get()  # ← بياخد Vector أو AND أو OR

        if mode == "Vector":
            results = self.ir_system.search(query, self.processor)[:5]
            if not results:
                self.results_box.insert(tk.END, "No results found.\n")
                return
            for idx, (pmid, score) in enumerate(results, start=1):
                doc = self.original_documents[pmid]
                snippet = doc['abstract'][:200] + "..." if len(doc['abstract']) > 200 else doc['abstract']
                self.results_box.insert(
                    tk.END,
                    f"{idx}. PMID: {pmid} | Score: {score:.4f}\nTitle: {doc['title']}\nAbstract: {snippet}\n{'-'*70}\n"
                )
        else:
            # Boolean AND أو OR
            pmids = self.ir_system.boolean_search(query, self.processor, mode=mode)[:5]
            if not pmids:
                self.results_box.insert(tk.END, "No results found.\n")
                return
            for idx, pmid in enumerate(pmids, start=1):
                doc = self.original_documents.get(pmid, {})
                snippet = doc.get('abstract', '')[:200] + "..."
                self.results_box.insert(
                    tk.END,
                    f"{idx}. PMID: {pmid}\nTitle: {doc.get('title','N/A')}\nAbstract: {snippet}\n{'-'*70}\n"
                )

if __name__ == "__main__":
    app = PubMedGUI()
    app.mainloop()