#
# Main View
#


def fake_currentRow():
    return 1


def fake_get_selected_student():
    return "ani-1111"


def fake_function(*args):
    pass


#
# Log View
#


class FakeQitem:
    def text(self, number):
        return "dummy91dcb1ae"


def fake_get_selected_file():
    return "dummy_file.txt"


def fake_currentText():
    return "selected dummy"


def fake_get_selected_sha():
    return "dummy91dcb1ae"


def fake_selectedItems():
    fake_qitem = FakeQitem()
    fake_qitem_2 = FakeQitem()
    return [fake_qitem, fake_qitem_2]
