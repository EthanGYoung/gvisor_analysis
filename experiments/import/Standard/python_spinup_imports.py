import time

if __name__== "__main__":
    #imports ends
    import_start_time = time.time()
    #imports ends
    import_end_time = time.time()
    import_elapsed_time = round((import_end_time - import_start_time)*1000,6)
    print("LOG_OUTPUT: It took %.6fms for standard function calls to execute."%import_elapsed_time)
    pass
