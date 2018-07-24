import os
import shutil
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import unicodedata
def pdf_to_text(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    result = []
    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    l = result
    cv_summary = {}
    counter = -1
    for line in l:
        counter+= 1
        
        if "Желаемая должность и зарплата" in line:
            cv_summary["position"] = l[counter+1]
            counter_l = counter + 3
            
            while("•" in l[counter_l]):
                cv_summary["position"] += " " + l[counter_l]
                counter_l += 1
        
        if "Навыки" in line:
            cv_summary["skills"] = l[counter+1]
            counter_l = counter+2
            
            while True:
                cv_summary["skills"] += " " + l[counter_l]
                counter_l += 1
                if("Опыт вождения" or "Дополнительная информация" in l[counter_l]):
                    break
        
        if "Образование" in line:
            cv_summary["education"] = l[counter+1]
            counter_l = counter+2
            
            while True:
                if("Резюме обновлено" not in l[counter_l]):
                    if("Ключевые навыки" in l[counter_l]):
                        break
                    cv_summary["education"] += " " + l[counter_l]
                
                counter_l += 1
        
        if "Опыт работы" in line:
            cv_summary["work"] = l[counter+1]
            counter_l = counter+2
            
            while True:
                if("Резюме обновлено" not in l[counter_l]):
                    if("Образование" in l[counter_l]):
                        break
                    cv_summary["work"] += " " + l[counter_l]
                
                counter_l += 1
                
    for key in cv_summary:
        cv_summary[key] = cv_summary[key].replace('.', '').split()

    cv_summary["position"] = [x for x in cv_summary["position"]  if x != "•"]

    return cv_summary