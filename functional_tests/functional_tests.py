from selenium import webdriver
import unittest


class NovoVisitanteTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/home/partiu/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def test_acessa_site(self):
        self.browser.get('http://localhost:8000')
        import time
        time.sleep(3)

        self.assertIn('Projeto Base', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')