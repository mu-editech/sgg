from sgg import SalaryGraphGenerator
import tempfile
import codecs
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


def test_set_file_date_1():
    sgg = SalaryGraphGenerator('3-給与明細書-20190625.pdf')
    assert sgg.set_file_date() == '2019-06'


def test_set_file_date_2():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    assert sgg.set_file_date() == '2017-07'


def test_get_parent_path_raw_file_1():
    sgg = SalaryGraphGenerator('1-給与明細書-20190625.pdf')
    assert sgg.get_parent_path_raw_file(file_type=1) == 'raw/income'

def test_get_parent_path_raw_file_2():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    assert sgg.get_parent_path_raw_file(file_type=2) == 'raw/bonus'


def test_read_part_csv():
    sgg = SalaryGraphGenerator('2-賞与明細書-20170705.pdf')
    with tempfile.TemporaryDirectory() as dir:
        print('Hello,World,Beginners\n1000,2000,3000',
              file=codecs.open(
                  os.path.join(dir, 'test_1.csv'), 'w', encoding='utf-8'
              )
        )

        print('Tamago,Hiyoko,Kokko\n4000,5000,6000',
              file=codecs.open(
                  os.path.join(dir, 'test_2.csv'), 'w', encoding='utf-8'
              )
        )


        assert sgg.read_part_csv(
            max_roop_count=3,
            parent_file_name=os.path.join(dir, 'test'),
            add_record_header=['income_month'],
            add_record_data=['2017-07']
        ) == (['income_month', 'Hello', 'World', 'Beginners',
              'Tamago', 'Hiyoko', 'Kokko'], \
            ['2017-07', '1000', '2000', '3000', '4000', '5000', '6000'])


def test_create_add_bonus_record():
    sgg = SalaryGraphGenerator('2-賞与明細書-20191204.pdf')
    sgg.get_data_as_table()
    add_bonus_header = ['bonus_month', '控除率', '嘱託控除', '賞与額', '決算賞与', 'エルダー賞与', '嘱託賞与', '嘱託勤怠減額', '支給調整', '持株奨励金', '立替支給', '賞総支給額', '賞雇用保険料', '賞健康保険料', '賞介護保険料', '賞与厚生年金', '賞与所得税', 'GRP年金', 'GRP一般', '財形貯蓄', '持株拠出', '厚生貸付', '労金', '他控除', '立替回収', '賞与控除合計']
    add_bonus_data = ['2019-12', '', '', '883,800', '', '', '', '', '', '600', '', '884,400', '2,651', '37,527', '', '80,794', '46,767', '', '', '', '6,600', '', '', '', '', '174,339']

    with tempfile.TemporaryDirectory() as dir:
        assert sgg.create_add_bonus_record(parent_path=dir, file_date='2019-12') == \
           (add_bonus_header, add_bonus_data)



def test_create_add_income_record():
    sgg = SalaryGraphGenerator('1-給与明細書-20191025.pdf')
    sgg.get_data_as_table()
    result_dict = {'1.0手当': '5,481',
                     '1.0Ｈ': '2.55',
                     '1.25手当': '',
                     '1.25Ｈ': '',
                     '1.35手当': '',
                     '1.35Ｈ': '',
                     '1.5H': '',
                     '1.5手当': '',
                     '1.6手当': '',
                     '1.6Ｈ': '',
                     'GRP年金': '',
                     'P給与': '',
                     'income_month': '2019-10',
                     'るいとう': '',
                     '介護保険料': '',
                     '他控除': '',
                     '他支給': '',
                     '代休控除': '',
                     '代休控Ｈ': '',
                     '仮払精算': '',
                     '住宅手当': '40,000',
                     '住民税': '24,400',
                     '健保還付': '',
                     '健康保険料': '14,450',
                     '入居料': '',
                     '共済会費': '483',
                     '共済支給': '',
                     '共済貸付': '',
                     '出向手当': '',
                     '前月欠勤': '',
                     '前欠勤控': '',
                     '労金': '800',
                     '勤怠': '',
                     '単身手当': '',
                     '厚生年金料': '31,110',
                     '厚生貸付': '',
                     '基本給': '241,800',
                     '報奨金': '',
                     '客先勤務': '',
                     '年末年始': '',
                     '年調繰越': '',
                     '年調過不足': '',
                     '当月欠勤': '',
                     '当欠勤控': '',
                     '役割給': '',
                     '役員報酬': '',
                     '所得税': '6,230',
                     '持株会拠出金': '2,200',
                     '持株奨励金': '200',
                     '控除': '',
                     '控除合計': '82,384',
                     '損害保険': '',
                     '支給': '',
                     '欠勤控除': '',
                     '欠勤控Ｈ': '',
                     '法60超': '',
                     '法60超H': '',
                     '現物控除': '',
                     '現物支給': '',
                     '生命保険料': '',
                     '立替回収': '',
                     '立替支給': '',
                     '組合費': '1,850',
                     '総支給額': '287,481',
                     '職務手当': '',
                     '課税支給': '',
                     '調整給1': '',
                     '調整給2': '',
                     '財形貯蓄': '',
                     '賞与調整': '',
                     '通信教育等計': '',
                     '通勤費': '',
                     '遅早H': '',
                     '遅早控除': '',
                     '遡及差額(課)': '',
                     '長期ｻﾎﾟｰﾄ': '',
                     '雇用保険料': '861',
                     '非税支給': '',
                     'Ｐ通勤費': '',
                     'ｼﾌﾄ勤務': '',
                     'ﾗｲﾝ手当': ''}
    with tempfile.TemporaryDirectory() as dir:
        assert sgg.create_add_income_record(parent_path=dir, file_date='2019-10') == result_dict



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
