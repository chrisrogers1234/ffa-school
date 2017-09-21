import os
import config_base

class Config(config_base.Config):
    pass

Config.substitution_list[0]["__energy__"] = 30.
Config.substitution_list[0]["__step_size__"] = 0.1
Config.substitution_list[0]["__max_y_power__"] = 2
Config.substitution_list[0]["__tan_delta__"] = 1
Config.find_closed_orbits["seed"] = [3471.52692682,    26.26536878, 0.] # tan_delta=1
if abs(Config.substitution_list[0]["__tan_delta__"] - 1) < 1e-3 and abs(Config.substitution_list[0]["__tan_delta__"] - 3) < 1e-3 :
    Config.find_closed_orbits["seed"] = [2791.9, -8.17141081316, 0.] # tan_delta=1
Config.run_control["output_dir"] = os.path.join(os.getcwd(), "output/base_alt_tan_delta=1")
Config.find_tune["delta_y"] = 0.01

dummy = """
    NOTE TAN DELTA = 1
    substitutions {u'__beamfile__': u'disttest.dat', u'__field_index__': 4.32, u'__energy__': 3.0, u'__d_length__': 0.2, u'__df_ratio__': -0.1965, u'__max_y_power__': 2, u'__b_mean__': -0.011, u'__end_length__': 0.1, u'__f_length__': 0.1, u'__n_turns__': 2.1, u'__tan_delta__': 1, u'__step_size__': 0.1}
    x_tune 0.216009715687
    x_tune_error 0.00369610508055
    y_tune 0.218366040288
    y_tune_error 0.00519897618106
tracking hit ... 2791.9 0.01 0.0 -8.17141081316 0.0 75.0908461119


    substitutions {u'__beamfile__': u'disttest.dat', u'__field_index__': 4.32, u'__energy__': 30.0, u'__d_length__': 0.2, u'__df_ratio__': -0.1965, u'__max_y_power__': 4, u'__b_mean__': -0.011, u'__end_length__': 0.1, u'__f_length__': 0.1, u'__n_turns__': 2.1, u'__tan_delta__': 1.0, u'__step_size__': 0.1}
    x_tune 0.216127504788
    x_tune_error 0.00273811317021
    y_tune 0.118950786817
    y_tune_error 9.8721359381e-05
Config.find_closed_orbits["seed"] = [3471.55, 26.2653294656, 0.]
"""

dummy = """
    NOTE TAN DELTA = 0

    substitutions {u'__beamfile__': u'disttest.dat', u'__field_index__': 4.32, u'__energy__': 3.0, u'__d_length__': 0.2, u'__df_ratio__': -0.1965, u'__max_y_power__': 2, u'__b_mean__': -0.011, u'__end_length__': 0.1, u'__f_length__': 0.1, u'__n_turns__': 2.1, u'__tan_delta__': 0, u'__step_size__': 0.1}
    x_tune 0.211069608604
    x_tune_error 0.00102945876859
    y_tune 0.194569470947
    y_tune_error 0.00695947008575
tracking hit ... 2772.84 0.01 0.0 -4.56047103656 0.0 75.0908461119

    substitutions {u'__beamfile__': u'disttest.dat', u'__field_index__': 4.32, u'__energy__': 30.0, u'__d_length__': 0.2, u'__df_ratio__': -0.1965, u'__max_y_power__': 2, u'__b_mean__': -0.011, u'__end_length__': 0.1, u'__f_length__': 0.1, u'__n_turns__': 2.1, u'__tan_delta__': 0, u'__step_size__': 0.1}
    x_tune 0.210982398164
    x_tune_error 0.00140331611041
    y_tune 0.194175924098
    y_tune_error 0.000799408728836
Config.find_closed_orbits["seed"] = [3471.55, 26.2653294656, 0.]
"""