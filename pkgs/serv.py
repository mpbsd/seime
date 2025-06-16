import json
import logging
import os
from datetime import datetime

import pandas as pd
import pdfplumber
from unidecode import unidecode

from .date import DATE
from .regx import REGX

logging.getLogger("pdfminer").setLevel(logging.ERROR)


class SERV:

    COD_PRE = 1
    COD_AUS = 2
    COD_JUS = 3

    def __init__(self):
        self.staff = self.__staff(self.__sigrh(), self.__seime())
        self.sheet = self.__sheet()

    def __cyear(self):
        return datetime.today().strftime("%Y")

    def __cadre(self):
        with open("data/json/staff.json", "r") as jfile:
            staff = json.load(jfile)
        return staff

    def __table(self):
        with open("data/json/table.json", "r") as jfile:
            table = json.load(jfile)
        return table

    def __trash(self, info):
        with open("brew/dump.csv", "a") as dumpfile:
            print(info, file=dumpfile)

    def __siape(self, fname):
        staff = self.__cadre()
        X = [k for k in staff.keys() if staff[k]["fname"] == fname.strip()]
        if X:
            siape = X[0]
        else:
            siape = None
        return siape

    def __siape_or_date(self, strdt):
        B = False
        if strdt:
            siape = REGX["siape"].match(strdt)
            if siape:
                B = True
            else:
                if DATE(strdt).iso != 0:
                    B = True
        return B

    def __excused(self, BREAK, dstr):
        c = 0
        for brk in BREAK:
            dt0 = DATE(brk[0])
            dt1 = DATE(brk[1])
            if (DATE(dstr).iso >= dt0.iso) and (DATE(dstr).iso <= dt1.iso):
                c += 1
        return True if (c > 0) else False

    def __a_whole_year(self, dtrng):
        C0 = DATE(dtrng[0]).D == 1
        C1 = DATE(dtrng[0]).M == 1
        C2 = DATE(dtrng[1]).D == 31
        C3 = DATE(dtrng[1]).M == 12
        C4 = DATE(dtrng[0]).Y == DATE(dtrng[1]).Y
        if C0 and C1 and C2 and C3 and C4:
            B = True
        else:
            B = False
        return B

    def __sigrh(self):
        L = []
        for document in os.listdir("data/pdfs/sig"):
            if document.endswith(".pdf"):
                with pdfplumber.open(f"data/pdfs/sig/{document}") as document:
                    for page in document.pages:
                        for TBL in page.find_tables():
                            for tbl in TBL.extract():
                                for row in tbl:
                                    if self.__siape_or_date(row):
                                        L.append(row)
        M = r""
        for dtrng in L:
            M += r" " + dtrng
        match = REGX["sigrh"].findall(M)
        N = {}
        if match:
            for m in match:
                siape = m[1]
                N[siape] = []
                X = m[0].split(" ")[1:]
                n = len(X) // 2
                for i in range(n):
                    dtrng = [X[2 * i], X[2 * i + 1]]
                    if not self.__a_whole_year(dtrng):
                        N[siape].append(dtrng)
        return N

    def __seime(self):
        M = {}
        T = ""
        for document in os.listdir("data/pdfs/sei"):
            if document.endswith(".pdf"):
                with pdfplumber.open(f"data/pdfs/sei/{document}") as document:
                    for page in document.pages:
                        T += unidecode(page.extract_text().lower())
        X = REGX["seime"].findall(T)
        if X:
            for x in X:
                siape = self.__siape(x[0])
                if siape:
                    if siape not in M.keys():
                        M[siape] = []
                    if x[2] in self.__table():
                        M[siape].append(x[2])
                    else:
                        self.__trash(x[0:4])
                else:
                    self.__trash(x[0:4])
        for siape in M.keys():
            M[siape] = sorted(M[siape], key=lambda x: DATE(x).iso)
        return M

    def __staff(self, SIGRH, SEIME):
        staff = self.__cadre()
        for siape in SIGRH.keys():
            if siape in staff.keys():
                staff[siape]["break"] = SIGRH[siape]
        for siape in SEIME.keys():
            if siape in staff.keys():
                staff[siape]["patch"] = SEIME[siape]
        for siape in staff.keys():
            staff[siape]["cd"] = {}
            for dt in self.__table():
                if dt in staff[siape]["patch"]:
                    staff[siape]["cd"][dt] = self.COD_PRE
                else:
                    if self.__excused(staff[siape]["break"], dt):
                        staff[siape]["cd"][dt] = self.COD_JUS
                    else:
                        staff[siape]["cd"][dt] = self.COD_AUS
        return staff

    def __sheet(self):
        Y = self.__cyear()
        S = self.staff
        A = {siape: [S[siape]["fname"]] for siape in S.keys()}
        B = {siape: S[siape]["cd"] for siape in S.keys()}
        da = pd.DataFrame.from_dict(A).T
        db = pd.DataFrame.from_dict(B).T
        with pd.ExcelWriter("brew/freq.ods", engine="odf") as ods:
            da.to_excel(ods, sheet_name="siape")
            db.to_excel(ods, sheet_name=f"{Y}")
        return db
