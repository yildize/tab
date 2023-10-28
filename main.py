from splitters.PdfSplitter import PdfSplitter


pdf_splitter = PdfSplitter(local_src_path="./extern")
splits = pdf_splitter.split(save=True)
