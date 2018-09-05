from fun_mooc.utils import *


class MOOCFormatter:
    @staticmethod
    def latex_to_mathjax(string):
        """
        Translates a string containing latex code to a mathjax-formatted string
        :param string: the laTex code (containing $$ and \begin{equation} etc)
        :return: the mathjax formatted string
        """
        if '$' in string:
            parts = string.split("$")
            string = ""
            for i, p in enumerate(parts):
                if i % 2 == 0:
                    string += p
                else:
                    string += '[mathjaxinline]' + p + '[/mathjaxinline]'
        string = string.replace(r"\begin{equation}", "[mathjax]")
        string = string.replace(r"\end{equation}", "[/mathjax]")
        return string

    @staticmethod
    def simple_text(text, inline=False):
        if len(text) > 0:
            if inline:
                return '<p style="display:inline">' + text + '</p>'
            else:
                return '<p>' + text + '</p>'
        return ""

    @staticmethod
    def insert_image(name):
        return '\t<center><image src="static/' + name + '"/></center>\n'

    @staticmethod
    def qcm(answers, corrects):
        text = ""
        if len(corrects) > 1:
            text += "<p><i> (plusieurs réponses possibles)</i></p>\n"
            text += "<choiceresponse>\n\t<checkboxgroup>\n"
            for j in range(len(answers)):
                if j in corrects:
                    text += '\t<choice correct="true">' + answers[j] + '</choice>\n'
                else:
                    text += '\t<choice correct="false">' + answers[j] + '</choice>\n'
            text += "\t</checkboxgroup>\n</choiceresponse>\n\n"
        else:
            text += '\n<multiplechoiceresponse>\n\t<choicegroup type="MultipleChoice">\n'
            for j in range(len(answers)):
                if j in corrects:
                    text += '\t<choice correct="true">' + answers[j] + '</choice>\n'
                else:
                    text += '\t<choice correct="false">' + answers[j] + '</choice>\n'
            text += "\t</choicegroup>\n</multiplechoiceresponse>\n\n"
        return text

    @staticmethod
    def numerical_input(answer, inline_question=None, inline=False):
        text = ""
        # reads it as a list ?
        answer = MOOCUtils.string_to_list(answer)

        if isinstance(answer, list):
            l = answer
            answer = "["
            for i in l[:-1]:
                answer += str(i) + ', '
            answer += str(l[-1]) + ']'
        if inline:
            text += '<numericalresponse answer="' + answer + '">\n'
            if inline_question is not None:
                text += '<p style="display:inline"> ' + inline_question + ' </p>'
            text += '<textline label="inline_input" inline="1"/>\n</stringresponse>'
        else:
            text += '<stringresponse answer="' + answer + '">\n'
            text += '\t<textline label="outline_input"/>\n</stringresponse>'
        return text

    @staticmethod
    def string_input(answer, inline_question=None, inline=False):
        additional = []
        text = ""

        # reads it as a list ?
        answer = MOOCUtils.string_to_list(answer)

        if isinstance(answer, list):
            additional = answer[1:]
            answer = answer[0]
        if inline:
            text += '<stringresponse answer="' + answer + '">\n'
            for a in additional:
                text += '\t<additional_answer answer="' + a + '"></additional_answer>\n'
            text += '\t'
            if inline_question is not None:
                text += '<p style="display:inline"> ' + inline_question + ' </p>'
            text += '<textline label="inline_input" inline="1"/>\n</stringresponse>'
        else:
            text += '<stringresponse answer="' + answer + '">\n'
            for a in additional:
                text += '\t<additional_answer answer="' + a + '"></additional_answer>\n'
            text += '\t<textline label="outline_input"/>\n</stringresponse>'
        return text

    @staticmethod
    def choice(choices, correct=None, inline=False):
        if not inline:
            text = '<optionresponse>\n\t<optioninput options="('
        else:
            text = '<optioninput options="('

        # reads it as a list ?
        choices = MOOCUtils.string_to_list(choices)

        # if the correct answer is not fond
        if correct is None:
            for i_c in range(len(choices)):
                c = choices[i_c].strip()
                if c.startswith("*"):
                    c = c.replace("*", "")
                    correct = c
                choices[i_c] = c
        for c in choices:
            text += "'" + c + "'"
            if not c == choices[-1]:
                text += ","
        if inline:
            text += ')" correct="' + correct + '" inline="1"></optioninput>\n'
        else:
            text += ')" correct="' + correct + '"></optioninput>\n</optionresponse>\n'
        return text