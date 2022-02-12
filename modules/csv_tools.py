import csv


def save_model(path, first_row, symbols_str, features):
    [
        weight_black, weight_black_norm,
        x_coords, y_coords,
        x_coords_norm, y_coords_norm,
        x_axis_moment, y_axis_moment,
        x_axis_moment_norm, y_axis_moment_norm,
        icm45,              icm135,
        icm45_norm,         icm135_norm
    ] = features

    with open(path, mode='w') as analysis_file:
        analysis_writer = csv.writer(analysis_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        analysis_writer.writerow(first_row)
        for _s in symbols_str:
            analysis_writer.writerow(
                [
                    _s,
                    weight_black[_s],
                    "%.3f" % weight_black_norm[_s],
                    "%.2f" % x_coords[_s],
                    "%.2f" % y_coords[_s],
                    "%.3f" % x_coords_norm[_s],
                    "%.3f" % y_coords_norm[_s],
                    "%.0f" % x_axis_moment[_s],
                    "%.0f" % y_axis_moment[_s],
                    "%.3f" % x_axis_moment_norm[_s],
                    "%.3f" % y_axis_moment_norm[_s],
                    "%.0f" % icm45[_s],
                    "%.0f" % icm135[_s],
                    "%.3f" % icm45_norm[_s],
                    "%.3f" % icm135_norm[_s]
                ]
            )


def load_model(path):
    result = {}

    with open(path, mode='r') as analysis_file:
        analysis_file.readline()
        analysis_reader = csv.reader(analysis_file, delimiter=';', quotechar='"')
        for row in analysis_reader:
            result[row[0]] = {
                "black": float(row[2]),
                "x_center": float(row[5]),
                "y_center": float(row[6]),
                "x_axis": float(row[9]),
                "y_axis": float(row[10]),
                "icm45": float(row[13]),
                "icm135": float(row[14]),
            }

    return result


def save_hypothesis(hyp, path):
    with open(path, mode='w') as analysis_file:
        analysis_writer = csv.writer(analysis_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for h in hyp:
            res = []
            for key, value in sorted(h.items(), key=lambda item: item[1], reverse=True):
                res.append("%s (%.3f)" % (key, value))
            analysis_writer.writerow(res)


def save_string(hypothesis, model_string, path):
    real = list(map(lambda d: max(d.items(), key=lambda x: x[1])[0], hypothesis))
    theory = list(model_string)

    correct = []
    for i in range(0, len(real)):
        correct.append(1 if real[i] == theory[i] else 0)

    with open(path, mode='w') as diff_string:
        diff_writer = csv.writer(diff_string, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        diff_writer.writerow(real)
        diff_writer.writerow(theory)
        diff_writer.writerow(correct)
