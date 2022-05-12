import io
import os.path

import panflute
import pypandoc


# 读取md图片地址
def __prepare(doc):
    doc.images = []
    doc.links = []


def __action(elem, doc):
    if isinstance(elem, panflute.Image):
        doc.images.append(elem)
    elif isinstance(elem, panflute.Link):
        doc.links.append(elem)


def scan_imgs(file_path):
    data = pypandoc.convert_file(file_path, 'json')
    doc = panflute.load(io.StringIO(data))
    doc.images = []
    doc.links = []
    doc = panflute.run_filter(__action, prepare=__prepare, doc=doc)
    results = []
    for image in doc.images:
        results.append(image.url)
    return results
