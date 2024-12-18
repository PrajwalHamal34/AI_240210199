#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox, scrolledtext
from rdflib import Graph
from prettytable import PrettyTable

def load_ontology():
    try:
        g = Graph()
        g.parse("Protege.owl", format="xml")
        return g
    except Exception as e:
        messagebox.showerror("Ontology Error", f"Failed to load ontology: {e}")
        return None

def convert_owl_to_ttl(owl_path, ttl_path):
    try:
        graph = Graph()
        graph.parse(owl_path, format="xml")
        graph.serialize(destination=ttl_path, format="turtle")
        return True
    except Exception as e:
        messagebox.showerror("Conversion Error", f"Failed to convert OWL to TTL: {e}")
        return False

def query_classes(graph):
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?class
    WHERE {
      ?class rdf:type owl:Class . 
    }
    """
    results = graph.query(query)
    return [str(row[0].split('#')[-1]) for row in results]

def calculate_area(shape, base, height, side):
    try:
        base = float(base) if base else 0
        height = float(height) if height else 0
        side = float(side) if side else 0

        if shape == "Rectangle":
            if base > 0 and height > 0:
                return base * height
            else:
                raise ValueError("Rectangle requires both base and height.")
        elif shape == "Square":
            if side > 0:
                return side ** 2
            else:
                raise ValueError("Square requires a valid side length.")
        elif shape == "Triangle":
            if base > 0 and height > 0:
                return 0.5 * base * height
            else:
                raise ValueError("Triangle requires both base and height.")
        else:
            raise ValueError("Unknown shape")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
        return None

def setup_gui():
    window = tk.Tk()
    window.title("Area Calculator and Ontology Viewer")
    window.geometry("600x500")

    owl_file = "Protege.owl"
    ttl_file = "Protege.ttl"
    if not convert_owl_to_ttl(owl_file, ttl_file):
        return

    graph = load_ontology()
    if not graph:
        return

    classes = query_classes(graph)

    shape_label = tk.Label(window, text="Select Shape:")
    shape_label.grid(row=0, column=0, pady=5)

    shape_var = tk.StringVar(window)
    shape_var.set("Triangle")

    shape_menu = tk.OptionMenu(window, shape_var, "Triangle", "Rectangle", "Square")
    shape_menu.grid(row=0, column=1, pady=5)

    base_label = tk.Label(window, text="Base Length:")
    base_label.grid(row=1, column=0, pady=5)
    base_entry = tk.Entry(window)
    base_entry.grid(row=1, column=1, pady=5)

    height_label = tk.Label(window, text="Height Length:")
    height_label.grid(row=2, column=0, pady=5)
    height_entry = tk.Entry(window)
    height_entry.grid(row=2, column=1, pady=5)

    side_label = tk.Label(window, text="Side Length:")
    side_label.grid(row=3, column=0, pady=5)
    side_entry = tk.Entry(window)
    side_entry.grid(row=3, column=1, pady=5)

    def update_fields(*args):
        shape = shape_var.get()
        if shape == "Rectangle":
            base_label.grid()
            base_entry.grid()
            height_label.grid()
            height_entry.grid()
            side_label.grid_remove()
            side_entry.grid_remove()
        elif shape == "Square":
            side_label.grid()
            side_entry.grid()
            base_label.grid_remove()
            base_entry.grid_remove()
            height_label.grid_remove()
            height_entry.grid_remove()
        elif shape == "Triangle":
            base_label.grid()
            base_entry.grid()
            height_label.grid()
            height_entry.grid()
            side_label.grid_remove()
            side_entry.grid_remove()

    shape_var.trace("w", update_fields)

    def on_calculate():
        shape = shape_var.get()
        base = base_entry.get()
        height = height_entry.get()
        side = side_entry.get()

        area = calculate_area(shape, base, height, side)
        if area is not None:
            result_label.config(text=f"Area: {area:.2f}")

    calculate_button = tk.Button(window, text="Calculate Area", command=on_calculate)
    calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

    result_label = tk.Label(window, text="Area: ")
    result_label.grid(row=5, column=0, columnspan=2, pady=5)

    ontology_label = tk.Label(window, text="Ontology Classes:")
    ontology_label.grid(row=6, column=0, pady=10, sticky="w")

    ontology_text = scrolledtext.ScrolledText(window, width=50, height=10)
    ontology_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
    ontology_text.insert(tk.END, "Classes in Ontology:\n" + "\n".join(classes))

    update_fields()

    window.mainloop()

if __name__ == "__main__":
    setup_gui()


# In[2]:


get_ipython().system('pip install prettytable')


# In[ ]:




