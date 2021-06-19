import os


def upload_resource_post(file, object):
    if file is not None:
        if object.file is not None:
            delete_resource_post(object)
        id = object.Post_id
        mimetype = file.mimetype.split('/')[1]
        print(mimetype)
        file.save('file/post/' + str(id) + '.' + mimetype)
        object.file = mimetype


def delete_resource_post(object):
    if object.file is not None:
        id = object.Post_id
        if os.path.exists('file/post/' + str(id) + '.' + object.file):
            os.remove('file/post/' + str(id) + '.' + object.file)


def upload_resource_reply(file, object):
    if file is not None:
        if object.file is not None:
            delete_resource_post(object)
        id = object.Reply_id
        mimetype = file.mimetype.split('/')[1]
        print(mimetype)
        file.save('file/reply/' + str(id) + '.' + mimetype)
        object.file = mimetype


def delete_resource_reply(object):
    if object.file is not None:
        id = object.Reply_id
        if os.path.exists('file/reply/' + str(id) + '.' + object.file):
            os.remove('file/reply/' + str(id) + '.' + object.file)
