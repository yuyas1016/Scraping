#!/usr/bin/env python
# coding: utf-8


from time import sleep

import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import re
from flask import request



def cookpad():
    # 検索したい料理名を定義しする
    food_name = request.form['keyword']
    # 検索したワードをエンコードする
    name_quote = urllib.parse.quote(food_name)

    # 変数base_urlにクックパッドサイトのURLを定義
    base_url = 'https://cookpad.com/search/' + name_quote

    # requestsモジュールで指定したURLのHTMLを取得
    r = requests.get(base_url)
    # BeautifulSoupで取得したHTMLをパースする
    soup = BeautifulSoup(r.text, 'html.parser') # r.textでencoding属性でデコードされたレスポンスの内容（文字列）を取得する

    # 2ページ目以降のURLに必要なrecipe_hitsをHTMLから抽出
    recipe_hits = soup.find('em')
    # reモジュールのsub関数でrecipe_hitsの数字だけ取り出す
    rh = re.sub('\D', '', recipe_hits.text)


    # 検索１〜５ページまでのレシピ名とレシピページへのURLをスクレイピング
    d_lists = []

    num = 1

    while num <= 5:
        next_url = base_url + '?page=' + str(num) + '&recipe_hit=' + rh
        print(next_url)
        # HTMLを取得
        r = requests.get(next_url)
        sleep(1)
        # HTMLを抽出
        soup = BeautifulSoup(r.text, 'html.parser')

        elems = soup.find_all('div', class_='recipe-preview')
        for elem in elems:
            title = elem.find('a', class_='recipe-title')
            title_text = title.text
            url = 'https://cookpad.com' + title.attrs['href']
            image_url = elem.find('img').attrs['src']

        
        # レシピタイトルとURLのa要素を抽出
        # elems = soup.find_all('a', class_='recipe-title font13')
        # for elem in elems:
        #     title = elem.text
        #     url = 'https://cookpad.com' + elem.attrs['href']
        
            
        # レシピ画像のimg要素を抽出
        # contents = soup.find_all('div', class_='recipe-preview')
        # for content in contents:
        #     if content.parent
        #     image = content.find('img').attrs['src']
        #     images_list.append(image)
        #     print(image)
            d = {
                'title':title_text,
                'url':url,
                'image_url':image_url
            }

            d_lists.append(d)

        num += 1
    
    return d_lists

    # DataFrameに出力する
    # df_title_url = pd.DataFrame({'Title':titles_list, 'URL':urls_list})
    
    # return df_title_url.to_html('/templates/cookpad.html')

    # # 指定したCSVファイルに値を書き出す
    # df_title_url.to_csv('cookpad.csv', encoding='utf-8-sig')

if __name__ == '__main__':
    cookpad()