from datetime import datetime

# Duration
duree = 5

# Three test periods for real data

set1 = {"T0": datetime.strptime("05/07/2000", "%d/%m/%Y").date(),
        "T1": datetime.strptime("03/07/2001", "%d/%m/%Y").date(),  
        "T2": datetime.strptime("02/07/2002", "%d/%m/%Y").date(),
        "T3": datetime.strptime("02/07/2003", "%d/%m/%Y").date(),
        "T4": datetime.strptime("02/07/2004", "%d/%m/%Y").date(),
        "Tc": datetime.strptime("05/07/2005", "%d/%m/%Y").date()}

set2 = {"T0": datetime.strptime("04/01/2005", "%d/%m/%Y").date(),
        "T1": datetime.strptime("04/01/2006", "%d/%m/%Y").date(),
        "T2": datetime.strptime("04/01/2007", "%d/%m/%Y").date(),
        "T3": datetime.strptime("04/01/2008", "%d/%m/%Y").date(),
        "T4": datetime.strptime("05/01/2009", "%d/%m/%Y").date(),
        "Tc": datetime.strptime("04/01/2010", "%d/%m/%Y").date()}

set3 = {"T0": datetime.strptime("05/01/2009", "%d/%m/%Y").date(),
        "T1": datetime.strptime("04/01/2010", "%d/%m/%Y").date(),
        "T2": datetime.strptime("04/01/2011", "%d/%m/%Y").date(),
        "T3": datetime.strptime("04/01/2012", "%d/%m/%Y").date(),
        "T4": datetime.strptime("04/01/2013", "%d/%m/%Y").date(),
        "Tc": datetime.strptime("06/01/2014", "%d/%m/%Y").date()}

# Currency for structured product cash flows
currency = "eur"

# Initial investment
initial_investment = 1000
