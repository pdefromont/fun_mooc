from fun_mooc.mooc_formatter import *


class MOOC:
    def __init__(self, name=None, **kwargs):
        """
        Creates an instance of MOOC.
        :param name: the name of the MOOC. If this MOOC does not exists, it will ask you to enter a new name.
        :param kwargs: the keywords that can be passed to the `create(...)` call.
        """
        if name is None:
            name = input("Enter Mooc name : ")
        self.name = name
        self.current_path = os.path.abspath(".").replace("\\", "/")
        print(self.current_path)
        self.params = None
        self.path = self._get_write_directory() + "/MOOC_" + self.name
        print(self.path)
        self.folders = {"css": self.path + "/css/",
                        "exercices": self.path + "/exercices/",
                        "evals": self.path + "/evals/",
                        "latex": self.path + "/latex/",
                        "other": self.path + "/other/",
                        "inputs": self.path + "/inputs/"
                        }

        if not MOOCUtils.folder_exists(self.path):
            res = input("\nThis MOOC does not exists ! Do you want to create it ? (y/n) ")
            if res == "y":
                self.create(**kwargs)
        else:
            self._load_params()
            print("MOOC", self.name, "correctly loaded.")

    @staticmethod
    def _get_write_directory():
        try:
            paths = open("_path", "r", encoding="utf8")
            c = paths.read()
            return c.strip().replace('\\', '/')
        except FileNotFoundError:
            path = os.path.abspath(input("\nEnter the root path where you want to create your MOOCs :")).replace('\\', '/')
            f = open("_path", "w", encoding="utf8")
            f.write(path)
            f.close()
            return path

    def _load_params(self):
        self.params = MOOCUtils.read_ini_file(self.path + "/mooc_parameters.ini", cast=False)

    def set_param(self, name, value=None):
        """
        Sets a new value for a parameter and updates the css file
        :param name: the name of the paramter
        :param value: the new value. If it is not specified, it will be asked
        """
        file_name = self.path + "/mooc_parameters.ini"
        if value is None:
            value = str(input("\tEnter the value for '" + name + "' : "))

        self._load_params()
        try:
            old_content = MOOCUtils.get_file_content(file_name)
            if name in self.params:
                old_content = old_content.replace(name + "=" + self.params[name], name + "=" + str(value))
            else:
                old_content += name + "=" + str(value) + "\n"

            MOOCUtils.set_file_content(file_name, old_content)
            self.params[name] = value

            self._update_css()
        except FileNotFoundError:
            return None

    def create(self, **kwargs):
        """
        Creates a new MOOC. It creates the various folders, the .css file and sets the global variables.
        :param kwargs: optionally can be one of the following arguments :
            - global_background_color
            - latex_summary_background_color
            - title_border_color
            - qcm_color
            - eval_color
            - left_delimiter (set to '((' )
            - right_delimiter (set to '))' )
            If they are not specified, they will be asked directly
        """
        print("=" * 30 + "\nCreating MOOC :" + self.name + "\n" + "=" * 30 + "\n\n")

        # folders
        self._create_folders()
        # css file
        self._create_css()
        # .ini file
        f = open(self.path + "/mooc_parameters.ini", "w", encoding="utf8")
        f.write("; This file is generated automatically. You can however edit it manually.\n\n[MOOC parameters]\n")
        f.close()

        # setting various elements:
        self.set_param("left_delimiter", kwargs.get("left_delimiter", '(('))
        self.set_param("right_delimiter", kwargs.get("right_delimiter", '))'))
        for key in ["global_background_color", "latex_summary_background_color", "title_border_color"]:
            self.set_param(key, kwargs.get(key, None))

        # default boxes
        self.create_css_environment("qcm",
                                    color=kwargs.get("qcm_color", None),
                                    header="Exercice de compréhension")
        self.create_css_environment("eval",
                                    color=kwargs.get("eval_color", None),
                                    header="Exercice d'évaluation")

        print("\n\t[Warning : the css have been updated. Please upload it on the FUN plateform]")
        self._load_params()

    def _create_folders(self):
        """
        create various folders
        """
        print("Creating folders ...", end="")
        MOOCUtils.create_folder_if_not_exists(self.path)
        for f in self.folders:
            MOOCUtils.create_folder_if_not_exists(self.folders[f][:-1])
        print("done")

    def _create_css(self):
        """
        Creates the .css and the .ini file
        """
        if not MOOCUtils.file_exists(self.path + "/css/" + self.name + "_template.txt"):
            print("Creating the template css file ...", end="")

            # copy template_file
            content = MOOCUtils.get_file_content(self.current_path + "/original_css/obspm_mooc_template.css")
            if content is None:
                print("File obspm_mooc_template.css not found in ", self.current_path + "/original_css/obspm_mooc_template.css")
                return False

            MOOCUtils.set_file_content(self.path + "/css/" + self.name + "_template.txt", content)
            print("done")

        if not MOOCUtils.file_exists(self.path + "/mooc_parameters.ini"):
            print("Creating ini file ...", end="")
            MOOCUtils.set_file_content(self.path + "/mooc_parameters.ini", "")
            print("done")

        if not MOOCUtils.file_exists(self.path + "/css/" + self.name + ".css"):
            print("Creating the css file ...", end="")

            # copy template_file
            content = MOOCUtils.get_file_content(self.current_path + "/original_css/obspm_mooc_template.css")
            if content is None:
                print("File obspm_mooc_template.css not found in ", self.current_path + "/original_css/obspm_mooc_template.css")
                return False

            self._set_css_content(content)
            print("done")

    def set_css_color(self, name, color=None):
        """
        Sets the color whose key is 'name' to 'color'
        :param name: the key of the box (e.g. 'global_background_color')
        :param color: an hexadecimal color
        :return: the color.
        """
        if color is None:
            color = str(input("Enter the color (hexadecimal format : '#xxxx') for the box " + name + " :"))

        # setting the new parameter
        self.set_param(name, color)

        # nox update the css file
        self._update_css()

        print("\n\t[Warning : the css have been updated. Please upload it on the FUN plateform]")
        return color

    def _update_css(self):
        """
        updates the css file from parameters and xxx_template.txt
        """
        self._load_params()

        content = self._get_css_content()
        for key in self.params:
            # print("replacing ", key.strip(), "=>", self.params[key])
            content = content.replace(key.strip(), self.params[key])
        self._set_css_content(content)

    def _get_css_content(self, as_line=False):
        """
        Get the content of the css file.
        :param as_line: if True, returns the content as a list of lines
        :return: the .css content
        """
        return MOOCUtils.get_file_content(self.folders["css"] + self.name + "_template.txt", as_line=as_line)

    def _set_css_content(self, new_content):
        """
        Sets the content of the css file.
        :param new_content: the string that contains the new content
        :return: True if the file exists, False else
        """
        return MOOCUtils.set_file_content(self.folders["css"] + self.name + ".css", new_content)

    def create_css_environment(self, title, color=None, header=None, lateral_bar=True, paragraph_in_bold=False, shadow=True):
        """
        Creates a custom css environment that behaves like a box
        :param title: the name of the class
        :param color: the color (hexadecimal)
        :param header: the text that appears in the header
        :param lateral_bar: displays a lateral if True
        :param paragraph_in_bold: True if the paragraph should be in bold.
        :param shadow: True if the box has a shadow
        :return:
        """
        if color is None:
            color = input("Enter the color (hexadecimal format : '#xxxx') for the box " + title + " :")
        # first, sets the parameters
        self.set_param(title + '_color', color)

        file_content = "\n\n/* custom box : " + title + " */\n.obspm_mooc_" + title + "{"
        if lateral_bar:
            file_content += "\n\tborder-left: 10px solid " + title + "_color;"
        file_content += "\n\tbackground-color: global_background_color;\n\tpadding:10px;\n\tpadding-top:5px;\n\tpadding-bottom:1px;"
        if shadow:
            file_content += "\n\tbox-shadow: 5px 5px 10px #9b9b9b;"
        file_content += "\n}\n"

        if header is not None:
            file_content += ".obspm_mooc_" + title + ":before{\n\tcolor:" + title + '_color;\n\tfont-size:120%;\n\tfont-weight: bold;\n\tcontent:"' + header + '"\n}\n'

        file_content += ".obspm_mooc_" + title + " p{\n\tpadding-top:10px;\n\ttext-align: justify;\n"
        if paragraph_in_bold:
            file_content += "\tfont-weight: bold;\n"
        file_content += "}\n\n"

        old_content = self._get_css_content()
        old_content = old_content.replace("</style>", file_content + "</style>")
        MOOCUtils.set_file_content(self.folders["css"] + self.name + "_template.txt", old_content)

        # now update the css file
        self._update_css()

        print("\n\t[Warning : the css have been updated. Please upload it on the FUN plateform]")
        return old_content

    def generate_text(self, file_name, output_name=None, environment="default"):
        """
        Generates a .html file correctly-formated for FUN with the desired environement. The ouput file
        :param file_name: the path of the input file. This file can contains laTex code.
        :param output_name: the name of the output file. If not specified, the file is called as the input. The ouptut file is placed in the /other/ folder.
        :param environment: the desired environment (box). If not specified, it is set to `default`
        :return: True if the file was correctly written, False else.
        """
        try:
            f = open(self.folders["inputs"] + file_name, "r", encoding="utf8")
            lines = f.readlines()
            f.close()

            print("Reading file ", file_name)

            content = '<LINK rel="stylesheet" type="text/css" href="/static/' + self.name + '.css">\n<div class="obspm_mooc_' + environment + '">\n'

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    content += "\n<p>" + MOOCFormatter.latex_to_mathjax(line).strip() + "</p>"

            content += "\n</div></LINk>"

            print("Source correctly read. Generating file", self.path + "/other/" + file_name.split(".")[0] + ".html")
            output_name = output_name if output_name is not None else file_name.split('/')[-1].split(".")[0]
            f = open(self.folders["other"] + output_name + ".html", "w", encoding="utf8")
            f.write(content)
            f.close()

        except FileNotFoundError:
            print("Error : the file", file_name, "does not exists !")

    def generate_latex_page(self, file_name, output_name=None):
        """
        Translates a .tex file to a correctly-formated html file for FUN.
        :param file_name: the path of the input .tex file. This file can contains laTex code.
        :param output_name: the name of the output file. If not specified, the file is called as the input. The ouptut file is placed in the /latex/ folder.
        :return: True if the file was correctly written, False else.
        """
        print("Formating file", file_name)

        file_name = file_name if file_name.endswith(".tex") else file_name + ".tex"
        end_file = output_name if output_name is not None else file_name.split('/')[-1].split(".")[0] + ".html"

        bashCommand = "pandoc " + self.folders["inputs"] + file_name + " -s --mathjax -o " + self.path + "/latex/" + end_file
        os.system(bashCommand)

        # modifying file
        file = open(self.path + "/latex/" + end_file, "r", encoding="utf8")
        file_content = file.read()
        file.close()

        # textnormal problem
        file_content = file_content.replace("textnormal", "text")

        # images
        im_positions = MOOCUtils.find_all(file_content, "<img src=")
        print("\nfinding images ...")
        for pos in im_positions:
            im_name = file_content[pos:].split('"')[1]
            file_content = file_content.replace('"' + im_name + '"', '"/static/' + im_name + '.png"')
            print("replacing : ", '"' + im_name + '"', "=>", '"/static/' + im_name + '.png"')
            print("(warning : file ", '"/static/' + im_name + '.png" should exist)')

        # captions in bold
        print("\nfinding captions ...")
        parts = file_content.split('<p class="caption">')
        for part in parts[1:]:
            label = part.split("<")[0]
            file_content = file_content.replace(label, "<b>" + label + "</b>")
            print("replacing : ", label, "=>", "<b>" + label + "</b>")

        parts = file_content.split('<caption>')
        for part in parts[1:]:
            label = part.split("<")[0]
            file_content = file_content.replace(label, "<b>" + label + "</b>")
            print("replacing : ", label, "=>", "<b>" + label + "</b>")

        # summary
        print("\nlooking for summary")
        texfile = open(self.path + "/latex/" + end_file, encoding="utf8")
        tex_file_content = texfile.read()
        texfile.close()

        # global style
        parts = file_content.split("<body>")
        file_content = parts[
                           0] + "<body>" + "\n" + '<LINK rel="stylesheet" type="text/css" href="/static/' + self.name + '.css">\n<div class="obspm_mooc_latex">\n' + \
                       parts[1]

        summary_key = r"\fbox{\parbox{\textwidth}{\textbf{Résumé} : "
        if summary_key in tex_file_content:
            summary = tex_file_content.split(summary_key)[1]
            summary = summary.split("}}")[0].strip()

            print("\nsummary founded !")

            # temp_file
            temp_tex = open("temp.tex", "w", encoding="utf8")
            temp_tex.write(summary)
            temp_tex.close()

            os.system("pandoc temp.tex -s --mathjax -o temp.html")

            temp_tex = open("temp.html", "r", encoding="utf8")
            summary = temp_tex.read().split("<body>")[1].split("</body>")[0]
            temp_tex.close()

            os.remove("temp.tex")
            os.remove("temp.html")

            if '<div class="footnotes">' in file_content:
                print("\nthis file contains footnotes")
                first_part = file_content.split('<div class="footnotes">')
                file_content = first_part[
                                   0] + '\n<div class="obspm_mooc_latex_summary">' + summary + '</div></div>\n<div class="footnotes">' + \
                               first_part[1]
            else:
                first_part = file_content.split('</body>')
                file_content = first_part[
                                   0] + '\n<div class="obspm_mooc_latex_summary">' + summary + "</div></div>\n</body>" + \
                               first_part[1]
        else:
            print("no summary in this file")
            if '<div class="footnotes">' in file_content:
                print("\nthis file contains footnotes")
                first_part = file_content.split('<div class="footnotes">')
                file_content = first_part[0] + '</div><div class="footnotes">' + first_part[1]
            else:
                first_part = file_content.split('</body>')
                file_content = first_part[0] + '\n<div>\n</body>' + first_part[1]

        print("saving final file !")
        new_file = open(self.folders["latex"] + end_file, "w", encoding="utf8")
        new_file.write(file_content)
        new_file.close()

    def generate_exercice(self, source_file, output_name=None, is_evaluation=False, custom_environment=None):
        """
        Generates a .html file correctly-formated for FUN with the desired environement.
        :param environment: the desired environment (box). If not specified, it is set to `default`
        :param source_file: the path of the input file. This file can contains laTex code.
        :param output_name: the name of the output file. If not specified, the file is called as the input. The ouptut file is placed in the /evals/ folder if `is_evaluation=True` else in  /exercices/
        :param is_evaluation: Specifies if it is a evaluation or not. If `True`, the output file is saved in the /evals/ folder and the environment used is : obspm_mooc_eval
        :param custom_environment: You can also specify a custom environment.
        """
        try:
            f = open(self.folders["inputs"] + source_file, "r", encoding="utf8")
            lines = f.readlines()
            f.close()

            print("Reading file ", source_file)

            if is_evaluation:
                global_text = '<problem>\n<LINK rel="stylesheet" type="text/css" href="/static/' + self.name + '.css">\n<div class="obspm_mooc_eval">\n'
            elif custom_environment is not None:
                global_text = '<problem>\n<LINK rel="stylesheet" type="text/css" href="/static/' + self.name + '.css">\n<problem>\n<div class="obspm_mooc_' + custom_environment + '>\n'
            else:
                global_text ='<problem>\n<LINK rel="stylesheet" type="text/css" href="/static/' + self.name + '.css">\n<problem>\n<div class="obspm_mooc_qcm">\n'

            keywords = ["QCM", "IMAGE", "CHOICE", "INPUT"]
            current_env = ""
            current_exo = 0
            is_mathjax= False
            qcm_a = []
            qcm_c = []
            for line in lines:
                line = MOOCFormatter.latex_to_mathjax(line.strip())
                if len(line) > 0:
                    if line.startswith(tuple(keywords)):
                        current_env = line.split(":")[0]

                        # generate previous qcm ?
                        if len(qcm_a) > 0:
                            global_text += MOOCFormatter.qcm(qcm_a, qcm_c)
                        qcm_a.clear()
                        qcm_c.clear()

                        # new exo ?
                        current_exo += 1
                        global_text += MOOCFormatter.simple_text('<b>Exercice ' + str(current_exo) + ' : </b>')
                        print("New exercice recognized (number", current_exo, ") : ", current_env)

                        question = line.split(":")[1].strip()

                        # check if the answer is inline :
                        if self.params["left_delimiter"] in question and current_env == "CHOICE":
                            text, env = self._read_brackets_env(question)

                            global_text += "<optionresponse>\n"

                            global_text += MOOCFormatter.simple_text(text.pop(0), inline=True)
                            for i in range(len(env)):
                                global_text += MOOCFormatter.choice(env[i], inline=True)
                                global_text += MOOCFormatter.simple_text(text[i], inline=True)
                            global_text += "\n</optionresponse>\n"
                        else:
                            if current_env == "IMAGE":
                                global_text += MOOCFormatter.insert_image(question)
                            else:
                                global_text += MOOCFormatter.simple_text(question, inline=False) + "\n"

                    elif line.startswith("-") and current_env == "QCM":
                        if line[1] == "A":
                            # maybe change to "*" ?
                            qcm_a.append(line.replace("-A", "").strip())
                            qcm_c.append(len(qcm_a[-1]) - 1)
                        else:
                            qcm_a.append(line[1:].strip())
                    elif line == '[mathjax]':
                        global_text += '[mathjax]\n'
                        is_mathjax = True
                    elif line == '[/mathjax]':
                        global_text += '[/mathjax]\n'
                        is_mathjax = False
                    else:
                        if is_mathjax:
                            global_text += "\t" + line + "\n"
                        else:
                            if self.params["left_delimiter"] in line:
                                text, env = self._read_brackets_env(line)
                                global_text += MOOCFormatter.simple_text(text.pop(0))
                                for i in range(len(env)):
                                    if current_env == "CHOICE":
                                        global_text += MOOCFormatter.choice(env[i])
                                        global_text += MOOCFormatter.simple_text(text[i])
                                    elif current_env == "INPUT":
                                        global_text += MOOCFormatter.string_input(env[i])
                                        global_text += MOOCFormatter.simple_text(text[i])
                                global_text += "\n"
                            else:
                                global_text += MOOCFormatter.simple_text(line) + "\n"

            # generate previous qcm ?
            if len(qcm_a) > 0:
                global_text += MOOCFormatter.qcm(qcm_a, qcm_c)
            qcm_a.clear()
            qcm_c.clear()

            global_text += "\n\t</div></LINK>\n</problem>"

            output_name = output_name if output_name is not None else source_file.split('/')[-1].split(".")[0]
            name = self.folders["exercices"] + output_name + ".html"
            if is_evaluation:
                name = self.folders["evals"] + output_name + ".html"

            print("File correctly read. Saving it as ", name)
            f = open(name, "w", encoding="utf8")
            print(f)
            f.close()

        except FileNotFoundError:
            print("Error : the file", source_file, "does not exists !")

    def _read_brackets_env(self, line):
        return MOOCUtils.extract_text(line,
                                      self.params["left_delimiter"],
                                      self.params["right_delimiter"])


if __name__ == '__main__':
    m = MOOC()

