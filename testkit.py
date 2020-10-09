import commands

class Testkit:
    def __init__(self):
        self.actuator = commands.Actuator()
        self.module_tests = self.get_module_tests()
        self.run_module_tests()
        self.update_readme()


    def get_module_tests(self):
        """ Tests are written as 1 line commands in a .txt """
        lines = []
        with open("tests.txt", "r+") as file:
            for line in file.readlines():
                lines.append(line.replace("\n", ""))
        return lines


    def run_module_tests(self):
        nick = "Bob"
        self.module_test_loop(nick, True)


    def module_test_loop(self, nick, pm):
        num = 1
        for test in self.module_tests:
            print("\nTEST {} <{}>".format(num, test))
            try:
                result = self.actuator.command(test, nick, pm)
                print(result)

            except Exception as e:
                print("TEST FAILED! ( {} - <{}> )".format(num, test))
                print("{}\n".format(e, "\n"))
            num += 1

    def update_readme(self):
        """This class automatically updates the readme to reflect added modules that may not be in the readme yet"""
        command_examples = self.actuator.get_examples()
        file_name = "README.md"
        # contents of the readme
        contents = ""
        # counts of total lines in file
        file_lines_count = 0
        # index of the last command found in the readme
        last_command_line_index = 0

        with open(file_name, 'r') as readme_in:
            for line in readme_in:
                # if the line is a command/example
                if "**!" in line:
                    # find indexes of the !command in this line
                    start = line.find(" **") + len(" **")
                    end = line.find("-") - len("** ")
                    # Removes markdown formatting and searches if the command found in the readme is in examples
                    if (line[start:end] + line[end+len("**"):len(line) - 1]) in command_examples:
                        # removes  command from the list so that only commands that arent added to the readme remain
                        command_examples.remove(line[start:end] + line[end+len("**"):len(line) - 1])
                        # saves the last line number that contains a command/example
                        last_command_line_index = file_lines_count
                file_lines_count += 1
            # go to the first line of the file and save the contents of the file
            readme_in.seek(0)
            contents = readme_in.readlines()

        # add new commands and examples to the readme
        for example in command_examples:
            end = example.find("-") - len(" ")
            contents.insert(last_command_line_index + 1, "* #### **" + example[:end] + "**" + example[end:] + "\n")
            last_command_line_index += 1

        # write to the file
        with open(file_name, "w") as readme_out:
            contents = "".join(contents)
            readme_out.write(contents)
            readme_out.close()

test = Testkit()