from collections import defaultdict
import click
import os
import requests

@click.command()
@click.argument("contest")
@click.argument("dif")
def main(contest, dif):
    contest_dir = f"AtCoder_{contest}"
    if os.path.exists(contest_dir):
        pass
    else:
        os.mkdir(contest_dir)
    #その難易度のテストケースのファイルがあるか
    if os.path.exists(contest_dir + f"/{dif}"):
        pass
    else:
        make_testcase(contest, dif)

def scrape_page_html(contest, dif):
    URL = f"https://atcoder.jp/contests/abc{contest}/tasks/abc{contest}_{dif}"
    if not os.path.exists(f"AtCoder_{contest}/{dif}/page/page.html"):
        r = requests.get(URL)
        page = r.text
        os.mkdir(f"AtCoder_{contest}/{dif}")
        os.mkdir(f"AtCoder_{contest}/{dif}/page")
        with open(f"AtCoder_{contest}/{dif}/page/page.html", "w") as f:
            f.write(page)   
    return

class test_case:
    def __init__(self):
        self.input = ""
        self.output = ""

def parse_test_case(contest, dif):
    #htmlを強引!にパースする
    test_cases = defaultdict(test_case)
    """
    <h3>入力例 {i}</h3>
    """
    open_pre = "<pre>"
    close_pre = "</pre>"
    with open(f"AtCoder_{contest}/{dif}/page/page.html", "r") as f:
        lines = f.readlines()
        for i in range(1, 4):
            input_form = f"<h3>入力例 {i}</h3>"
            output_form = f"<h3>出力例 {i}</h3>"
            for idx, v in enumerate(lines):
                if input_form in v:
                    input_ = []
                    lines[idx] = lines[idx].strip(input_form)
                    lines[idx] = lines[idx].strip(open_pre)

                    while close_pre not in lines[idx]:
                        input_.append(lines[idx])
                        idx+=1
                    test_cases[i].input = input_
                    continue
                if output_form in v:
                    output_ = []
                    lines[idx] = lines[idx].strip(output_form)
                    lines[idx] = lines[idx].strip(open_pre)
                    while close_pre not in lines[idx]:
                        output_.append(lines[idx])
                        idx+=1
                    test_cases[i].output = output_
    os.mkdir(f"AtCoder_{contest}/{dif}/testcase")
    for i, tc in test_cases.items():
        os.mkdir(f"AtCoder_{contest}/{dif}/testcase/{i}")
        with open(f"AtCoder_{contest}/{dif}/testcase/{i}/input", "w") as f:
            for line in tc.input:
                f.write(line)
        with open(f"AtCoder_{contest}/{dif}/testcase/{i}/output", "w") as f:
            for line in tc.output:
                f.write(line)

def make_testcase(contest, dif):
    #そのページのHTMLがあるかどうか。
    #何度もダウンロードせずに、一回だけHTMLをダウンロードする
    if not os.path.exists(f"AtCoder_{contest}/{dif}/testcase"):
        scrape_page_html(contest, dif)
        print("ok")
        parse_test_case(contest, dif)
        
        
def test(contest, dif):
    pass

if __name__ == "__main__":
    main()