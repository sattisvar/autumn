def mapper(attr, target=None, mapf=(lambda x: x)):
    def mapper_deco(f):
        def decorated_func(entity, *args, **kwargs):
            result = f(entity, *args, **kwargs)
            if type(entity) == type({}):
                if attr in entity.keys():
                    entity_source = entity[attr]
                else:
                    return result
            else:
                try:
                    entity_source = getattr(entity, attr)
                except AttributeError:
                    return result

            if target is None:
                target_attr = attr
            else:
                target_attr = target
            if isinstance(result, dict):
                result[target_attr] = mapf(entity_source)
            else:
                setattr(result, target_attr, mapf(entity_source))
            return result
        return decorated_func
    return mapper_deco
