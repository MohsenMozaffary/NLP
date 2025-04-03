from langchain.document_loaders import RecursiveUrlLoader, WebBaseLoader

class webScraper():

    def __init__(self, mode ="base"):

        self.mode = mode

    def base_loader(self, url):

        loader = WebBaseLoader(url)
        docs = loader.load()

        return docs
    
    def recursive(self, url, depth = 2):
        
        loader = RecursiveUrlLoader(url, max_depth = depth)
        docs = loader.load()

        return docs

    def scrape_url(self, url, max_depth = 2):

        if self.mode == "base":
            docs = self.base_loader(url)
        elif self.mode == "recursive":
            docs = self.recursive(url, depth = max_depth)

        return docs


