from time import sleep

reference = None


def stat():
    f = open("/proc/stat", "r")
    data = [int(x) for x in f.readline().split()[1:]]
    f.close()
    return data

def relative(data):
    global reference
    if not reference:
        reference = data
    return [d-r for r,d in zip(reference,data)]

if __name__ == "__main__":
    while True:
        sleep(1)
        print " ".join([str(x) for x in relative(stat())])
            
                

   
