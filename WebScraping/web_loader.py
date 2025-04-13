from langchain.document_loaders import WebBaseLoader, RecursiveUrlLoader


class WebLoader:

    def __init__(self, depth =2, n_selection = 5):

        self.depth = depth
        self.n_selection = n_selection

    def recusrsive_load_web(self, url):

        loader = RecursiveUrlLoader(
                                    url,
                                    max_depth=self.depth)
        
        docs = loader.load()
        docs = [doc for doc in docs if 'title' in doc.metadata]
        titles = [doc.metadata['title'] for doc in docs]

        if self.n_selection > len(titles):
            self.n_selection = len(titles)
            print("n_selection is changed to {}".format(len(titles)))

        return titles, docs
    

    def base_loader(self, url):

        loader = WebBaseLoader(url)
        docs = loader.load()

        contents = [doc.page_content for doc in docs]

        return contents
