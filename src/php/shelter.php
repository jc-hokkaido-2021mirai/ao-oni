<!doctype html>

<link rel="stylesheet" href="design.css">

<html lang="ja">

        <head>
                <meta charset="UTF-8">
                <title>
                        避難所 状況
                </title>
        </head>

        <body>
                <h1><span>避難所 状況確認</span></h1>

		<h2><span>・</span>避難所 風景</h2>

		<img src="https://storageaccounttest91a3.blob.core.windows.net/climbanother/img_rectangle.png">

		<h2><span>・</span>避難所 状況</h2>

		<?php
			// 人数取得・表示
			$get_Url = curl_init("https://storageaccounttest91a3.blob.core.windows.net/climbanother-results/count.json");
			curl_setopt($get_Url, CURLOPT_HEADER, 0);
			echo "・人数　　：";
			curl_exec($get_Url);
			curl_close($get_Url);
	
			// ケージ数取得・表示
			$get_Url = curl_init("https://storageaccounttest91a3.blob.core.windows.net/climbanother-results/cagedata.json");
			curl_setopt($get_Url, CURLOPT_HEADER, 0);
			echo "<br />・ペット数：";
			curl_exec($get_Url);
			curl_close($get_Url);
		?>

		<h2><span>・</span><a href="index.html">TOPページ</a></h2>
	</body>
</html>
