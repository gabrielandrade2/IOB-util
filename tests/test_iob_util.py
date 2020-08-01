from iob_util import __version__, util
import unittest


def test_version():
    assert __version__ == '0.1.0'


class TestEncode(unittest.TestCase):
    """test class of iob encode
    """
    def setUp(self):
        self.sents = [
                "<C>脳梗塞</C>を認め，<M>医薬品</M>の投与を行った．",
                '<C value="N">関節液貯留</C>は認めない．'
                ]
        self.test_res = [[(0, 3, "C", "脳梗塞"), (7, 10, "M", "医薬品")], [(0, 5, "C", "関節液貯留")]]
        self.test_res_without_M = [[(0, 3, "C", "脳梗塞")], [(0, 5, "C", "関節液貯留")]]
        self.test_res_attr = [[(0, 3, "C", "脳梗塞"), (7, 10, "M", "医薬品")], [(0, 5, "CN", "関節液貯留")]]
        self.test_sent = ["脳梗塞を認め，医薬品の投与を行った．", "関節液貯留は認めない．"]

    def test_convert_xml_to_dict(self):
        s, ans = util.convert_xml_to_taglist(self.sents[0])
        self.assertEqual(s, self.test_sent[0])
        self.assertEqual(ans, self.test_res[0])

        s, ans = util.convert_xml_to_taglist(self.sents[0], tag_list=["C"])
        self.assertEqual(s, self.test_sent[0])
        self.assertEqual(ans, self.test_res_without_M[0])

        s, ans = util.convert_xml_to_taglist(self.sents[1])
        self.assertEqual(s, self.test_sent[1])
        self.assertEqual(ans, self.test_res[1])

        s, ans = util.convert_xml_to_taglist(self.sents[1], attr=["value"])
        self.assertEqual(s, self.test_sent[1])
        self.assertEqual(ans, self.test_res_attr[1])

    def test_convert_taglist_to_iob(self):
        pass

if __name__ == "__main__":
    unittest.main()

