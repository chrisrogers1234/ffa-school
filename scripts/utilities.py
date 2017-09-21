import xboa.common

def sub_to_name(sub_key):
    sub_name = sub_key[2:-2]
    sub_name = sub_name.replace("_", " ")
    return sub_name
  
def tune_lines(canvas, min_order=0, max_order=8):
    canvas.cd()
    for x_power in range(0, max_order):
        for y_power in range(0, max_order):
            if y_power + x_power > max_order or y_power + x_power == 0:
                continue
            x_points = [0., 1.]
            y_points = [0., 1.]
            if x_power > y_power:
                x_points[0] = y_points[0]*y_power/x_power
                x_points[1] = y_points[1]*y_power/x_power
            else:
                y_points[0] = x_points[0]*x_power/y_power
                y_points[1] = x_points[1]*x_power/y_power
            hist, graph = xboa.common.make_root_graph("", x_points, "", y_points, "")
            graph.Draw("SAMEL")
            x_points = [1.-x for x in x_points]
            #y_points = [1.-y for y in y_points]
            hist, graph = xboa.common.make_root_graph("", x_points, "", y_points, "")
            graph.Draw("SAMEL")
    canvas.Update()

def get_substitutions_axis(data):
    subs_ref = data[0]['substitutions']
    axis_candidates = {}
    for item in data:
        subs = item['substitutions']
        for key in subs.keys():
            if subs[key] != subs_ref[key]:
                try:
                    float(subs[key])
                    axis_candidates[key] = []
                except TypeError:
                    continue
    for item in data:
        for key in axis_candidates:
            axis_candidates[key].append(item['substitutions'][key])
    return axis_candidates
