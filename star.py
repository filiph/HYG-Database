#!/usr/bin/python
#  -*- coding: utf-8 -*-

import re
import unicodedata

CONSTELLATION_ABBR = {
    # Constelations
    "And": u"Andromedae",
    "Ant": u"Antliae",
    "Aps": u"Apodis",
    "Aqr": u"Aquarii",
    "Aql": u"Aquilae",
    "Ara": u"Arae",
    "Ari": u"Arietis",
    "Aur": u"Aurigae",
    "Boo": u"Boötis",
    "Cae": u"Caeli",
    "Cam": u"Camelopardalis",
    "Cnc": u"Cancri",
    "CVn": u"Canum Venaticorum",
    "CMa": u"Canis Majoris",
    "CMi": u"Canis Minoris",
    "Cap": u"Capricorni",
    "Car": u"Carinae",
    "Cas": u"Cassiopeiae",
    "Cen": u"Centauri",
    "Cep": u"Cephei",
    "Cet": u"Ceti",
    "Cha": u"Chamaeleontis",
    "Cir": u"Circini",
    "Col": u"Columbae",
    "Com": u"Comae Berenices",
    "CrA": u"Coronae Australis",
    "CrB": u"Coronae Borealis",
    "Crv": u"Corvi",
    "Crt": u"Crateris",
    "Cru": u"Crucis",
    "Cyg": u"Cygni",
    "Del": u"Delphini",
    "Dor": u"Doradus",
    "Dra": u"Draconis",
    "Equ": u"Equulei",
    "Eri": u"Eridani",
    "For": u"Fornacis",
    "Gem": u"Geminorum",
    "Gru": u"Gruis",
    "Her": u"Herculis",
    "Hor": u"Horologii",
    "Hya": u"Hydrae",
    "Hyi": u"Hydri",
    "Ind": u"Indi",
    "Lac": u"Lacertae",
    "Leo": u"Leonis",
    "LMi": u"Leonis Minoris",
    "Lep": u"Leporis",
    "Lib": u"Librae",
    "Lup": u"Lupi",
    "Lyn": u"Lyncis",
    "Lyr": u"Lyrae",
    "Men": u"Mensae",
    "Mic": u"Microscopii",
    "Mon": u"Monocerotis",
    "Mus": u"Muscae",
    "Nor": u"Normae",
    "Oct": u"Octantis",
    "Oph": u"Ophiuchi",
    "Ori": u"Orionis",
    "Pav": u"Pavonis",
    "Peg": u"Pegasi",
    "Per": u"Persei",
    "Phe": u"Phoenicis",
    "Pic": u"Pictoris",
    "Psc": u"Piscium",
    "PsA": u"Piscis Austrini",
    "Pup": u"Puppis",
    "Pyx": u"Pyxidis",
    "Ret": u"Reticuli",
    "Sge": u"Sagittae",
    "Sgr": u"Sagittarii",
    "Sco": u"Scorpii",
    "Scl": u"Sculptoris",
    "Sct": u"Scuti",
    "Ser": u"Serpentis",
    "Sex": u"Sextantis",
    "Tau": u"Tauri",
    "Tel": u"Telescopii",
    "Tri": u"Trianguli",
    "TrA": u"Trianguli Australis",
    "Tuc": u"Tucanae",
    "UMa": u"Ursae Majoris",
    "UMi": u"Ursae Minoris",
    "Vel": u"Velorum",
    "Vir": u"Virginis",
    "Vol": u"Volantis",
    "Vul": u"Vulpeculae",

    # Bayer Greek letter abbreviations
    "alf": u"Alpha",
    "bet": u"Beta",
    "gam": u"Gamma",
    "del": u"Delta",
    "eps": u"Epsilon",
    "zet": u"Zeta",
    "eta": u"Eta",
    "tet": u"Theta",  # non-standard, but used by Simbad
    "the": u"Theta",
    "iot": u"Iota",
    "kap": u"Kappa",
    "lam": u"Lambda",
    "mu.": u"Mu",
    "nu.": u"Nu",
    "ksi": u"Xi",
    "omi": u"Omicron",
    "pi.": u"Pi",
    "rho": u"Rho",
    "sig": u"Sigma",
    "tau": u"Tau",
    "ups": u"Upsilon",
    "phi": u"Phi",
    "chi": u"Chi",
    "psi": u"Psi",
    "omd": u"Omega"
}

COMPILED_CONSTELLATION_ABBR = []
for k in CONSTELLATION_ABBR:
    regex = re.compile(ur"\b{}(\b|(?=\s))".format(k), flags=re.UNICODE)
    COMPILED_CONSTELLATION_ABBR.append((regex, CONSTELLATION_ABBR[k]))


SUPERSCRIPT_ABBR = {
    "01": u"¹",
    "02": u"²",
    "03": u"³",
}


class Star:
    def __init__(self, StarID, HIP, HD, HR, Gliese, BayerFlamsteed, ProperName,
                 RA, Dec, Distance, PMRA, PMDec, RV, Mag, AbsMag, Spectrum,
                 ColorIndex, X, Y, Z, VX, VY, VZ, X2d, Y2d, habitable=False):
        self.StarID = StarID
        self.HIP = HIP
        self.HD = HD
        self.HR = HR
        self.Gliese = Gliese
        self.BayerFlamsteed = BayerFlamsteed
        self.ProperName = ProperName
        self.RA = RA
        self.Dec = Dec
        self.Distance = Distance
        self.PMRA = PMRA
        self.PMDec = PMDec
        self.RV = RV
        self.Mag = Mag
        self.AbsMag = AbsMag
        self.Spectrum = Spectrum
        self.ColorIndex = ColorIndex
        self.X = X
        self.Y = Y
        self.Z = Z
        self.VX = VX
        self.VY = VY
        self.VZ = VZ
        self.X2d = X2d
        self.Y2d = Y2d
        self.habitable = habitable
        self.simbad_string_id = None
        self.simbad_identifiers = None

    def coords_2d(self, hex=False, multiply=1):
        hex_offset = 0
        if hex and self.Y2d % 2 != 0:
            hex_offset = multiply / 2
        return self.X2d * multiply + hex_offset, self.Y2d * multiply

    def get_simbad_ident(self):
        """
        Returns the best way to represent this star for searching through
        http://simbad.u-strasbg.fr/simbad/sim-fbasic. Already URL encoded (so HIP 123 is returned
        as "HIP+123").
        """
        if self.HIP is not None and self.HIP != "" and self.HIP != "0":
            return "HIP+{}".format(self.HIP)
        if self.HD is not None and self.HD != "" and self.HD != "0":
            return "HD+{}".format(self.HD)
        if self.Gliese is not None and self.Gliese != "" and self.Gliese != "0":
            s = self.Gliese.replace("NN", "GJ")  # NN stands for No Name, but to find it in Simbad,
                                                 # we need to rewrite to GJ
            s = s.replace(" ", "+")
            return s

    @staticmethod
    def score_and_normalize_name(name):
        """
        Takes a Simbad name and returns a tuple with 1) a score (lower is better) of how 'human' the
        name is, and 2) the name normalized (without "NAME" prefixes and the like).
        """
        assert(isinstance(name, unicode))
        if name.startswith(u"NAME "):
            name = name[len(u"NAME "):]
            if not any(map(lambda c: unicodedata.category(c) == 'Ll', name)):
                # No lower case ("PROXIMA CENTAURI"). Let's put it in title case.
                name = name.title()
        elif name.startswith(u"* "):
            name = name[len(u"* "):]
        elif name.startswith(u"** "):
            name = name[len(u"** "):]
        elif name.startswith(u"V* "):
            name = name[len(u"V* "):]

        score = 0
        for ch in name:
            if ch.isdigit():
                score += 10
            if not ch.isalnum():
                score += 5
            if ch.isupper():
                score += 2
            score += 1
        if name.startswith(u"Zkh"):
            # Get rid of too much Zkh NNN stars.
            score += 20
        if name.startswith(u"MCY"):
            # Get rid of too much obscure MCY stars.
            score += 20

        # TODO: alf02 -> Alpha²
        name = re.sub(SUPERSCRIPT_REGEX, ur" \1", name)

        # alf Cen -> Alpha Centauri
        for regex, full_name in COMPILED_CONSTELLATION_ABBR:
            name = re.sub(regex, full_name, name)

        return score, name


    def get_best_human_ident(self):
        """
        Returns the string that would most likely be used by a human when referring to the star.
        """
        if self.simbad_identifiers:
            scored = []
            if self.ProperName is not None and self.ProperName != "":
                scored.append("NAME {}".format(self.ProperName))
            for identifier in self.simbad_identifiers:
                if identifier != "" and not identifier.isspace():
                    scored.append(Star.score_and_normalize_name(identifier))

            scored.sort(key=lambda tup: tup[0])  # sort by score
            return scored[0][1]  # return normalized name

        if self.ProperName:
            return self.ProperName

        return self.get_simbad_ident().replace("+", " ")

    def __repr__(self):
        return "Star <id={};{},{},{};{}>".format(self.StarID, self.X, self.Y, self.Z,
                                                 self.get_simbad_ident())

    def __str__(self):
        return self.__repr__()

SUPERSCRIPT_REGEX = re.compile(ur"(?<=[a-z\.]{3})0([1-3])")