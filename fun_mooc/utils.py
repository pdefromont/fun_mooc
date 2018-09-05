#!/usr/bin/python
import argparse
import sys
import os
from pathlib import Path


class MOOCUtils:
    """
    A utility class for fun_MOOC
    """
    @staticmethod
    def find_all(string, to_find):
        l = []
        last_pos = -1
        while True:
            last_pos = string.find(to_find, last_pos + 1)
            if last_pos > 0:
                l.append(last_pos)
            else:
                break
        return l

    @staticmethod
    def get_file_content(file_path, as_line=False):
        try:
            f = open(file_path, "r", encoding="utf8")
            if as_line:
                content = f.readlines()
            else:
                content = f.read()
            f.close()
            return content
        except FileNotFoundError:
            return None

    @staticmethod
    def set_file_content(file_path, content):
        try:
            f = open(file_path, "w", encoding="utf8")
            f.write(content)
            f.close()
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def file_exists(file):
        return Path(file).is_file()

    @staticmethod
    def folder_exists(folder):
        return Path(folder).is_dir()

    @staticmethod
    def create_folder_if_not_exists(folder):
        Path(folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def smart_cast(s):
        if s == "True":
            return True
        elif s == "False":
            return False
        try:
            return int(s)
        except ValueError:
            pass
        try:
            return float(s)
        except ValueError:
            return s

    @staticmethod
    def string_to_list(s):
        if isinstance(s, str) and ',' in s:
            return MOOCUtils.strip_list(s.split(','))
        return s

    @staticmethod
    def string_to_smart_list(s, cast=True):
        if ',' in s:
            l = list()
            parts = s.split(",")
            for e in parts:
                if len(e) > 0:
                    if cast:
                        l.append(MOOCUtils.smart_cast(e.strip()))
                    else:
                        l.append(e.strip())
            return l
        elif cast:
            return MOOCUtils.smart_cast(s.strip())
        else:
            return s.strip()

    @staticmethod
    def read_ini_file(file_name, cast=True):
        try:
            file = open(file_name, "r", encoding="utf8")
            lines = file.readlines()
            file.close()
            params = dict()
            for line in lines:
                if not line.strip().startswith(';') and '=' in line:
                    params[line.split("=")[0].strip()] = MOOCUtils.string_to_smart_list(line.split("=")[1].strip(),
                                                                                        cast=cast)
            return params
        except FileNotFoundError:
            return None

    @staticmethod
    def extract_text(text, del1, del2):
        envs = []
        rest = []
        if del1 in text and del2 in text:
            parts = text.split(del1)
            rest.append(parts[0])
            for p in parts[1:]:
                if del2 in p:
                    envs.append(p.split(del2)[0].strip())
                    rest.append(p.split(del2)[1])
        else:
            rest = [text]
        return rest, envs

    @staticmethod
    def strip_list(l):
        return list(map(str.strip, l))
