import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import re
import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

hops_data = []

def run_traceroute():

    target = entry.get().strip()

    if target == "":
        messagebox.showerror("Error", "Please enter a domain or IP address")
        return

    for row in tree.get_children():
        tree.delete(row)

    hops_data.clear()

    try:

        command = ["traceroute", "-m", "15", target]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        output = result.stdout.split("\n")

        for line in output:

            match = re.search(r"^\s*(\d+)\s+.*\(([\d\.]+)\)\s+([\d\.]+)\s+ms", line)

            if match:

                hop = match.group(1)
                ip = match.group(2)
                latency = match.group(3) + " ms"

                hops_data.append((hop, ip, latency))

                tree.insert("", "end", values=(hop, ip, latency))

        hop_label.config(text=f"Total Hops: {len(hops_data)}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def visualize_path():

    if len(hops_data) == 0:
        messagebox.showinfo("Info", "Run traceroute first")
        return

    G = nx.Graph()

    for i in range(len(hops_data) - 1):

        node1 = hops_data[i][1]
        node2 = hops_data[i + 1][1]

        G.add_edge(node1, node2)

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=2200,
        font_size=9
    )

    plt.title("Traceroute Network Path")
    plt.show()


def save_report():

    if len(hops_data) == 0:
        messagebox.showinfo("Info", "No data to save")
        return

    file = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if file:

        df = pd.DataFrame(
            hops_data,
            columns=["Hop", "IP Address", "Latency"]
        )

        df.to_csv(file, index=False)

        messagebox.showinfo("Saved", "Report saved successfully")


def clear_table():

    for row in tree.get_children():
        tree.delete(row)

    hops_data.clear()
    hop_label.config(text="Total Hops: 0")


root = tk.Tk()

root.title("Traceroute Network Visualizer")

root.geometry("900x550")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#2e2e3e",
                foreground="white",
                rowheight=28,
                fieldbackground="#2e2e3e")

style.configure("Treeview.Heading",
                font=("Arial",11,"bold"))

title = tk.Label(root,
                 text="Traceroute Network Visualization Tool",
                 font=("Arial",18,"bold"),
                 bg="#1e1e2f",
                 fg="white")

title.pack(pady=15)

input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10)

label = tk.Label(input_frame,
                 text="Enter Domain / IP:",
                 bg="#1e1e2f",
                 fg="white",
                 font=("Arial",11))

label.pack(side=tk.LEFT)

entry = tk.Entry(input_frame,
                 width=35,
                 font=("Arial",11))

entry.pack(side=tk.LEFT,padx=8)

run_btn = tk.Button(input_frame,
                    text="Run Traceroute",
                    bg="#4CAF50",
                    fg="white",
                    font=("Arial",10,"bold"),
                    command=run_traceroute)

run_btn.pack(side=tk.LEFT)

hop_label = tk.Label(root,
                     text="Total Hops: 0",
                     bg="#1e1e2f",
                     fg="white",
                     font=("Arial",11,"bold"))

hop_label.pack()

columns = ("Hop","IP Address","Latency")

tree = ttk.Treeview(root,
                    columns=columns,
                    show="headings")

tree.heading("Hop",text="Hop")
tree.heading("IP Address",text="IP Address")
tree.heading("Latency",text="Latency")

tree.column("Hop",width=80)
tree.column("IP Address",width=400)
tree.column("Latency",width=120)

tree.pack(fill=tk.BOTH,expand=True,padx=25,pady=20)

btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

visual_btn = tk.Button(btn_frame,
                       text="Visualize Path",
                       bg="#2196F3",
                       fg="white",
                       width=15,
                       command=visualize_path)

visual_btn.grid(row=0,column=0,padx=10)

save_btn = tk.Button(btn_frame,
                     text="Save Report",
                     bg="#9C27B0",
                     fg="white",
                     width=15,
                     command=save_report)

save_btn.grid(row=0,column=1,padx=10)

clear_btn = tk.Button(btn_frame,
                      text="Clear",
                      bg="#FF9800",
                      fg="white",
                      width=15,
                      command=clear_table)

clear_btn.grid(row=0,column=2,padx=10)

exit_btn = tk.Button(btn_frame,
                     text="Exit",
                     bg="#f44336",
                     fg="white",
                     width=15,
                     command=root.quit)

exit_btn.grid(row=0,column=3,padx=10)

root.mainloop()