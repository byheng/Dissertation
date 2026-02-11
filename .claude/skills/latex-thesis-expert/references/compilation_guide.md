# 编译与环境指南 (Compilation & Environment Guide)

## 1. 命令行编译 (`artratex.sh`)

本模板提供了一个自动化编译脚本 `artratex.sh`（位于根目录）。

### 常用命令
*   **XeLaTeX + BibTeX (推荐)**:
    ```bash
    ./artratex.sh xa Thesis.tex
    ```
*   **PDFLaTeX + BibTeX**:
    ```bash
    ./artratex.sh pa Thesis.tex
    ```
*   **LuaLaTeX + Biber**:
    ```bash
    ./artratex.sh lb Thesis.tex
    ```

### 脚本逻辑
1.  自动在当前目录创建 `Tmp/` 文件夹存放中间文件。
2.  设置 `TEXINPUTS`, `BIBINPUTS` 等环境变量，支持递归搜索子目录。
3.  编译成功后会自动尝试打开 pdf 文件。

---

## 2. VS Code LaTeX Workshop 集成

若要使用 VS Code 插件实现一键编译，建议在 `.vscode/settings.json` 中配置自定义 Recipe 调用 `artratex.sh`。

### 配置示例
```json
{
  "latex-workshop.latex.recipes": [
    {
      "name": "artratex (xelatex)",
      "tools": ["artratex-xelatex"]
    }
  ],
  "latex-workshop.latex.tools": [
    {
      "name": "artratex-xelatex",
      "command": "./artratex.sh",
      "args": ["xa", "Thesis.tex"],
      "env": {}
    }
  ]
}
```

---

## 3. 规范化调整要求 (UCAS Standard)

*   **双语题注**：所有图表必须使用 `\bicaption` 命令。
    ```latex
    \begin{figure}
        \centering
        \includegraphics[width=0.8\textwidth]{Img/example}
        \bicaption{中文标题}{English Title}
        \label{fig:example}
    \end{figure}
    ```
*   **数学符号**：变量使用斜体，矩阵和向量建议使用粗斜体（通过 `\bm`），单位使用正体（`\mathrm`）。
*   **引用规范**：
    *   正文引用：`\cite{key}` (上标) 或 `\citep{key}` (平排)。
    *   图表引用：`图~\ref{fig:key}`，`表~\ref{tab:key}`。建议使用 `~` 防止换行断开。
