f = open('hightmap.map.csv', 'w')

grid_meassurements = []
for i in range(10):
    grid_meassurements.append(i)
print(grid_meassurements)
# f.write(str(grid_meassurements))
# Devuelve [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

grid_meassurements = []
for i in range(10):
    line_to_append = (str(i) + ";" + str(i) +
                      ";" + str(i))
    # grid_meassurements.append(line_to_append)
    # print(grid_meassurements)
    f.write(line_to_append + "\n")