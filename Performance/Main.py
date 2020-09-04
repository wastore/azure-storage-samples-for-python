import time
import pandas as pd

from azure.storage.blob import BlobServiceClient

def main():
    connection_string = ""
    container_name = "yay"
    excel_name = "single_var.xlsx"
    num_upload_per_run = 100
    # TODO: testing files were created using fsutil file createnew in cmd. Need to create files before code can work
    file_list = ["testing128", "testing256", "testing384"]
    max_concurrency_list = [1, 2, 3, 4, 5, 10, 15, 20]
    mb_size_list = [1*1024*1024, 16*1024*1024, 32*1024*1024, 48*1024*1024, 56*1024*1024]
    # mb_size_list = [64*1024*1024, 72*1024*1024, 80*1024*1024, 88*1024*1024, 96*1024*1024]

    # Setting up clients
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_container_client = blob_service_client.get_container_client(container_name)

    # Testing based on keeping params constant
    data_concurrency = {}
    data_max_block = {}
    data_min_threshold = {}
    for file in file_list:
        data_concurrency[file] = testing_max_concurrency(blob_container_client, num_upload_per_run, file, max_concurrency_list)
        data_max_block[file] = testing_max_block_size(connection_string, container_name, num_upload_per_run, file, mb_size_list)
        data_min_threshold[file] = testing_min_large_block_upload_threshold(connection_string, container_name, num_upload_per_run, file, mb_size_list)


    # Writing data to Excel sheet, each col is a different file, and each sheet varies a different parameter
    df_concurrency = pd.DataFrame(data=data_concurrency, index=max_concurrency_list)
    df_block = pd.DataFrame(data=data_max_block, index=mb_size_list)
    df_thresh = pd.DataFrame(data=data_min_threshold, index=mb_size_list)

    writer = pd.ExcelWriter(excel_name, engine="xlsxwriter")
    df_concurrency.to_excel(writer, sheet_name="vary_concurrency")
    df_block.to_excel(writer, sheet_name="vary_max_block")
    df_thresh.to_excel(writer, sheet_name="vary_min_thresh")

    writer.save()

    # Testing based on combining params
    testing_combined_params(connection_string, container_name, num_upload_per_run, file_list[0], max_concurrency_list, mb_size_list, mb_size_list)

    print("Finished compiling outputs to csv files")


def testing_max_concurrency(blob_container_client, num_upload_per_run, file, max_concurrency_list):
    times = []
    print("Checking file " + file)
    optimal_concurrency = 0
    optimal_concurrency_time = None
    for max_concurrency in max_concurrency_list:
        print("Concurrency: "+ str(max_concurrency))
        avg_time = upload_many_blobs(num_upload_per_run, blob_container_client, file, max_concurrency) / num_upload_per_run
        print("Time: " + str(avg_time))
        times.append(avg_time)
        if optimal_concurrency == 0 or optimal_concurrency_time > avg_time:
            optimal_concurrency = max_concurrency
            optimal_concurrency_time = avg_time
    print("Best concurrency for file " + file + ": " + str(optimal_concurrency) + " at time of: " + str(optimal_concurrency_time))
    return times


def testing_max_block_size(connection_string, container_name, num_upload_per_run, file, max_block_list):
    times = []
    print("Checking file " + file)
    optimal_size = 0
    optimal_size_time = None
    for max_block in max_block_list:
        print("Testing max_block_size of: " + str(max_block))
        blob_service_client = BlobServiceClient.from_connection_string(connection_string, max_block_size=max_block)
        blob_container_client = blob_service_client.get_container_client(container_name)
        avg_time = upload_many_blobs(num_upload_per_run, blob_container_client, file, 1) / num_upload_per_run
        times.append(avg_time)
        print("Time: " + str(avg_time))
        if optimal_size == 0 or optimal_size_time > avg_time:
            optimal_size = max_block
            optimal_size_time = avg_time
    print("Best max_block for file: " + str(optimal_size) + " at time of: " + str(optimal_size_time))
    return times


def testing_min_large_block_upload_threshold(connection_string, container_name, num_upload_per_run, file, min_thresh_list):
    times = []
    print("Checking file " + file)
    optimal_size = 0
    optimal_size_time = None
    for min_thresh in min_thresh_list:
        print("Testing min_large_block_upload_threshold of: " + str(min_thresh))
        blob_service_client = BlobServiceClient.from_connection_string(connection_string, min_large_block_upload_threshold=min_thresh)
        blob_container_client = blob_service_client.get_container_client(container_name)
        avg_time = upload_many_blobs(num_upload_per_run, blob_container_client, file, 1) / num_upload_per_run
        times.append(avg_time)
        print("Time: " + str(avg_time))
        if optimal_size == 0 or optimal_size_time > avg_time:
            optimal_size = min_thresh
            optimal_size_time = avg_time
    print("Best min_large_block_upload_threshold for file: " + str(optimal_size) + " at time of: " + str(optimal_size_time))
    return times

# Saves file with rows as values of concurrency, cols as block size, and sheet number as min thresh
def testing_combined_params(connection_string, container_name, num_upload_per_run, file, max_concurrency_list, max_block_list, min_thresh_list):
    print("Checking file " + file)
    writer = pd.ExcelWriter("combined_var.xlsx", engine="xlsxwriter")
    optimal_params = []
    optimal_time = None
    for min_thresh in min_thresh_list:
        data = {}
        for max_block in max_block_list:
            times = []
            for max_concurrency in max_concurrency_list:
                print("Params (max_concurrency, max_block, min_thresh): " + str([max_concurrency, max_block, min_thresh]))
                blob_service_client = BlobServiceClient.from_connection_string(connection_string,
                                                                               max_block_size=max_block,
                                                                               min_large_block_upload_threshold=min_thresh)
                blob_container_client = blob_service_client.get_container_client(container_name)
                avg_time = upload_many_blobs(num_upload_per_run, blob_container_client, file, 1) / num_upload_per_run
                times.append(avg_time)
                print("Time: " + str(avg_time))
                if optimal_params == [] or optimal_time > avg_time:
                    optimal_params = [max_concurrency, max_block, min_thresh]
                    optimal_time = avg_time
            data["max_block_"+ str(max_block)] = times
            df = pd.DataFrame(data=data, index=["max_concurrency_" + str(s) for s in max_concurrency_list])
        df.to_excel(writer, sheet_name="min_thresh_" + str(min_thresh))
    print("Optimal params (ordered in concurrency, max_block, min_thresh): " + str(optimal_params) + " at time: " + str(optimal_time))
    writer.save()


"""
Uploads a large number of blobs and returns total amount of time it takes for upload to complete
"""
def upload_many_blobs(num_uploads, blob_container_client, blob_name, max_concurrency):
    total_time = 0
    for i in range(num_uploads):
        with open(blob_name, "rb") as blob_content:
            numbered_blob_name = str(i) + blob_name + "m" + str(max_concurrency)
            start = time.time()
            blob_container_client.upload_blob(numbered_blob_name, blob_content, max_concurrency=max_concurrency, overwrite=True)
            end = time.time()
            total_time += (end - start)
            blob_client = blob_container_client.get_blob_client(blob=numbered_blob_name)
            blob_client.delete_blob()
    return total_time


if __name__ == '__main__':
    main()
