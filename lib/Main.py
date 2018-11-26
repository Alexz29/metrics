class Main:

    def __init__(self):
        pass

    @staticmethod
    def isset(arr, name, attr):
        flag = False
        for value in arr:
            if value[attr] == name:
                flag = value['id']
                break
            else:
                flag = False
        return flag

    @staticmethod
    def get_ids_for_delete(arr, arr_local, attr):
        array = []
        for remote in arr:
            flag = True
            for local in arr_local:
                if remote[attr] == local[attr]:
                    flag = False

            if flag:
                array.append(remote['id'])

        return array
