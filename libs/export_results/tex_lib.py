#Usefull tags in latex
BEG_DOCUMENT_CLASS_TAG = "\\documentclass[a4paper]{article}"
BEG_DOCUMENT_TAG = "\\begin{document}"
END_DOCUMENT_TAG = "\\end{document}"
BEG_TABULAR_TAG = "\\begin{tabular}"
END_TABULAR_TAG = "\\end{tabular}"

#Functions

#About file
def open_latex_file(path):
    """
    Function to open a latex file, to save results in it.
    Return a pointer to the latex file object.
    path : The path file of the latex file.
    Note : the label is "a" for append - each statement of this function will append the data, not replace the file by the given data.
    """
    try:
        return open(path, "a")
    except:
        print("ERROR : failed to open {0}".format(path))

def close_latex_file(latex_f):
    """
    Function to close the latex file object, given as parameter.
    Return a boolean - True if the latex file object as been closed, else False.
    latex_f : The pointer to the latex file object to close.
    """
    try:
        close_document(latex_f)
        latex_f.close()
    except:
        print("ERROR : failed to close {0}".format(latex_f.name))
        return False
    return True

#About tag
def open_document(latex_f):
    """
    Function to write beginning tags in latex file object.
    latex_f : The pointer to the latex file object to close.
    """
    write_in_latex_file(BEG_DOCUMENT_CLASS_TAG, latex_f)
    write_in_latex_file(BEG_DOCUMENT_TAG, latex_f)

def close_document(latex_f):
    """
    Function to write ending tags in latex file object.
    latex_f : The pointer to the latex file object to close.
    """
    write_in_latex_file(END_DOCUMENT_TAG, latex_f)

def open_table(columns, latex_f):
    """
    Function to begin the table in latex file object.
    columns : The number of columns to add in the table
    latex_f : The pointer to the latex file object.
    """
    write_in_latex_file("{0}{{1}|}".format(BEG_TABULAR_TAG, "|l"*columns), latex_f)

def close_table(latex_f):
    """
    Function to begin the tabular in latex file object.
    latex_f : The pointer to the latex file object.
    """
    write_in_latex_file(END_TABULAR_TAG, latex_f)

def new_line_in_table(latex_f):
    """
    Function to write some code to make a new line in latex file object.
    latex_f : The pointer to the latex file object.
    """
    write_in_latex_file("\\\\", latex_f)
    write_in_latex_file("\\hline", latex_f)

#Low level - clear and write data in a latex file
def clear_latex_file(latex_f):
    """
    Function to clear the latex file given as parameter, by the latex file object.
    latex_f : The pointer to the latex file object to clear.
    """
    try:
        latex_f.seek(0)
        latex_f.truncate()
    except:
        print("ERROR : failed to clear {0}".format(latex_f.name))

def write_in_latex_file(data, latex_f):
    """
    Function to append the data given as parameter in a latex file.
    data : The data to save (a string which represents a single tabular line in latex).
    latex_f :  The pointer to the latex file object to close.
    """
    try:
        latex_f.write("{0}\n".format(data))
    except:
        print("ERROR : failed to save data in {0}".format(latex_f.name))
