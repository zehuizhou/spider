js = '''function decrypt(t, e) {
            for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++) a[n[o]] = n[n.length / 2 + o];
            for (var s = 0; s < e.length; s++) r.push(a[i[s]]);
            return r.join("")
        }'''

headers = {
    "Cookie": "BAIDUID=B0B1F3D534AD44A6513406C1BB445988:FG=1; BIDUPSID=B0B1F3D534AD44A6513406C1BB445988; PSTM=1568808511; MCITY=-179%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BDUSS=ZReWN2VTJmY0xXR09YWlgxZEZmVDNwRzVJRVYxaHJuMUlPZlZsWDB3Uk93UjllSVFBQUFBJCQAAAAAAAAAAAEAAAD2E6iF0ruxrcb41srLrwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE40-F1ONPhdcT; PSINO=3; H_PS_PSSID=1467_21115_30211_20698_26350_22160; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1576547412; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1576547412",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
data_url = 'https://index.baidu.com/api/SearchApi/index?word={}&area=0&days=30'
uniqid_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'

if __name__ == '__main__':
    pass
