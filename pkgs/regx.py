import re

REGX = {
    "date": re.compile(
        r"^"
        r"(0[1-9]|[12][0-9]|3[01])"
        r"([/-]?)"
        r"(0[1-9]|1[0-2])"
        r"\2"
        r"(20[0-9]{2})"
        r"$"
    ),
    "siape": re.compile(r"\b[0-9]{6,}\b"),
    "sigrh": re.compile(
        r"("
        r"([0-9]{6,})"
        r"(?: "
        r"(?:0[1-9]|[12][0-9]|3[01])"
        r"/"
        r"(?:0[1-9]|1[0-2])"
        r"/"
        r"(?:20[0-9]{2})"
        r"){2,}"
        r")"
    ),
    "nproc": re.compile(
        r"lista de presenca (com direito a voz e voto)"
        r"[0-9]+ sei [0-9]+\.[0-9]+/[0-9]+-[0-9]+ / pg\. [0-9]+"
    ),
    "seime": re.compile(
        r"documento assinado eletronicamente por\s([^,]+),\s([^,]+),\sem"
        r"\s([^,]+),\sas\s([^,]+),\sconforme horario oficial de brasilia",
        re.MULTILINE,
    ),
}
