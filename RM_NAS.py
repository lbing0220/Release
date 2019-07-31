#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
from datetime import datetime
import shutil
import time
import threading

delPath = r"D:\Share\myProjects\gitProjects"
keepDays = 1

checkPath = r"/home/albin/myProjects/"
dt = datetime.now()
log_name = os.getcwd() + os.sep + "rm_nas_log_" + dt.strftime('%Y-%m-%d')
eqp_id_list = []
lay_list = []
step_list = []


if delPath == checkPath:
    for dir1 in os.listdir(delPath):
        dir1_full_path = delPath + os.sep + dir1
        if os.path.isdir(dir1_full_path):
            eqp_id_list.append(dir1_full_path)
            for dir2 in os.listdir(dir1_full_path):
                dir2_full_path = dir1_full_path + os.sep + dir2
                if os.path.isdir(dir2_full_path):
                    lay_list.append(dir2_full_path)
                    for dir3 in os.listdir(dir2_full_path):
                        dir3_full_path = dir2_full_path + os.sep + dir3
                        if os.path.isdir(dir3_full_path):
                            step_list.append(dir3_full_path)


def rm_nas(*del_path):
    print(threading.current_thread())
    # print(threading.active_count())
    time.sleep(3)
    for single_path in del_path:
        # print(str(datetime.now()) + "  " + str(del_path) + "  PROCESS:  %.2f%%" % (
        #        (del_path.index(single_path) + 1) * 100 / len(del_path)))
        if os.path.isdir(single_path):
            print(single_path + " is a directory")
            child_list = os.listdir(single_path)
            for child in child_list:
                child_full_name = single_path + os.sep + child
                print(str(datetime.now()) + "  " + single_path + "  PROCESS:  %.2f%%    " % (
                        (child_list.index(child) + 1) * 100 / len(child_list)))
                print(child_full_name)
                if os.path.isdir(child_full_name):
                    dt_dir = datetime.fromtimestamp(os.path.getatime(child_full_name))
                    if (dt - dt_dir).days > keepDays:
                        print("Delete directory: " + child_full_name)
                        ##shutil.rmtree(child_full_name)
                        if len(os.listdir(os.path.dirname(child_full_name))) == 0:
                            print("Delete Father Directory: " + os.path.dirname(child_full_name))
                            ###os.removedirs(os.path.dirname(child_full_name))
                    elif len(os.listdir(child_full_name)) == 0:
                        print("Delete Empty Directory: " + child_full_name)
                        ###os.removedirs(child_full_name)
                    else:
                        rm_nas(child_full_name)
                elif os.path.isfile(child_full_name):
                    print(child_full_name + " is a file in " + single_path)
                    dt_file = datetime.fromtimestamp(os.path.getctime(child_full_name))
                    if (dt - dt_file).days > keepDays:
                        print("Delete timeout file: " + child_full_name)
                        ####os.remove(child_full_name)
                        if len(os.listdir(os.path.dirname(child_full_name))) == 0:
                            print("Delete father directory after file deleted" + os.path.dirname(child_full_name))
                            ####os.removedirs(os.path.dirname(child_full_name))
                else:
                    print(child_full_name + "is not a file or directory")

        elif os.path.isfile(single_path):
            print(single_path + " is a file")

        else:
            print(single_path + " is not a file or directory")


def thread_choose(del_thread_path):
    child_thread_list = sorted(os.listdir(del_thread_path))
    child_thread_list_length = len(child_thread_list)
    thread_max_count = 10								#  最大线程数

    if child_thread_list_length <= thread_max_count:
        print("Every para has one single thread")
        for child_thread in child_thread_list:
            child_thread_fullpath = del_thread_path + os.sep + child_thread
            thrd = threading.Thread(target=rm_nas, args=(child_thread_fullpath,))
            thrd.start()

    else:
        print("==========")
        if child_thread_list_length % thread_max_count == 0:
            thread_index_span = int(child_thread_list_length / thread_max_count)     # 刚好整除
        else:
            thread_index_span = int(child_thread_list_length / thread_max_count) + 1   # 不能被整除的情况
        thread_num = 0
        while thread_num < child_thread_list_length:
            para_tup = tuple(del_thread_path + os.sep + child_thread
                             for child_thread in child_thread_list[thread_num: thread_num + thread_index_span])
            thrd = threading.Thread(target=rm_nas, args=para_tup)
            print(para_tup)
            thrd.start()


            thread_num += thread_index_span

    while True:   # Main Thread Keep Runing and wait only main thread left
        if threading.active_count() == 1:
            print("Finished")
            break


if __name__ == "__main__":
    with open(log_name, "a+") as dateoutput:
        dateoutput.write("##########################Begin:" + str(datetime.now()) + "##########################\n")
        dateoutput.flush()
        try:
            if delPath == checkPath:
                print("Will run fast speed")
                for step_id in step_list:
                    thread_choose(step_id)
            else:
                print("Will run normal speed")
                thread_choose(delPath)
        except Exception as ex:
            print("Some Error Happened")
            dateoutput.write("Some Error Happened\n")
            dateoutput.write(str(ex) + "\n")
        finally:
            dateoutput.write("#########################Finish:" + str(datetime.now()) + "##########################\n")


'''
def rm_nas(path):
    dirlist = os.listdir(path)
    for fileOrDirectory in dirlist:
        if os.path.basename(path):
            fileOrDirectoryFullName = path + os.sep + fileOrDirectory
        else:
            fileOrDirectoryFullName = path + fileOrDirectory
        ### Print the percent
        print(str(datetime.now()) + "  " + path + "  PROCESS:  %.2f%%" % (
                        (dirlist.index(fileOrDirectory) + 1) * 100 / len(dirlist)))

        if os.path.isdir(fileOrDirectoryFullName):
            dt_Dir = datetime.fromtimestamp(os.path.getatime(fileOrDirectoryFullName))  ##LastAccessTime
            if (dt - dt_Dir).days > keepDays:
                shutil.rmtree(fileOrDirectoryFullName)
            elif len(os.listdir(fileOrDirectoryFullName)) == 0:
                os.removedirs(fileOrDirectoryFullName)
            else:
                rm_nas(fileOrDirectoryFullName)
        elif os.path.isfile(fileOrDirectoryFullName):
            dt_File = datetime.fromtimestamp(os.path.getctime(fileOrDirectoryFullName))  ##FileCreateTime
            if (dt - dt_File).days > keepDays:
                os.remove(fileOrDirectoryFullName)
                if len(os.listdir(os.path.dirname(fileOrDirectoryFullName))) == 0:
                    os.removedirs(os.path.dirname(fileOrDirectoryFullName))
        else:  # Path type is not directory and file. Will try to remove
            os.remove(fileOrDirectoryFullName)


def thread_choose(path):
    childlist = os.listdir(path)
    with open(path + os.sep + "temp.txt", "a+") as temp:
        temp.write("Only for temp, You need to delete it by hand only some error happens\n")
        for dir in childlist:
            if os.path.basename(path):
                dir_full_path = path + os.sep + dir
            else:
                dir_full_path = path + dir
            if os.path.isdir(dir_full_path):
                if len(os.listdir(dir_full_path)) == 0:
                    os.removedirs(dir_full_path)
                elif (childlist.index(dir) + 1) % 9 == 0:
                    #print("thrd9 will be running")
                    thrd9 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd9.start()
                elif (childlist.index(dir) + 1) % 8 == 0:
                    #print("thrd8 will be running")
                    thrd8 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd8.start()
                elif (childlist.index(dir) + 1) % 7 == 0:
                    #print("thrd7 will be running")
                    thrd7 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd7.start()
                elif (childlist.index(dir) + 1) % 6 == 0:
                    #print("thrd6 will be running")
                    thrd6 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd6.start()
                elif (childlist.index(dir) + 1) % 5 == 0:
                    #print("thrd5 will be running")
                    thrd5 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd5.start()
                elif (childlist.index(dir) + 1) % 4 == 0:
                    #print("thrd4 will be running")
                    thrd4 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd4.start()
                elif (childlist.index(dir) + 1) % 3 == 0:
                    #print("thrd3 will be running")
                    thrd3 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd3.start()
                elif (childlist.index(dir) + 1) % 2 == 0:
                    #print("thrd2 will be running")
                    thrd2 = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd2.start()
                else:
                    #print("thrd will be running")
                    thrd = threading.Thread(target=rm_nas, args=(dir_full_path,))
                    thrd.start()
            else:
                dt_file = datetime.fromtimestamp(os.path.getctime(dir_full_path))
                if (dt-dt_file).days > keepDays:
                    os.remove(dir_full_path)
        while True:
            if threading.active_count() == 1:
                os.remove(path + os.sep + "temp.txt")
                break


try:
    with open(log_name, "a+") as dateoutput:
        dateoutput.write("##########################Begin:" + str(datetime.now()) + "##########################\n")
        dateoutput.flush()
        if delPath == checkPath:
            print("Will run fast speed")
            for step_id in step_list:
                thread_choose(step_id)
        else:
            print("Will run normal speed")
            step_id = delPath
            thread_choose(delPath)
        dateoutput.write("#########################Finish:" + str(datetime.now()) + "##########################\n")
except Exception as ex:
    dateoutput.write(str(ex) + "\n")
    dateoutput.write("Some error happened.Please kindly check")'''



