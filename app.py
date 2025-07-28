import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class ClusterAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shluková analýza - Cluster Analysis")
        self.root.geometry("800x600")
        
        self.data = None
        self.category_columns = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Nahrání souboru
        file_frame = ttk.LabelFrame(main_frame, text="Nahrání dat", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_frame, text="Vybrat CSV/XLSX soubor", 
                  command=self.load_file).grid(row=0, column=0, padx=5)
        
        self.file_label = ttk.Label(file_frame, text="Žádný soubor nevybrán")
        self.file_label.grid(row=0, column=1, padx=10)
        
        # Parametry
        params_frame = ttk.LabelFrame(main_frame, text="Parametry analýzy", padding="5")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # S (počet shluků)
        ttk.Label(params_frame, text="Počet shluků (S):").grid(row=0, column=0, padx=5, pady=2)
        self.s_var = tk.IntVar(value=4)
        s_spinbox = ttk.Spinbox(params_frame, from_=2, to=10, textvariable=self.s_var, width=10)
        s_spinbox.grid(row=0, column=1, padx=5, pady=2)
        
        # BW_ADJUST
        ttk.Label(params_frame, text="BW Adjust:").grid(row=1, column=0, padx=5, pady=2)
        self.bw_var = tk.DoubleVar(value=1.0)
        bw_spinbox = ttk.Spinbox(params_frame, from_=0.1, to=3.0, increment=0.1, 
                                textvariable=self.bw_var, width=10)
        bw_spinbox.grid(row=1, column=1, padx=5, pady=2)
        
        # THRESH
        ttk.Label(params_frame, text="Threshold:").grid(row=2, column=0, padx=5, pady=2)
        self.thresh_var = tk.DoubleVar(value=0.2)
        thresh_spinbox = ttk.Spinbox(params_frame, from_=0.01, to=1.0, increment=0.01, 
                                    textvariable=self.thresh_var, width=10)
        thresh_spinbox.grid(row=2, column=1, padx=5, pady=2)
        
        # Levels
        ttk.Label(params_frame, text="Levels:").grid(row=3, column=0, padx=5, pady=2)
        self.levels_var = tk.IntVar(value=5)
        levels_spinbox = ttk.Spinbox(params_frame, from_=3, to=10, textvariable=self.levels_var, width=10)
        levels_spinbox.grid(row=3, column=1, padx=5, pady=2)
        
        # Tlačítko pro spuštění analýzy
        ttk.Button(main_frame, text="Spustit analýzu", 
                  command=self.run_analysis).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Textové pole pro výsledky
        results_frame = ttk.LabelFrame(main_frame, text="Výsledky analýzy", padding="5")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = tk.Text(results_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Konfigurace grid weights
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Vyberte datový soubor",
            filetypes=[("CSV soubory", "*.csv"), ("Excel soubory", "*.xlsx"), ("Všechny soubory", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    self.data = pd.read_excel(file_path)
                else:
                    messagebox.showerror("Chyba", "Nepodporovaný formát souboru!")
                    return
                
                # Automaticky detekujeme numerické sloupce (kromě možných ID sloupců)
                numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
                
                # Odfiltrujeme sloupce s názvy naznačujícími ID nebo indexy
                self.category_columns = [col for col in numeric_columns 
                                       if not any(keyword in col.lower() 
                                                for keyword in ['id', 'index', 'idx', 'cluster'])]
                
                filename = os.path.basename(file_path)
                self.file_label.config(text=f"Nahráno: {filename} ({len(self.data)} řádků)")
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Soubor úspěšně nahrán: {filename}\n")
                self.results_text.insert(tk.END, f"Počet řádků: {len(self.data)}\n")
                self.results_text.insert(tk.END, f"Detekované kategorie: {', '.join(self.category_columns)}\n\n")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst soubor:\n{str(e)}")
    
    def run_analysis(self):
        if self.data is None:
            messagebox.showerror("Chyba", "Nejprve nahrajte datový soubor!")
            return
        
        if not self.category_columns:
            messagebox.showerror("Chyba", "Nebyly nalezeny vhodné sloupce pro analýzu!")
            return
        
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Spouštím analýzu...\n")
            self.root.update()
            
            # Příprava dat
            data_filtered = self.data.copy()
            odpovedi_sum = data_filtered[self.category_columns].sum(axis=1)
            data_filtered = data_filtered[odpovedi_sum > 0].reset_index(drop=True)
            X = data_filtered[self.category_columns]
            
            self.results_text.insert(tk.END, f"Původní počet respondentů: {len(self.data)}\n")
            self.results_text.insert(tk.END, f"Počet po filtraci: {len(data_filtered)}\n\n")
            self.root.update()
            
            # Clustering
            FINAL_S = self.s_var.get()
            kmeans = KMeans(n_clusters=FINAL_S, random_state=42, n_init=10)
            data_filtered['cluster'] = kmeans.fit_predict(X)
            
            # t-SNE
            self.results_text.insert(tk.END, "Provádím t-SNE redukci...\n")
            self.root.update()
            
            tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(data_filtered)-1), max_iter=1000)
            tsne_results = tsne.fit_transform(X)
            data_filtered['tsne_x'] = tsne_results[:, 0]
            data_filtered['tsne_y'] = tsne_results[:, 1]
            
            # Vytvoření grafu
            self.create_plot(data_filtered, FINAL_S)
            
            # Výpis výsledků
            self.results_text.insert(tk.END, "\nKOMPLETNÍ POŘADÍ TÉMAT V JEDNOTLIVÝCH SHLUCÍCH:\n\n")
            
            for i in range(FINAL_S):
                cluster_data = data_filtered[data_filtered['cluster'] == i]
                summary = cluster_data[self.category_columns].mean().sort_values(ascending=False)
                self.results_text.insert(tk.END, f"--- Shluk {i + 1} ({len(cluster_data)} respondentů) ---\n")
                
                for rank, (theme, percentage) in enumerate(summary.items(), 1):
                    self.results_text.insert(tk.END, f"  {rank}. {theme}: {percentage:.1%}\n")
                self.results_text.insert(tk.END, "\n")
            
            self.root.update()
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při analýze:\n{str(e)}")
    
    def create_plot(self, data, FINAL_S):
        # Parametry z GUI
        BW_ADJUST = self.bw_var.get()
        THRESH = self.thresh_var.get()
        LEVELS = self.levels_var.get()
        
        fig, ax = plt.subplots(figsize=(16, 10))
        palette = sns.color_palette("deep", FINAL_S)
        
        sns.scatterplot(
            data=data, x='tsne_x', y='tsne_y', hue='cluster',
            palette=palette, alpha=0.3, s=25, legend=False, ax=ax
        )
        
        sns.kdeplot(
            data=data, x='tsne_x', y='tsne_y', hue='cluster',
            palette=palette, fill=False,
            levels=LEVELS,
            linewidths=1.2,
            bw_adjust=BW_ADJUST,
            thresh=THRESH,
            legend=False, ax=ax
        )
        
        legend_texts = []
        for i in range(FINAL_S):
            cluster_data = data[data['cluster'] == i]
            summary = cluster_data[self.category_columns].mean().sort_values(ascending=False)
            legend_title = f"Shluk {i + 1} ({len(cluster_data)} respondentů)"
            
            top_themes = "\n".join([f"  • {col}" for col, val in summary.head(4).items()])
            legend_texts.append(plt.Line2D([0], [0], marker='o', color='w', label=f"{legend_title}\n{top_themes}",
                                           markerfacecolor=palette[i], markersize=10))
        
        ax.legend(handles=legend_texts, title="Charakteristika shluků", loc='upper right', 
                 fontsize=9, frameon=True, facecolor='white', framealpha=0.85)
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # Uložení do složky výsledků
        output_dir = "vysledky"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_filename = os.path.join(output_dir, f'cluster_S-{FINAL_S}_BW-{BW_ADJUST}_T-{THRESH}.png')
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.results_text.insert(tk.END, f"Graf uložen jako: {output_filename}\n")

def main():
    root = tk.Tk()
    app = ClusterAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

