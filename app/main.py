from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from catalogo import CatalogError, CatalogoArticoli


APP_TITLE = "SST Manager - Anagrafica articoli"


class SSTManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x680")
        self.minsize(900, 520)

        self.catalogo: CatalogoArticoli | None = None
        self.file_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="File anagrafica articoli:").pack(side="left")
        ttk.Entry(top, textvariable=self.file_var).pack(
            side="left", fill="x", expand=True, padx=8
        )
        ttk.Button(top, text="Sfoglia...", command=self.choose_file).pack(side="left")
        ttk.Button(top, text="Carica / aggiorna", command=self.load_catalog).pack(
            side="left", padx=(8, 0)
        )

        search = ttk.Frame(self, padding=(12, 0, 12, 10))
        search.pack(fill="x")
        ttk.Label(search, text="Cerca per codice, descrizione o fornitore:").pack(
            side="left"
        )
        entry = ttk.Entry(search, textvariable=self.search_var)
        entry.pack(side="left", fill="x", expand=True, padx=8)
        entry.bind("<KeyRelease>", lambda _event: self.refresh_table())
        ttk.Button(search, text="Pulisci", command=self.clear_search).pack(side="left")

        table_frame = ttk.Frame(self, padding=(12, 0, 12, 8))
        table_frame.pack(fill="both", expand=True)

        columns = ("Codice_Articolo", "Descrizione", "desc_marca",
                   "Codice_Articolo_Fornitore", "prezzo_lordo", "prezzo_netto")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {
            "Codice_Articolo": ("Codice articolo", 170),
            "Descrizione": ("Descrizione", 390),
            "desc_marca": ("Marca", 130),
            "Codice_Articolo_Fornitore": ("Codice fornitore", 170),
            "prezzo_lordo": ("Prezzo lordo", 110),
            "prezzo_netto": ("Prezzo netto", 110),
        }
        for key, (label, width) in headings.items():
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, minwidth=70, anchor="w")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Seleziona il file Excel dell'anagrafica.")
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(
            fill="x", side="bottom"
        )

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Seleziona Anagrafica articoli DHS",
            filetypes=[("File Excel", "*.xlsx *.xlsm"), ("Tutti i file", "*.*")],
        )
        if path:
            self.file_var.set(path)
            self.load_catalog()

    def load_catalog(self):
        path = self.file_var.get().strip()
        if not path:
            self.choose_file()
            return
        try:
            self.catalogo = CatalogoArticoli(Path(path))
        except CatalogError as exc:
            messagebox.showerror("Errore anagrafica", str(exc))
            self.status_var.set("Caricamento non riuscito.")
            return
        self.refresh_table()
        self.status_var.set(
            f"Anagrafica caricata: {len(self.catalogo.rows)} articoli | {path}"
        )

    def clear_search(self):
        self.search_var.set("")
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self.catalogo:
            return

        rows = self.catalogo.search(self.search_var.get())
        for row in rows:
            values = [
                row.get("Codice_Articolo") or "",
                row.get("Descrizione") or "",
                row.get("desc_marca") or "",
                row.get("Codice_Articolo_Fornitore") or "",
                row.get("prezzo_lordo") if row.get("prezzo_lordo") is not None else "",
                row.get("prezzo_netto") if row.get("prezzo_netto") is not None else "",
            ]
            self.tree.insert("", "end", values=values)

        self.status_var.set(
            f"Visualizzati {len(rows)} articoli"
            + (f" su {len(self.catalogo.rows)}" if len(rows) == 500 else "")
        )


if __name__ == "__main__":
    app = SSTManager()
    app.mainloop()
