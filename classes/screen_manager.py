class ScreenManagerPercentage:
    def __init__(self, **data):
        self.window_width = 929
        self.window_height = 522

        self.width = self.__axis_x(data["width"])
        self.height = self.__axis_y(data["height"])
        self.offset_x = self.__axis_x(data["offset_x"])
        self.offset_y = self.__axis_y(data["offset_y"])

        self.x1 = self.offset_x
        self.x2 = self.x1 + self.width
        self.y1 = self.offset_y
        self.y2 = self.y1 + self.height

    def __axis_x(self, x_percentage):
        return round((self.window_width * x_percentage) / 100)

    def __axis_y(self, y_percentage):
        return round((self.window_height * y_percentage) / 100)

    def capture(self, img):
        return img[self.y1:self.y2, self.x1:self.x2]