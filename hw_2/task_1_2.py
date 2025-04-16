def generate_latex_table(data, caption="", label="", position="htbp"):
    """Генерирует LaTeX код для таблицы на основе входных данных"""
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input data must be a non-empty 2D list")

    num_columns = len(data[0])
    column_alignment = "c" * num_columns
    latex_code = "\\begin{table}[" + position + "]\n"
    latex_code += "\\centering\n"

    if caption:
        latex_code += "\\caption{" + caption + "}\n"

    if label:
        latex_code += "\\label{" + label + "}\n"

    latex_code += "\\begin{tabular}{|" + column_alignment + "|}\n"
    latex_code += "\\hline\n"

    for i, row in enumerate(data):
        escaped_row = []
        for cell in row:
            if isinstance(cell, (int, float)):
                escaped_row.append(str(cell))
            else:
                escaped = str(cell).replace("\\", "\\textbackslash") \
                    .replace("&", "\\&") \
                    .replace("%", "\\%") \
                    .replace("$", "\\$") \
                    .replace("#", "\\#") \
                    .replace("_", "\\_") \
                    .replace("{", "\\{") \
                    .replace("}", "\\}") \
                    .replace("~", "\\textasciitilde") \
                    .replace("^", "\\textasciicircum")
                escaped_row.append(escaped)

        latex_code += " & ".join(escaped_row) + " \\\\\n"

    latex_code += "\\hline\n"
    latex_code += "\\end{tabular}\n"
    latex_code += "\\end{table}"
    return latex_code


def generate_latex_image(filepath, caption="", label="", width="0.8\\textwidth", position="htbp"):
    """Генерирует LaTeX код для вставки изображения"""
    latex_code = "\\begin{figure}[" + position + "]\n"
    latex_code += "\\centering\n"
    latex_code += f"\\includegraphics[width={width}]{{{filepath}}}\n"

    if caption:
        latex_code += "\\caption{" + caption + "}\n"

    if label:
        latex_code += "\\label{" + label + "}\n"

    latex_code += "\\end{figure}"
    return latex_code


def generate_full_document(content, title="LaTeX Document", author="Anonymous", documentclass="article"):
    """Генерирует полный LaTeX документ с заданным содержимым"""
    return f"""\\documentclass{{{documentclass}}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T2A]{{fontenc}}
\\usepackage[russian]{{babel}}
\\usepackage{{graphicx}} % Для вставки изображений

\\title{{{title}}}
\\author{{{author}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{content}

\\end{{document}}
"""


# Пример данных для таблицы
table_data = [
    ["Столбец 1", "Столбец 2", "Столбец 3", "Столбец 4"],
    ["1", 10, 2.5, "Mister"],
    ["2", 5, 3.2, "pelican"],
    ["3", 8, 4.1, "is"],
    ["4", 12, 3.8, "standing"]
]

# Генерируем таблицу
table = generate_latex_table(
    data=table_data,
    caption="Пример таблицы с каким-то \n содержимом и пеликаном",
    label="tab:pelicans",
    position="htbp"
)

# Генерируем изображение
image = generate_latex_image(
    filepath="artifacts/image.jpg",
    caption="Пеликан (жестко удивляется)",
    label="fig:example",
    width="0.5\\textwidth"
)

# Генерируем полный документ
full_doc = generate_full_document(
    content=image + "\n\n" + table,  # Сначала изображение, затем таблица, но можно свапнуть
    title="Пример документа с таблицей и каким-то пеликаном",
    author="Анастасия Шпилева"
)

with open("artifacts/table_image.tex", "w", encoding="utf-8") as f:
    f.write(full_doc)
