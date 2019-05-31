def update(params, optional):
    for key in optional:
        if optional[key] is not None:
            params[key] = optional[key]
