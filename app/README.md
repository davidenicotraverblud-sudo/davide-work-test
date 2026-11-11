# Applicazione SST

Prima versione della nuova applicazione Windows che sostituirà progressivamente il file Excel `XXXXX26-FPD001.xlsm`.

## Stato
Questa è la base tecnica iniziale, non ancora la replica completa del workbook. Il primo modulo permette di aprire e consultare l'anagrafica articoli esterna.

## Scelte tecniche
- Python per la logica applicativa.
- Tkinter per l'interfaccia desktop iniziale.
- openpyxl per leggere il file Excel dell'anagrafica.
- PyInstaller per generare l'eseguibile Windows.

## Anagrafica articoli
Il programma cerca il foglio `Anagrafica articoli` e usa la prima riga come intestazione. Il file resta esterno e aggiornabile: non viene incorporato nell'eseguibile.

Il percorso del file può essere indicato dall'utente dalla finestra dell'applicazione. In seguito verrà aggiunta anche una configurazione persistente del percorso.

## Avvio in sviluppo
Dalla cartella `app`:

```bat
python -m pip install -r requirements.txt
python main.py
```

## Creazione EXE (Windows)
Dalla cartella `app`:

```bat
build.bat
```

Il risultato sarà creato in `dist\SST Manager.exe`.

## Prossimi moduli
1. Mappatura completa delle macro VBA e dei flussi operativi.
2. Scheda commessa e dati generali.
3. Progettazione SST e calcoli tecnici.
4. Distinta componenti e listini.
5. Fogli produzione IT/FR.
6. Scarichi, contatori e revisioni.
7. Esportazioni Excel/PDF e integrazione Outlook.
