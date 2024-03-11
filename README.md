這個Project負責以下幾件事情：
1. 對ICG自己的電話錄音(ICG_dataset)進行基本前處理
2. 以Google的Speech Recognition套件進行初步轉譯
3. 將無法辨識的語音檔分類以利人工處理

關於各個文件的功能使用方式如下：
1. preprocessing1.py: 移除壞掉的檔案並將所有檔案改為單聲道
2. preprocessing2_generate_transcript.py: 以google speech recognition package生成初步的逐字稿./data/transcript.txt
3. preprocessing3.py: 將google speech recognition package無法處理的檔案移到check，並將所有檔案重新取樣
4. preprocessing4.py: 將check中的檔案移回各自在icg_dataset中所屬的資料夾
5. ICG_dataset.ipynb: 調查ICG_dataset之資料科學性質

正確執行步驟：
1. 依序執行preprocessing1.py, preprocessing2_generate_transcript.py, preprocessing3.py
2. 以人工方式處理./data/check中的語音檔並修正所有逐字稿（詳細方法如下所述）
3. 執行preprocessing4.py

上述2.中處理的方法如下：
./data/transcript.txt中有所有檔案以google speech recognition package生成初步的逐字稿。而初步處理時有問題的檔案被移到./data/check底下的各個資料夾了。這些有問題的檔案
1. ./data/check資料夾：
  (1) Cannot_resample: 無法重新取樣，這個除了刪掉以外沒有別的方法了，同時也要刪去逐字稿中的對應行
  (2) Could_not_open_file: 無法以python開啟檔案，這個除了刪掉以外沒有別的方法了，同時也要刪去逐字稿中的對應行
  (3) Could_not_understand: 代表無法辨識，須直接以人工聽寫進transcript.txt對應的位置。如果根本沒有對話，只有電話系統的聲音，請直接刪掉該檔案與transcript.txt的對應行
  (4) File_too_large: 代表檔案太大，如果這個語音檔全部都是回鈴音就刪掉，因為那會有害於我們的訓練。若大部分時間都有說話的話請每30秒剪成一段，並在transcript.txt中分別生成逐字稿。例如原本transcrpit.txt是"0101/a.wav	File_too_large"就把這行刪掉後換成 "0101/a—1.wav	xxxx..." "0101/a—2.wav	yyyy..." "0101/a—3.wav	zzzz..."...依此類推
  (5) Need_verification: 代表無法辨識，須直接以人工聽寫進transcript.txt對應的位置，若只有電話系統的聲音，請直接刪掉該檔案與transcript.txt的對應行
  處理以上檔案時，不要移動任何檔案，修正逐字稿時也不要添加任何標點符號
2. ./data/ICG_dataset: 這些檔案是能正常被語音辨識的檔案，請一個一個打開來聽並修正./data/transcript.txt中對應的逐字稿，過程中不要移動任何檔案，修正逐字稿時也不要添加任何標點符號

