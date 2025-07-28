# Shluková analýza - GUI aplikace

Tato aplikace umožňuje provádět shlukovou analýzu dat s grafickým uživatelským rozhraním.

## Funkce
- Nahrání CSV nebo XLSX souborů
- Automatická detekce numerických sloupců
- Nastavitelné parametry analýzy (počet shluků, BW adjust, threshold, levels)
- Generování grafů s výsledky
- Uložení výsledků do složky "vysledky"

## Instalace a spuštění

### Metoda 1: Přímé spuštění Python skriptu
```bash
pip install -r requirements.txt
python app.py
```

### Metoda 2: Kompilace do EXE souboru

**Na macOS/Linux:**
```bash
./build.sh
```

**Na Windows:**
```cmd
build.bat
```

Po kompilaci bude EXE soubor v složce `dist/ClusterAnalysis` (Linux/macOS) nebo `dist/ClusterAnalysis.exe` (Windows).

## Použití

1. Spusťte aplikaci
2. Klikněte na "Vybrat CSV/XLSX soubor" a nahrajte váš datový soubor
3. Nastavte parametry analýzy:
   - **Počet shluků (S)**: 2-10 shluků
   - **BW Adjust**: 0.1-3.0 pro vyhlazování
   - **Threshold**: 0.01-1.0 pro prahování
   - **Levels**: 3-10 úrovní kontur
4. Klikněte na "Spustit analýzu"
5. Výsledky se zobrazí v textovém poli a graf se uloží do složky "vysledky"

## Požadavky na data

- Soubor musí být ve formátu CSV nebo XLSX
- Musí obsahovat numerické sloupce pro analýzu
- Sloupce s názvy obsahujícími "id", "index", "idx", "cluster" budou automaticky ignorovány
- Řádky s nulovými hodnotami ve všech kategoriích budou odstraněny

## Výstupy

- Graf shluků uložený jako PNG soubor ve složce "vysledky"
