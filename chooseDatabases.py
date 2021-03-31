def getDatabases(rollNumber):
    suffix = []
    for x in rollNumber:
        for y in rollNumber:
            suffix.append(int((x*y) % 5))

    databases = ["(A-100.csv,B-100-3-",
    "(A-100.csv,B-100-5-",
    "(A-100.csv,B-100-10-",
    "(A-1000.csv,B-1000-5-",
    "(A-1000.csv,B-1000-10-",
    "(A-1000.csv,B-1000-50-",
    "(A-10000.csv,B-10000-5-",
    "(A-10000.csv,B-10000-50-",
    "(A-10000.csv,B-10000-500-"]

    addExtension = ".csv)"


    for i in range(len(suffix)):
        databases[i] = databases[i] + str(suffix[i]) + addExtension

    return databases
