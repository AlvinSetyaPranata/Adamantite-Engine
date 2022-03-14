

def get_locals(var_):
    local_var = {}


    for key, var in vars(var_).items():
        if not (key.startswith("__") and key.endswith("__")):
            local_var[key] = var

    return local_var

