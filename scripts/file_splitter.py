#!/usr/bin/env python

import csv
import math
import sys
import os


def split_chart(csv_path):
    """
    Split given csv like text file into a file containing all data, but only one gene per row.
    And additionally files the contain only 50 rows each.

    :param csv_path: path to the csv like text file
    """

    # read teh original data into a list of dictionary element with the same keys
    dict_list = []
    with open(csv_path, "rb") as csv_file:
        reader = csv.DictReader(csv_file, delimiter="\t")

        for line in reader:
            dict_list.append(line)

    # prepare the headline for the new file
    headline = "Category\tTerm\tCount\t%\tPValue\tGenes\tList Total\tPop Hits\tPop Total\t" + \
               "Fold Enrichment\tBonferroni\t" + "Benjamini\tFDR\tEnrichment\n"

    # create the output directory if it doesn't exist
    try:
        os.mkdir("output")
    except OSError as e:
        print "INFO: directory 'output' already exists, will probably overwrite the old data"

    # get the original filename from the csv_path
    if "/" in csv_path:
        file_name = csv_path.split("/")[-1].split(".")[0]
    elif "\\" in csv_path:
        file_name = csv_path.split("\\")[-1].split(".")[0]
    else:
        file_name = csv_path.split(".")[0]

    # create the file containing all data rows
    create_complete(dict_list, file_name, headline)

    # create the files containing only 50 rows per file
    create_parts(dict_list, file_name, headline)


def create_parts(dict_list, file_name, headline):
    """
    Creates files that contain only 50 data rows each. this with the data from dict_list.

    :param dict_list: a list of dictionaries containing the data that gets written
    :param file_name: the original name that will be the prefix for the splitted files
    :param headline: the headline that each file gets
    """

    # prepare the counters that we'll need for the file creation
    line_counter = 50
    file_counter = 0

    # prepare the consistent file object
    csv_file = None

    # for every dictionary entry in the list
    for dict_entry in dict_list:
        # for every gene
        for gene in dict_entry["Genes"].split(","):
            # if we have enough rows in one file
            if line_counter >= 50:
                # reset the line counter
                line_counter = 0

                # create a new csv_file and write the headline into it
                csv_file = open("output/" + file_name + "_part_" + str(file_counter) + ".txt", "w")
                csv_file.write(headline)

                # increase the file counter
                file_counter += 1

            # write a data entry into the file, ordered like the headline
            csv_file.write(dict_entry["Category"] + "\t" +
                           dict_entry["Term"] + "\t" +
                           dict_entry["Count"] + "\t" +
                           dict_entry["%"] + "\t" +
                           dict_entry["PValue"] + "\t " +
                           gene.strip() + "\t" +
                           dict_entry["List Total"] + "\t" +
                           dict_entry["Pop Hits"] + "\t" +
                           dict_entry["Pop Total"] + "\t" +
                           dict_entry["Fold Enrichment"] + "\t" +
                           dict_entry["Bonferroni"] + "\t" +
                           dict_entry["Benjamini"] + "\t" +
                           dict_entry["FDR"] + "\t" +
                           str(-math.log(float(dict_entry["PValue"]), 10)) + "\n")

            # increase the line counter
            line_counter += 1

    print "INFO: created", file_counter, "splitted files"


def create_complete(dict_list, file_name, headline):
    """
    Create the file that contains all data. This with the data from dict_list.

    :param dict_list: a list of dictionaries containing the data that gets written
    :param file_name: the original name that will be the postfix for file
    :param headline: the headline that each file gets
    """

    # open the output file
    with open("output/complete_" + file_name + ".txt", "w") as output_file:
        # add the headline to the top of the file
        output_file.write(
            headline)

        # for every data entry
        for dict_entry in dict_list:
            # for every gene
            for gene in dict_entry["Genes"].split(","):
                # write the data in the same order as it is in the headline
                output_file.write(dict_entry["Category"] + "\t" +
                                  dict_entry["Term"] + "\t" +
                                  dict_entry["Count"] + "\t" +
                                  dict_entry["%"] + "\t" +
                                  dict_entry["PValue"] + "\t " +
                                  gene.strip() + "\t" +
                                  dict_entry["List Total"] + "\t" +
                                  dict_entry["Pop Hits"] + "\t" +
                                  dict_entry["Pop Total"] + "\t" +
                                  dict_entry["Fold Enrichment"] + "\t" +
                                  dict_entry["Bonferroni"] + "\t" +
                                  dict_entry["Benjamini"] + "\t" +
                                  dict_entry["FDR"] + "\t" +
                                  str(-math.log(float(dict_entry["PValue"]), 10)) + "\n")

    print "INFO: created the complete data file"


def handle_cluster(file_path):
    """
    Handles the cluster like files. Splits the file into several files, each containing one cluster with the cluster
    and enrichment info as additional columns. Handles every lonely cluster file like a chart file afterwards

    :param file_path: a path to the cluster file
    """
    # create the output directory if it doesn't exist
    try:
        os.mkdir("output")
    except OSError as e:
        print "INFO: directory 'output' already exists, will probably overwrite the old data"

    # the paths to the created lonely cluster files gonna be stored
    output_files = []

    with open(file_path, "r") as cluster_file:
        # put one cluster per file
        lines_to_print = []
        cluster_num = 1

        # for line the every cluster file
        for line in cluster_file:
            # if the line is empty then we are at a clusters end
            if not line.strip():
                # convert first row to 2 columns
                first_row = lines_to_print[0].split("\t")
                first_row[0] = first_row[0].split(" ")
                first_row[1] = first_row[1].split(" ")
                first_row[1][2] = first_row[1][2].strip()

                # add the new columns to the headline
                lines_to_print[1] = lines_to_print[1].replace("\r\n", "\tAnnotation Cluster\tEnrichment Score\r\n")

                # add the data to every line
                for i in range(2, len(lines_to_print)):
                    lines_to_print[i] = lines_to_print[i].replace("\r\n", "\t" + first_row[0][2] + "\t" + first_row[1][
                        2] + "\r\n")

                # print the file and story the path to it
                output_path = "output/cluster_" + str(cluster_num) + ".txt"
                output_files.append(output_path)
                with open(output_path, "w") as output_file:
                    for i in range(1, len(lines_to_print)):
                        output_file.write(lines_to_print[i])

                # increase the cluster num and empty the lines to print array
                cluster_num += 1
                lines_to_print = []
            else:
                lines_to_print.append(line)

    # do the split chart algorithm for every newly created lonely cluster file
    for former_output_file in output_files:
        split_cluster_charts(former_output_file)


def split_cluster_charts(csv_path):
    """
    Split given csv like text file into a file containing all data, but only one gene per row.
    And additionally files the contain only 50 rows each.

    :param csv_path: path to the csv like text file
    """

    # read teh original data into a list of dictionary element with the same keys
    dict_list = []
    with open(csv_path, "rb") as csv_file:
        reader = csv.DictReader(csv_file, delimiter="\t")

        for line in reader:
            dict_list.append(line)

    # prepare the headline for the new file
    headline = "Category\tTerm\tCount\t%\tPValue\tGenes\tList Total\tPop Hits\tPop Total\t" + \
               "Fold Enrichment\tBonferroni\t" + "Benjamini\tFDR\tEnrichment\n"

    # create the output directory if it doesn't exist
    try:
        os.mkdir("output")
    except OSError as e:
        print "INFO: directory 'output' already exists, will probably overwrite the old data"

    # get the original filename from the csv_path
    if "/" in csv_path:
        file_name = csv_path.split("/")[-1].split(".")[0]
    elif "\\" in csv_path:
        file_name = csv_path.split("\\")[-1].split(".")[0]
    else:
        file_name = csv_path.split(".")[0]

    # create the file containing all data rows
    create_cluster_complete(dict_list, file_name, headline)

    # create the files containing only 50 rows per file
    create_cluster_parts(dict_list, file_name, headline)


def create_cluster_parts(dict_list, file_name, headline):
    """
    Creates files that contain only 50 data rows each. this with the data from dict_list.

    :param dict_list: a list of dictionaries containing the data that gets written
    :param file_name: the original name that will be the prefix for the splitted files
    :param headline: the headline that each file gets
    """

    # prepare the counters that we'll need for the file creation
    line_counter = 50
    file_counter = 0

    # prepare the consistent file object
    csv_file = None

    # for every dictionary entry in the list
    for dict_entry in dict_list:
        # for every gene
        for gene in dict_entry["Genes"].split(","):
            # if we have enough rows in one file
            if line_counter >= 50:
                # reset the line counter
                line_counter = 0

                # create a new csv_file and write the headline into it
                csv_file = open("output/" + file_name + "_part_" + str(file_counter) + ".txt", "w")
                csv_file.write(headline)

                # increase the file counter
                file_counter += 1

            # write a data entry into the file, ordered like the headline
            csv_file.write(dict_entry["Category"] + "\t" +
                           dict_entry["Term"] + "\t" +
                           dict_entry["Count"] + "\t" +
                           dict_entry["%"] + "\t" +
                           dict_entry["PValue"] + "\t " +
                           gene.strip() + "\t" +
                           dict_entry["List Total"] + "\t" +
                           dict_entry["Pop Hits"] + "\t" +
                           dict_entry["Pop Total"] + "\t" +
                           dict_entry["Fold Enrichment"] + "\t" +
                           dict_entry["Bonferroni"] + "\t" +
                           dict_entry["Benjamini"] + "\t" +
                           dict_entry["FDR"] + "\t" +
                           dict_entry["Annotation Cluster"] + "\t" +
                           dict_entry["Enrichment Score"] + "\n")

            # increase the line counter
            line_counter += 1

    print "INFO: created", file_counter, "splitted files"


def create_cluster_complete(dict_list, file_name, headline):
    """
    Create the file that contains all data. This with the data from dict_list.

    :param dict_list: a list of dictionaries containing the data that gets written
    :param file_name: the original name that will be the postfix for file
    :param headline: the headline that each file gets
    """

    # open the output file
    with open("output/complete_" + file_name + ".txt", "w") as output_file:
        # add the headline to the top of the file
        output_file.write(
            headline)

        # for every data entry
        for dict_entry in dict_list:
            # for every gene
            for gene in dict_entry["Genes"].split(","):
                # write the data in the same order as it is in the headline
                output_file.write(dict_entry["Category"] + "\t" +
                                  dict_entry["Term"] + "\t" +
                                  dict_entry["Count"] + "\t" +
                                  dict_entry["%"] + "\t" +
                                  dict_entry["PValue"] + "\t " +
                                  gene.strip() + "\t" +
                                  dict_entry["List Total"] + "\t" +
                                  dict_entry["Pop Hits"] + "\t" +
                                  dict_entry["Pop Total"] + "\t" +
                                  dict_entry["Fold Enrichment"] + "\t" +
                                  dict_entry["Bonferroni"] + "\t" +
                                  dict_entry["Benjamini"] + "\t" +
                                  dict_entry["FDR"] + "\t" +
                                  dict_entry["Annotation Cluster"] + "\t" +
                                  dict_entry["Enrichment Score"] + "\n")

    print "INFO: created the complete data file"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "ERROR: to less arguments"
        print "Usage: "
        print "python file_splitter.py [file_path] [chart|cluster]"
        exit(1)
    if sys.argv[2] == "chart":
        split_chart(sys.argv[1])
    elif sys.argv[2] == "cluster":
        handle_cluster(sys.argv[1])
    else:
        print "ERROR: " + sys.argv[2] + " is a wrong mode argument"
        print "Usage: "
        print "python file_splitter.py [file_path] [chart|cluster]"
        exit(1)