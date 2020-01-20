class SvgElement:
    def __init__(self, name, attrs, value=None):
        self.name = name
        self.value = value
        self.attrs = attrs

    def to_string(self):
        result = "<%s" % self.name

        for attr in self.attrs:
            result += " %s=\"%s\"" % (attr[0], attr[1])
        result += ">"

        if self.value is not None:
            for v in self.value:
                if type(v) is str:
                    result += v
                else:
                    result += v.to_string()
        result += "</%s>" % self.name

        return result

    def add_attr(self, attr_tuple):
        self.attrs.append(attr_tuple)

    def modify_attr(self, attr_tuple):
        for attr in self.attrs:
            if attr[0] == attr_tuple[0]:
                attr[1] = attr_tuple[1]


def line(x1, y1, x2, y2, color="black", thickness=1, opacity=1.0, dashes=0):
    return SvgElement("line", [
        ("x1", x1),
        ("x2", x2),
        ("y1", y1),
        ("y2", y2),
        ("stroke", color),
        ("stroke-width", thickness),
        ("opacity", opacity),
        ("stroke-dasharray", dashes)
    ])


def rect(x, y, width, height, border_color="black", fill_color="black", border_width=1, corner_radius=0):
    return SvgElement("rect", [
        ("x", x),
        ("y", y),
        ("width", width),
        ("height", height),
        ("stroke", border_color),
        ("stroke-width", border_width),
        ("fill-color", fill_color),
        ("rx", corner_radius)
    ])


def circle(x, y, r, fill_color="black", border_color="black", border_width="black"):
    return SvgElement("circle", [
        ("cx", x),
        ("cy", y),
        ("r", r),
        ("stroke", border_color),
        ("stroke-width", border_width),
        ("fill-color", fill_color)
    ])


def text(x, y, txt, style="font: 13px sans-serif", transform=""):
    return SvgElement("text", [
        ("x", x),
        ("y", y),
        ("style", style),
        ("transform", transform)
    ], txt)


def add_tooltip(element, txt):
    title = SvgElement("title", [], txt)
    if element.value is None:
        element.value = [title]
    else:
        element.value += title


def headers():
    return "<svg " \
           "xmlns=\"http://www.w3.org/2000/svg\" " \
           "xmlns:xlink=\"http://www.w3.org/1999/xlink\">"


def closing_tag():
    return "</svg>"
