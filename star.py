

class Star:
    def __init__(self, StarID, HIP, HD, HR, Gliese, BayerFlamsteed, ProperName,
                 RA, Dec, Distance, PMRA, PMDec, RV, Mag, AbsMag, Spectrum,
                 ColorIndex, X, Y, Z, VX, VY, VZ, X2d, Y2d):
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

    def __repr__(self):
        return "Star <id={};{},{},{}>".format(self.StarID, self.X, self.Y, self.Z)

    def __str__(self):
        return self.__repr__()