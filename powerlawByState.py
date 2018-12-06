import sqlite3
import powerlaw
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

#####
## This is gets powerlaw fit per state for the full data set.
##
## Run with "python powerlawByState.py > byState.csv"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE, STATE FROM fires')
tableData = cur.fetchall()
conn.close()

states = {}
for i in range(0, len(tableData)):
    states[tableData[i][1]] = True

print("State, Count, Min, Max, alpha, sigma, xmin")

for state in states:
    data = []
    minSize = tableData[0][0]
    maxSize = tableData[0][0]
    for i in range(0, len(tableData)):
        if tableData[i][1] == state:
            size = tableData[i][0]
            minSize = min(minSize, size)
            maxSize = max(maxSize, size)
            data.append(size)

    results = powerlaw.Fit(data[:100])

    print(state, ",", len(data), ",",  minSize,
          ",",  maxSize, ",",  results.alpha,
          ",",results.sigma, ",",  results.xmin)
