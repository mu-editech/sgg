from sgg_fargate import SalaryGraphGenerator, SalaryGraphGeneratorParameters, get_list_s3
import tempfile
import os
import pytest

def test_set_file_type_1():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    sgg.set_file_type()
    assert sgg.file_type == 2


def test_set_file_type_2():
    sgg = SalaryGraphGenerator('1-給与明細書-20190625.pdf')
    sgg.set_file_type()
    assert sgg.file_type == 1


def test_set_file_type_3():
    sgg = SalaryGraphGenerator('7-給与明細書-20190625.pdf')
    sgg.set_file_type()
    assert sgg.file_type == 3


def test_set_file_type_4():
    sgg = SalaryGraphGenerator('給与明細書-20190625.pdf')
    sgg.set_file_type()
    assert sgg.file_type == 3



def test_chk_format_file_name_1():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    sgg.set_file_type()
    assert sgg.chk_format_file_name() == True


def test_chk_format_file_name_2():
    sgg = SalaryGraphGenerator('1-給与明細書-20190625.pdf')
    sgg.set_file_type()
    assert sgg.chk_format_file_name() == True


def test_chk_format_file_name_3():
    sgg = SalaryGraphGenerator('3-給与明細書-20190625.pdf')
    sgg.set_file_type()
    assert sgg.chk_format_file_name() == False


def test_chk_format_file_name_4():
    sgg = SalaryGraphGenerator('1-明細書-2019.pdf')
    sgg.set_file_type()
    assert sgg.chk_format_file_name() == False


def test_chk_format_file_name_5():
    sgg = SalaryGraphGenerator('1-明細書-20190625.txt')
    sgg.set_file_type()
    assert sgg.chk_format_file_name() == False


def test_get_file_date_1():
    sgg = SalaryGraphGenerator('3-給与明細書-20190625.pdf')
    assert sgg.get_file_date() == '2019-06'


def test_get_file_date_2():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    assert sgg.get_file_date() == '2017-07'


def test_create_add_data():
    add_data = {'income_month': '2019-10'}
    sgg = SalaryGraphGenerator('1-給与明細書-20191025.pdf')
    # test_texts = ["Col1", "Col2", "Col3", "\n", "Val1", "Val2", "Val3", "\n", "Col4", "Col5", "Col6", "\n", "Val4", "Vol5", "Vol6"]
    test_texts = """Col1,Col2,Col3
Val1,Val2,Val3
Col4,Col5,Col6
Val4,Val5,Val6"""
    result_dict = {
        "income_month":"2019-10",
        "Col1":"Val1",
        "Col2":"Val2",
        "Col3":"Val3",
        "Col4":"Val4",
        "Col5":"Val5",
        "Col6":"Val6"
    }

    with tempfile.TemporaryDirectory() as dir:
        with open(os.path.join(dir, 'test_text.csv'), 'w', encoding='utf-8') as f:
            f.write(test_texts)
        kekka = sgg.create_add_data(input_csv_file_name=os.path.join(dir, 'test_text.csv'), max_records=4, add_data=add_data)
        assert kekka == result_dict


def test_update_void_to_none():
    sgg = SalaryGraphGenerator('1-給与明細書-20191025.pdf')
    input_table_dict = {'Col1':'Val1', 'Col2':'', 'Col3':'Val3', 'Col4':''}
    assert sgg.update_void_to_none(input_table_dict) == {'Col1':'Val1', 'Col2':None, 'Col3':'Val3', 'Col4':None}

