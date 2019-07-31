import os
import PyPDF2
import re
import time


def get_page_num(num_str):
    num_list = num_str.split(",")
    num_need_list = []
    for pageNum in num_list:
        if pageNum.__contains__("-"):
            page_num_index = pageNum.split("-")
            for i in range(int(page_num_index[0]), int(page_num_index[1])+1):
                num_need_list.append(i)
        else:
            num_need_list.append(int(pageNum))

    return num_need_list


def pdf_split(pdf_file_name, num_str):
    num_need_list = get_page_num(num_str)
    pdf_read = PyPDF2.PdfFileReader(open(pdf_file_name, "rb"))
    pagenum = pdf_read.getNumPages()
    pdf_write = PyPDF2.PdfFileWriter()
    for index in num_need_list:
        if pagenum < index:
            print("The page num is less than your input")
            return
        pdf_obj = pdf_read.getPage(index-1)
        pdf_write.addPage(pdf_obj)
    pdf_write.write(open("splitTest.pdf", "wb"))
    print("Please check the file: splitTest.pdf")


def pdf_merge(pdf_file_list):
    pdf_writer = PyPDF2.PdfFileWriter()
    if len(pdf_file_list) >0:
        for pdf_file in pdf_file_list:
            pdf_reader = PyPDF2.PdfFileReader(open(pdf_file, "rb"))
            page_total_num = pdf_reader.getNumPages()
            for index in range(0, page_total_num):
                pdf_obj = pdf_reader.getPage(index)
                pdf_writer.addPage(pdf_obj)
        pdf_writer.write(open("merged.pdf", "wb"))
    else:
        print("mergePDFDir is empty directory. Please check again!!!")
        return


if __name__ == '__main__':
    print("1.Split PDF")
    print("2.Merge PDF")
    print("3.Exit")
    check_num = input("Please choose the function:")
    if check_num == "1":
        if not os.path.exists(os.getcwd() + os.sep + "splitPDFDir"):
            os.mkdir("splitPDFDir", 0o666)
        input("Please put the file into splitPDFDir Directory.Only can put 1 file......")
        split_file_list = os.listdir(os.getcwd() + os.sep + "splitPDFDir")
        if len(split_file_list) > 0:
            pdf_file_name1 = os.getcwd() + os.sep + "splitPDFDir" + os.sep + split_file_list[0]
        else:
            print("splitPDFdir is empty dir.Please check. THX")
            exit()
        print("Need split file is:  " + pdf_file_name1)
        numValue1 = input("Please input the number you want to get: ")
        pdf_split(pdf_file_name1, numValue1)
    elif check_num == "2":
        if not os.path.exists(os.getcwd() + os.sep + "mergePDFDir"):
            os.mkdir("mergePDFDir", 0o666)
        input("Please put pdf files into mergePDFDir Directory.......")
        my_path = os.getcwd() + os.sep + "mergePDFDir"
        pattern = r".pdf$"
        list1 = [my_path + os.sep + item for item in os.listdir(my_path) if re.search(pattern, item, re.IGNORECASE)]
        pdf_merge(list1)
    else:
        print("System will exit in 3s")
        time.sleep(3)
        print("THX for Use")
        exit()
    print("THX for Use")