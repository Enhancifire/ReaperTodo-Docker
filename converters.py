import schema, models

def task_model_to_schema(model: models.Task, scheme: schema.Task):
    title = model.title
    id = model.id
    owner_id = model.owner_id
    due = model.due

    scheme.title = title
    scheme.id = id
    scheme.owner_id = owner_id
    scheme.due = due

    return scheme
