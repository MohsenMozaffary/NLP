from langchain.document_loaders import PyPDFLoader


"""
    Loader's role is to load and read .pdf files.
    It takes a list of folder directories, reads them and stack them to final returned output.

"""

def import_pdf(dirs):
    print('loading the pdfs...')
    pdfs = []
    for dir in dirs:
        pdfs.extend(PyPDFLoader(dir).load())

    return pdfs