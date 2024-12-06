from dataclasses import fields


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def class_from_args(class_name, arg_dict):
    field_set = {f.name for f in fields(class_name) if f.init}
    filtered_arg_dict = {k: v for k, v in arg_dict.items() if k in field_set}
    return class_name(**filtered_arg_dict)
