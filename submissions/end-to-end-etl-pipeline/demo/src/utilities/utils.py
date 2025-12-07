"""
The 'utilities' folder contains Python modules.
Keeping them separate provides a clear overview
of utilities you can reuse across your transformations.
"""

def process_column(col: str) -> str:
    return col.strip().replace(" ", "").replace(",", "_").replace(";", "_").replace("{", "_").replace("}", "_").replace("(", "_").replace(")", "_").replace("\n", "_").replace("\t", "_").replace("=", "_")
