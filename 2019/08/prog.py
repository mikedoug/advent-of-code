
class LayeredImage(object):
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns

    def parse_raw_data(self, data):
        chunk_size = self._rows * self._columns
        self.layers = [ data[i:i+chunk_size] for i in range(0, len(data), chunk_size) ]

    def get_layer(self, i):
        return self.layers[i]

    def get_layer_count(self):
        return len(self.layers)

    def get_image(self):
        picture = list('2' * (self._rows * self._columns))
        for layer in self.layers:
            for i in range(len(picture)):
                if picture[i] == '2':
                    picture[i] = layer[i]

                if picture[i] == '0':
                    picture[i] = ' '
                elif picture[i] == '1':
                    picture[i] = 'X'

        picture = "".join(picture)

        return [ picture[i:i+self._columns] for i in range(0, self._rows * self._columns, self._columns) ]

        
with open("input.txt", "r") as f:
    # software = list(map(lambda x: int(x),f.readline().rstrip().split(",")))
    raw_image_data = f.readline().rstrip()

image = LayeredImage(6,25)
image.parse_raw_data(raw_image_data)

min_n0 = None
min_n0_layer = None
for layer in image.layers:
    n0 = layer.count('0')

    if min_n0 is None or n0 < min_n0:
        min_n0 = n0
        min_n0_layer = layer

print(f'Winning Layer: {min_n0_layer}')
print(f'count("1") * count("2") = {min_n0_layer.count("1") * min_n0_layer.count("2")}')

picture = image.get_image()
for row in picture:
    print (row)
