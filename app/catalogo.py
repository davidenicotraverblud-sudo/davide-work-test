from __future__ import annotations

from pathlib import Path
from typing import Any

from openpyxl import load_workbook


SHEET_NAME = "Anagrafica articoli"
REQUIRED_COLUMNS = {"Codice_Articolo", "Descrizione"}


class CatalogError(Exception):
    """Errore nella lettura del file anagrafica."""


class CatalogoArticoli:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.columns: dict[str, int] = {}
        self.rows: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        if not self.file_path.is_file():
            raise CatalogError(f"File non trovato: {self.file_path}")

        try:
            workbook = load_workbook(
                self.file_path,
                read_only=True,
                data_only=True,
            )
        except Exception as exc:
            raise CatalogError(f"Impossibile aprire il file Excel: {exc}") from exc

        try:
            if SHEET_NAME not in workbook.sheetnames:
                raise CatalogError(
                    f"Nel file manca il foglio richiesto '{SHEET_NAME}'."
                )

            sheet = workbook[SHEET_NAME]
            headers = [
                str(value).strip() if value is not None else ""
                for value in next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
            ]
            self.columns = {
                name: index
                for index, name in enumerate(headers)
                if name
            }

            missing = REQUIRED_COLUMNS - self.columns.keys()
            if missing:
                raise CatalogError(
                    "Intestazioni mancanti nel foglio Anagrafica articoli: "
                    + ", ".join(sorted(missing))
                )

            self.rows = []
            for values in sheet.iter_rows(min_row=2, values_only=True):
                if not values or not any(value is not None for value in values):
                    continue
                item = {
                    name: values[index] if index < len(values) else None
                    for name, index in self.columns.items()
                }
                self.rows.append(item)
        finally:
            workbook.close()

    def search(self, query: str, limit: int = 500) -> list[dict[str, Any]]:
        needle = query.casefold().strip()
        if not needle:
            return self.rows[:limit]

        results = []
        searchable = (
            "Codice_Articolo",
            "Descrizione",
            "Descrizione_estesa",
            "Codice_Articolo_Fornitore",
            "Codice_fornitore",
            "desc_marca",
        )
        for item in self.rows:
            text = " ".join(
                str(item.get(key) or "")
                for key in searchable
            ).casefold()
            if needle in text:
                results.append(item)
                if len(results) >= limit:
                    break
        return results
