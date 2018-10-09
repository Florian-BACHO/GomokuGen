class ArgmaxActionSelector:
    def __call__(self, values):
        out = 0
        max = values[out]
        for i, it in enumerate(values):
            if it > max:
                out = i
                max = it
        return out
