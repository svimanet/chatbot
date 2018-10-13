import os

def refactor(directory, oldWord, newWord, numOfReplacements=0, numOfFiles=0, files=[]):
    dirs = os.listdir(directory)
    if len(dirs)==0:
        return numOfReplacements, numOfFiles, files
    else:
        for dirFile in dirs:
            fullName = directory + dirFile
            replaceOccured = True
            if os.path.isfile(fullName):
                newLines = []
                with open(fullName, "r") as inFile:
                    for line in inFile:
                        if oldWord in line:
                            line = line.replace(oldWord, newWord)
                            numOfReplacements += 1
                            if replaceOccured:
                                numOfFiles += 1
                                files.append(os.path.basename(fullName))
                                replaceOccured = False
                        newLines.append(line)

                with open(fullName, "w") as outFile:
                    for line in newLines:
                        outFile.write(line)
            else:
                refactor(directory + dirFile, oldWord, newWord, numOfReplacements, numOfFiles, files)
    return (numOfReplacements, numOfFiles, files)

def refactorInfo(result):
    numOfReplacements, numOfFiles, files = result
    replacementInfoString = "Total replacements: "
    fileInfoString = "Total files modified: "
    fileString = "Files: "
    rightPadding = 15
    print(replacementInfoString + str(numOfReplacements).rjust(len(fileInfoString) - rightPadding," "))
    print(fileInfoString + str(numOfFiles).rjust(len(replacementInfoString) - rightPadding, " "))
    print(fileString)
    for f in files:
        print("- ", end="")
        print(f)
