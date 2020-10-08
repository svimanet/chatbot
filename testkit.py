import commands

class Testkit:
    def __init__(self):
        self.actuator = commands.Actuator()
        #self.module_tests = self.get_module_tests()
        #self.run_module_tests()
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
        file_name = "README.md"
        # TO DO: Complete this, updates readme from list returned with get_examples
        examples = self.actuator.get_examples()
        last_example = ""
        with open(file_name) as readme_in:
            for line in readme_in:
                if "**!" in line:
                    start = line.find(" **") + len(" **")
                    end = line.find("-") - len("** ")
                    if (line[start:end] + line[end+len("**"):len(line) -1]) in examples:
                        print(line[start:end] + line[end+len("**"):len(line)])
                    #print(line[start:end] + line[end + len("**"):len(line) - 1])
                    #print(examples[12])




        #examples = self.actuator.get_examples()
        #print(examples)


test = Testkit()