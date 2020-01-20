import charts.histogram as histo
import charts.svg as svg

width = 600
height = 300
padding = 40

total_cn = svg.SvgElement("symbol", [
    ("id", "total_cn"),
    ("viewBox", "0 0 %s %s" % (width, height))
])

# full_cn = svg.SvgElement("symbol", [
#     ("id", "full_cn"),
#     ("viewBox", "0 0 %s %s" % (width, height))
# ])

total_cn.value = histo.get_svg("/Users/awarren/Documents/Illumina/XiaoSMN/SMN_1kGP_results.tsv",
                               "/Users/awarren/Documents/Illumina/XiaoSMN/SMN.tsv",
                               col="Total_CN_raw",
                               width=width,
                               height=height,
                               padding=padding)

total_cn_link = svg.SvgElement("use", [
    ("xlink:href", "#total_cn"),
    ("style", "opacity:1.0"),
    ("x", "0"),
    ("y", "0")
])

# full_cn.value = histo.get_svg("/Users/awarren/Documents/Illumina/XiaoSMN/SMN_1kGP_results.tsv",
#                               "/Users/awarren/Documents/Illumina/XiaoSMN/SMN.tsv",
#                               col="Full_length_CN_raw")

# full_cn_link = svg.SvgElement("use", [
#     ("xlink:href", "#full_cn"),
#     ("style", "opacity:1.0"),
#     ("x", "0"),
#     ("y", "%s" % height)
# ])

with open("/Users/awarren/Desktop/test.svg", 'w') as fo:
    svg_head = svg.headers(width, height, padding)
    svg_tail = svg.closing_tag()

    fo.write(svg_head)
    fo.write(total_cn.to_string())
    # fo.write(full_cn.to_string())
    fo.write(total_cn_link.to_string())
    # fo.write(full_cn_link.to_string())
    fo.write(svg_tail)
