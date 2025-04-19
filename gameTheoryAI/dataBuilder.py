import sim
import csv
import random

def buildData(entries, csvName):
    with open(csvName, mode="w", newline='') as file:
        writer = csv.writer(file)
        #Remove this if rerunning to gather more data
        writer.writerow(["fightWinScore",
                        "fightLoseScore",
                        "scareWinScore",
                        "threatWinScore",
                        "threatLoseScore",
                        "hawkFraction"])
        for entry in range(entries):
            features = {
                "fightWinScore": random.randint(-100, 100),
                "fightLoseScore": random.randint(-100, 100),
                "scareWinScore": random.randint(-100, 100),
                "threatWinScore": random.randint(-100, 100),
                "threatLoseScore": random.randint(-100, 100)
            }
            hawkFraction = sim.runSim(500, features)
            writer.writerow([features["fightWinScore"], 
                             features["fightLoseScore"], 
                             features["scareWinScore"], 
                             features["threatWinScore"], 
                             features["threatLoseScore"],
                             hawkFraction])
            if not entry%1000:
                print("Entry", str(entry) + "- Fraction: ", str(hawkFraction))
            
buildData(50000, "hawkDoveData.csv")