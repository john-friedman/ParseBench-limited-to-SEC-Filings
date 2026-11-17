# ParseBench limited to SEC Filings

More than 7% of [ParseBench](https://github.com/run-llama/ParseBench) is from SEC Filings. This is neat, because SEC Filings usually have either a html version or a pdf version with underlying text. 

This allows me to test [doc2struct](https://github.com/john-friedman/doc2struct)'s performance. doc2struct is an algorithmic document parser that parses millions of pages of text per second, on a single thread (cpu). It does not parse images or pdfs without underlying text structure. It costs a few cents in compute to parse the entire SEC corpus using AWS Spot instances.


## data

Consists of {metric}/{case}/

- parsebench_input.pdf: original ParseBench input
- sec_input.{filetype}: paired SEC input
- expected.json: expected output of document parser

Pairing was done using GPT Sol 6.1, and may have bugs.

## benchmark 

As of 11/16/2026

| Rank | Provider | Category | Overall | Text | Formatting | Tables | Charts | Visual Ground. | Forms | ¢ / Page |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | LlamaParse (Agentic Plus) | Document Parsers | 90.09 | 90.27 | 93.60 | 94.72 | 92.58 | 87.62 | 81.76 | 2.81¢ |
| **2†** | **doc2struct** | **Document Parsers** | **88.84†** | **83.33** | **94.85** | **88.32** | **—** | **—** | **—** | **0¢** |
| 3 | LlamaParse (Agentic) | Document Parsers | 86.06 | 87.01 | 92.75 | 89.90 | 77.39 | 88.35 | 80.94 | 1.25¢ |
| 4 | Claude Opus 5.5 | Vision Models | 85.75 | 92.71 | 89.38 | 94.20 | 74.12 | 86.24 | 77.83 | 6.49¢ |
| 5 | Reducto (r-1) | Document Parsers | 85.23 | 82.49 | 92.45 | 90.97 | 78.45 | 88.74 | 78.30 | 1.00¢ |
| 6 | LlamaParse (Cost Effective) | Document Parsers | 84.60 | 85.50 | 91.94 | 87.22 | 73.07 | 88.66 | 81.21 | 0.38¢ |
| 7 | Gemini 4 argon (low) | Vision Models | 84.20 | 89.68 | 89.22 | 92.85 | 68.20 | 88.10 | 77.18 | 2.68¢ |
| 8 | Reducto | Document Parsers | 83.92 | 81.86 | 82.70 | 84.92 | 89.07 | 84.10 | 80.88 | 3.00¢ |
| 9 | Extend (Parse 2) | Document Parsers | 83.20 | 80.18 | 83.39 | 84.20 | 85.08 | 84.82 | 81.52 | 2.50¢ |
| 10 | Pulse (Ultra 2) | Document Parsers | 82.73 | 86.09 | 88.68 | 84.80 | 86.80 | 73.54 | 76.50 | 1.50¢ |
| 11 | Extend (Parse Light) | Document Parsers | 81.58 | 78.29 | 78.65 | 81.39 | 85.35 | 84.66 | 81.16 | 0.62¢ |

† Doc2struct's **88.84 partial score** is the unweighted mean of its limited dimensions. PDF tables are excluded, as doc2struct currently lacks table parsing support for PDFs. Other models scores are their full scores on the full ParseBench. Apples to oranges!


## doc2struct scores by metric

| Subset | Included cases | Excluded PDF tables | Primary metric | Mean score |
|---|---:|---:|---|---:|
| complex_table_headers | 4 | 0 | `table_next` | **99.59%** |
| dense_tables | 23 | 4 | `table_next` | **87.00%** |
| financial_tables | 94 | 24 | `table_next` | **81.97%** |
| tables | 86 | 9 | `table_next` | **95.10%** |
| headings | 11 | 0 | `formatting_v2` | **96.08%** |
| text | 6 | 0 | `text_next` | **83.33%** |

## doc2struct scores by case

261 cases. 37 excluded PDF tables.

<details>
<summary>Show all 261 cases</summary>

| Case / result | SEC input | Primary score |
|---|---|---:|
| [complex_table_headers/055](runs/doc2struct/complex_table_headers/055/result.md) | HTML | 100.00% |
| [complex_table_headers/068](runs/doc2struct/complex_table_headers/068/result.md) | HTML | 100.00% |
| [complex_table_headers/090](runs/doc2struct/complex_table_headers/090/result.md) | HTML | 100.00% |
| [complex_table_headers/097](runs/doc2struct/complex_table_headers/097/result.md) | HTML | 98.35% |
| [dense_tables/141](runs/doc2struct/dense_tables/141/result.md) | HTML | 94.00% |
| [dense_tables/346](runs/doc2struct/dense_tables/346/result.md) | HTML | 52.85% |
| [dense_tables/360](runs/doc2struct/dense_tables/360/result.md) | PDF | Excluded (PDF table) |
| [dense_tables/382](runs/doc2struct/dense_tables/382/result.md) | HTML | 100.00% |
| [dense_tables/383](runs/doc2struct/dense_tables/383/result.md) | HTML | 100.00% |
| [dense_tables/387](runs/doc2struct/dense_tables/387/result.md) | HTML | 0.00% |
| [dense_tables/391](runs/doc2struct/dense_tables/391/result.md) | HTML | 73.80% |
| [dense_tables/395](runs/doc2struct/dense_tables/395/result.md) | HTML | 100.00% |
| [dense_tables/400](runs/doc2struct/dense_tables/400/result.md) | HTML | 39.90% |
| [dense_tables/406](runs/doc2struct/dense_tables/406/result.md) | HTML | 81.61% |
| [dense_tables/412](runs/doc2struct/dense_tables/412/result.md) | HTML | 94.02% |
| [dense_tables/415](runs/doc2struct/dense_tables/415/result.md) | HTML | 100.00% |
| [dense_tables/421](runs/doc2struct/dense_tables/421/result.md) | HTML | 72.73% |
| [dense_tables/430](runs/doc2struct/dense_tables/430/result.md) | HTML | 100.00% |
| [dense_tables/434](runs/doc2struct/dense_tables/434/result.md) | HTML | 100.00% |
| [dense_tables/438](runs/doc2struct/dense_tables/438/result.md) | PDF | Excluded (PDF table) |
| [dense_tables/444](runs/doc2struct/dense_tables/444/result.md) | PDF | Excluded (PDF table) |
| [dense_tables/445](runs/doc2struct/dense_tables/445/result.md) | HTML | 100.00% |
| [dense_tables/449](runs/doc2struct/dense_tables/449/result.md) | HTML | 100.00% |
| [dense_tables/458](runs/doc2struct/dense_tables/458/result.md) | HTML | 100.00% |
| [dense_tables/459](runs/doc2struct/dense_tables/459/result.md) | HTML | 100.00% |
| [dense_tables/461](runs/doc2struct/dense_tables/461/result.md) | HTML | 100.00% |
| [dense_tables/465](runs/doc2struct/dense_tables/465/result.md) | HTML | 100.00% |
| [dense_tables/470](runs/doc2struct/dense_tables/470/result.md) | HTML | 100.00% |
| [dense_tables/478](runs/doc2struct/dense_tables/478/result.md) | HTML | 100.00% |
| [dense_tables/487](runs/doc2struct/dense_tables/487/result.md) | PDF | Excluded (PDF table) |
| [dense_tables/492](runs/doc2struct/dense_tables/492/result.md) | HTML | 92.18% |
| [financial_tables/001](runs/doc2struct/financial_tables/001/result.md) | HTML | 84.00% |
| [financial_tables/002](runs/doc2struct/financial_tables/002/result.md) | HTML | 90.00% |
| [financial_tables/003](runs/doc2struct/financial_tables/003/result.md) | HTML | 98.18% |
| [financial_tables/004](runs/doc2struct/financial_tables/004/result.md) | HTML | 100.00% |
| [financial_tables/005](runs/doc2struct/financial_tables/005/result.md) | HTML | 75.13% |
| [financial_tables/006](runs/doc2struct/financial_tables/006/result.md) | HTML | 100.00% |
| [financial_tables/007](runs/doc2struct/financial_tables/007/result.md) | HTML | 100.00% |
| [financial_tables/008](runs/doc2struct/financial_tables/008/result.md) | HTML | 100.00% |
| [financial_tables/009](runs/doc2struct/financial_tables/009/result.md) | HTML | 99.00% |
| [financial_tables/010](runs/doc2struct/financial_tables/010/result.md) | HTML | 99.00% |
| [financial_tables/011](runs/doc2struct/financial_tables/011/result.md) | HTML | 90.88% |
| [financial_tables/012](runs/doc2struct/financial_tables/012/result.md) | HTML | 100.00% |
| [financial_tables/013](runs/doc2struct/financial_tables/013/result.md) | HTML | 99.00% |
| [financial_tables/014](runs/doc2struct/financial_tables/014/result.md) | HTML | 95.00% |
| [financial_tables/015](runs/doc2struct/financial_tables/015/result.md) | HTML | 100.00% |
| [financial_tables/016](runs/doc2struct/financial_tables/016/result.md) | HTML | 47.83% |
| [financial_tables/017](runs/doc2struct/financial_tables/017/result.md) | HTML | 72.00% |
| [financial_tables/018](runs/doc2struct/financial_tables/018/result.md) | HTML | 100.00% |
| [financial_tables/019](runs/doc2struct/financial_tables/019/result.md) | HTML | 44.81% |
| [financial_tables/020](runs/doc2struct/financial_tables/020/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/021](runs/doc2struct/financial_tables/021/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/022](runs/doc2struct/financial_tables/022/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/023](runs/doc2struct/financial_tables/023/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/024](runs/doc2struct/financial_tables/024/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/025](runs/doc2struct/financial_tables/025/result.md) | HTML | 100.00% |
| [financial_tables/026](runs/doc2struct/financial_tables/026/result.md) | HTML | 84.00% |
| [financial_tables/027](runs/doc2struct/financial_tables/027/result.md) | HTML | 99.00% |
| [financial_tables/028](runs/doc2struct/financial_tables/028/result.md) | HTML | 100.00% |
| [financial_tables/029](runs/doc2struct/financial_tables/029/result.md) | HTML | 94.00% |
| [financial_tables/030](runs/doc2struct/financial_tables/030/result.md) | HTML | 100.00% |
| [financial_tables/031](runs/doc2struct/financial_tables/031/result.md) | HTML | 99.00% |
| [financial_tables/032](runs/doc2struct/financial_tables/032/result.md) | HTML | 100.00% |
| [financial_tables/033](runs/doc2struct/financial_tables/033/result.md) | HTML | 14.47% |
| [financial_tables/034](runs/doc2struct/financial_tables/034/result.md) | HTML | 74.00% |
| [financial_tables/035](runs/doc2struct/financial_tables/035/result.md) | HTML | 69.96% |
| [financial_tables/036](runs/doc2struct/financial_tables/036/result.md) | HTML | 100.00% |
| [financial_tables/037](runs/doc2struct/financial_tables/037/result.md) | HTML | 95.73% |
| [financial_tables/038](runs/doc2struct/financial_tables/038/result.md) | HTML | 93.33% |
| [financial_tables/039](runs/doc2struct/financial_tables/039/result.md) | HTML | 95.00% |
| [financial_tables/040](runs/doc2struct/financial_tables/040/result.md) | HTML | 96.00% |
| [financial_tables/041](runs/doc2struct/financial_tables/041/result.md) | HTML | 99.00% |
| [financial_tables/042](runs/doc2struct/financial_tables/042/result.md) | HTML | 100.00% |
| [financial_tables/043](runs/doc2struct/financial_tables/043/result.md) | HTML | 99.00% |
| [financial_tables/044](runs/doc2struct/financial_tables/044/result.md) | HTML | 100.00% |
| [financial_tables/045](runs/doc2struct/financial_tables/045/result.md) | HTML | 100.00% |
| [financial_tables/046](runs/doc2struct/financial_tables/046/result.md) | HTML | 100.00% |
| [financial_tables/047](runs/doc2struct/financial_tables/047/result.md) | HTML | 100.00% |
| [financial_tables/048](runs/doc2struct/financial_tables/048/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/049](runs/doc2struct/financial_tables/049/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/050](runs/doc2struct/financial_tables/050/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/051](runs/doc2struct/financial_tables/051/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/052](runs/doc2struct/financial_tables/052/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/053](runs/doc2struct/financial_tables/053/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/054](runs/doc2struct/financial_tables/054/result.md) | HTML | 99.00% |
| [financial_tables/055](runs/doc2struct/financial_tables/055/result.md) | HTML | 100.00% |
| [financial_tables/056](runs/doc2struct/financial_tables/056/result.md) | HTML | 100.00% |
| [financial_tables/057](runs/doc2struct/financial_tables/057/result.md) | HTML | 0.00% |
| [financial_tables/058](runs/doc2struct/financial_tables/058/result.md) | HTML | 97.97% |
| [financial_tables/059](runs/doc2struct/financial_tables/059/result.md) | HTML | 67.89% |
| [financial_tables/060](runs/doc2struct/financial_tables/060/result.md) | HTML | 99.00% |
| [financial_tables/061](runs/doc2struct/financial_tables/061/result.md) | HTML | 100.00% |
| [financial_tables/062](runs/doc2struct/financial_tables/062/result.md) | HTML | 100.00% |
| [financial_tables/063](runs/doc2struct/financial_tables/063/result.md) | HTML | 100.00% |
| [financial_tables/064](runs/doc2struct/financial_tables/064/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/065](runs/doc2struct/financial_tables/065/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/066](runs/doc2struct/financial_tables/066/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/067](runs/doc2struct/financial_tables/067/result.md) | HTML | 100.00% |
| [financial_tables/068](runs/doc2struct/financial_tables/068/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/069](runs/doc2struct/financial_tables/069/result.md) | HTML | 100.00% |
| [financial_tables/070](runs/doc2struct/financial_tables/070/result.md) | HTML | 56.78% |
| [financial_tables/071](runs/doc2struct/financial_tables/071/result.md) | HTML | 100.00% |
| [financial_tables/072](runs/doc2struct/financial_tables/072/result.md) | HTML | 95.00% |
| [financial_tables/073](runs/doc2struct/financial_tables/073/result.md) | HTML | 100.00% |
| [financial_tables/074](runs/doc2struct/financial_tables/074/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/075](runs/doc2struct/financial_tables/075/result.md) | HTML | 100.00% |
| [financial_tables/076](runs/doc2struct/financial_tables/076/result.md) | HTML | 0.00% |
| [financial_tables/077](runs/doc2struct/financial_tables/077/result.md) | HTML | 100.00% |
| [financial_tables/078](runs/doc2struct/financial_tables/078/result.md) | HTML | 100.00% |
| [financial_tables/079](runs/doc2struct/financial_tables/079/result.md) | HTML | 90.00% |
| [financial_tables/080](runs/doc2struct/financial_tables/080/result.md) | HTML | 0.00% |
| [financial_tables/081](runs/doc2struct/financial_tables/081/result.md) | HTML | 91.55% |
| [financial_tables/082](runs/doc2struct/financial_tables/082/result.md) | HTML | 100.00% |
| [financial_tables/083](runs/doc2struct/financial_tables/083/result.md) | HTML | 100.00% |
| [financial_tables/084](runs/doc2struct/financial_tables/084/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/085](runs/doc2struct/financial_tables/085/result.md) | HTML | 0.00% |
| [financial_tables/086](runs/doc2struct/financial_tables/086/result.md) | HTML | 77.06% |
| [financial_tables/087](runs/doc2struct/financial_tables/087/result.md) | HTML | 0.00% |
| [financial_tables/088](runs/doc2struct/financial_tables/088/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/089](runs/doc2struct/financial_tables/089/result.md) | HTML | 85.00% |
| [financial_tables/090](runs/doc2struct/financial_tables/090/result.md) | HTML | 88.64% |
| [financial_tables/091](runs/doc2struct/financial_tables/091/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/092](runs/doc2struct/financial_tables/092/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/093](runs/doc2struct/financial_tables/093/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/094](runs/doc2struct/financial_tables/094/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/095](runs/doc2struct/financial_tables/095/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/096](runs/doc2struct/financial_tables/096/result.md) | PDF | Excluded (PDF table) |
| [financial_tables/097](runs/doc2struct/financial_tables/097/result.md) | HTML | 92.00% |
| [financial_tables/098](runs/doc2struct/financial_tables/098/result.md) | HTML | 0.00% |
| [financial_tables/099](runs/doc2struct/financial_tables/099/result.md) | HTML | 0.00% |
| [financial_tables/100](runs/doc2struct/financial_tables/100/result.md) | HTML | 86.52% |
| [financial_tables/101](runs/doc2struct/financial_tables/101/result.md) | HTML | 100.00% |
| [financial_tables/102](runs/doc2struct/financial_tables/102/result.md) | HTML | 40.00% |
| [financial_tables/103](runs/doc2struct/financial_tables/103/result.md) | HTML | 0.00% |
| [financial_tables/104](runs/doc2struct/financial_tables/104/result.md) | HTML | 100.00% |
| [financial_tables/105](runs/doc2struct/financial_tables/105/result.md) | HTML | 92.86% |
| [financial_tables/106](runs/doc2struct/financial_tables/106/result.md) | HTML | 86.43% |
| [financial_tables/107](runs/doc2struct/financial_tables/107/result.md) | HTML | 80.71% |
| [financial_tables/108](runs/doc2struct/financial_tables/108/result.md) | HTML | 80.39% |
| [financial_tables/109](runs/doc2struct/financial_tables/109/result.md) | HTML | 71.46% |
| [financial_tables/110](runs/doc2struct/financial_tables/110/result.md) | HTML | 74.80% |
| [financial_tables/111](runs/doc2struct/financial_tables/111/result.md) | HTML | 66.53% |
| [financial_tables/112](runs/doc2struct/financial_tables/112/result.md) | HTML | 100.00% |
| [financial_tables/113](runs/doc2struct/financial_tables/113/result.md) | HTML | 0.00% |
| [financial_tables/114](runs/doc2struct/financial_tables/114/result.md) | HTML | 100.00% |
| [financial_tables/115](runs/doc2struct/financial_tables/115/result.md) | HTML | 100.00% |
| [financial_tables/116](runs/doc2struct/financial_tables/116/result.md) | HTML | 95.00% |
| [financial_tables/117](runs/doc2struct/financial_tables/117/result.md) | HTML | 83.22% |
| [financial_tables/118](runs/doc2struct/financial_tables/118/result.md) | HTML | 100.00% |
| [headings/0006](runs/doc2struct/headings/0006/result.md) | HTML | 100.00% |
| [headings/0010](runs/doc2struct/headings/0010/result.md) | TXT | 100.00% |
| [headings/0011](runs/doc2struct/headings/0011/result.md) | HTML | 90.00% |
| [headings/0016](runs/doc2struct/headings/0016/result.md) | HTML | 96.00% |
| [headings/0018](runs/doc2struct/headings/0018/result.md) | HTML | 100.00% |
| [headings/0021](runs/doc2struct/headings/0021/result.md) | HTML | 100.00% |
| [headings/0026](runs/doc2struct/headings/0026/result.md) | HTML | 96.00% |
| [headings/0032](runs/doc2struct/headings/0032/result.md) | HTML | 87.50% |
| [headings/0035](runs/doc2struct/headings/0035/result.md) | HTML | 96.00% |
| [headings/0039](runs/doc2struct/headings/0039/result.md) | HTML | 91.43% |
| [headings/0043](runs/doc2struct/headings/0043/result.md) | HTML | 100.00% |
| [tables/001](runs/doc2struct/tables/001/result.md) | HTML | 95.00% |
| [tables/002](runs/doc2struct/tables/002/result.md) | HTML | 100.00% |
| [tables/003](runs/doc2struct/tables/003/result.md) | HTML | 100.00% |
| [tables/004](runs/doc2struct/tables/004/result.md) | HTML | 100.00% |
| [tables/005](runs/doc2struct/tables/005/result.md) | HTML | 99.00% |
| [tables/006](runs/doc2struct/tables/006/result.md) | HTML | 95.00% |
| [tables/007](runs/doc2struct/tables/007/result.md) | HTML | 100.00% |
| [tables/008](runs/doc2struct/tables/008/result.md) | HTML | 80.00% |
| [tables/009](runs/doc2struct/tables/009/result.md) | HTML | 100.00% |
| [tables/010](runs/doc2struct/tables/010/result.md) | HTML | 100.00% |
| [tables/011](runs/doc2struct/tables/011/result.md) | HTML | 100.00% |
| [tables/012](runs/doc2struct/tables/012/result.md) | HTML | 100.00% |
| [tables/013](runs/doc2struct/tables/013/result.md) | HTML | 100.00% |
| [tables/014](runs/doc2struct/tables/014/result.md) | HTML | 99.00% |
| [tables/015](runs/doc2struct/tables/015/result.md) | HTML | 100.00% |
| [tables/016](runs/doc2struct/tables/016/result.md) | HTML | 100.00% |
| [tables/017](runs/doc2struct/tables/017/result.md) | HTML | 100.00% |
| [tables/018](runs/doc2struct/tables/018/result.md) | HTML | 100.00% |
| [tables/019](runs/doc2struct/tables/019/result.md) | HTML | 58.64% |
| [tables/020](runs/doc2struct/tables/020/result.md) | HTML | 100.00% |
| [tables/021](runs/doc2struct/tables/021/result.md) | HTML | 100.00% |
| [tables/022](runs/doc2struct/tables/022/result.md) | HTML | 100.00% |
| [tables/023](runs/doc2struct/tables/023/result.md) | HTML | 100.00% |
| [tables/024](runs/doc2struct/tables/024/result.md) | HTML | 100.00% |
| [tables/025](runs/doc2struct/tables/025/result.md) | HTML | 100.00% |
| [tables/026](runs/doc2struct/tables/026/result.md) | HTML | 100.00% |
| [tables/027](runs/doc2struct/tables/027/result.md) | HTML | 100.00% |
| [tables/028](runs/doc2struct/tables/028/result.md) | HTML | 100.00% |
| [tables/029](runs/doc2struct/tables/029/result.md) | HTML | 100.00% |
| [tables/030](runs/doc2struct/tables/030/result.md) | HTML | 87.66% |
| [tables/031](runs/doc2struct/tables/031/result.md) | HTML | 100.00% |
| [tables/032](runs/doc2struct/tables/032/result.md) | HTML | 100.00% |
| [tables/033](runs/doc2struct/tables/033/result.md) | HTML | 56.21% |
| [tables/034](runs/doc2struct/tables/034/result.md) | HTML | 100.00% |
| [tables/035](runs/doc2struct/tables/035/result.md) | HTML | 100.00% |
| [tables/036](runs/doc2struct/tables/036/result.md) | HTML | 100.00% |
| [tables/037](runs/doc2struct/tables/037/result.md) | HTML | 100.00% |
| [tables/038](runs/doc2struct/tables/038/result.md) | HTML | 100.00% |
| [tables/039](runs/doc2struct/tables/039/result.md) | HTML | 100.00% |
| [tables/040](runs/doc2struct/tables/040/result.md) | HTML | 0.00% |
| [tables/041](runs/doc2struct/tables/041/result.md) | HTML | 100.00% |
| [tables/042](runs/doc2struct/tables/042/result.md) | HTML | 95.00% |
| [tables/043](runs/doc2struct/tables/043/result.md) | HTML | 90.00% |
| [tables/044](runs/doc2struct/tables/044/result.md) | HTML | 95.00% |
| [tables/045](runs/doc2struct/tables/045/result.md) | HTML | 100.00% |
| [tables/046](runs/doc2struct/tables/046/result.md) | HTML | 100.00% |
| [tables/047](runs/doc2struct/tables/047/result.md) | HTML | 95.00% |
| [tables/048](runs/doc2struct/tables/048/result.md) | HTML | 99.00% |
| [tables/049](runs/doc2struct/tables/049/result.md) | HTML | 100.00% |
| [tables/050](runs/doc2struct/tables/050/result.md) | HTML | 100.00% |
| [tables/051](runs/doc2struct/tables/051/result.md) | HTML | 100.00% |
| [tables/052](runs/doc2struct/tables/052/result.md) | HTML | 100.00% |
| [tables/053](runs/doc2struct/tables/053/result.md) | HTML | 100.00% |
| [tables/054](runs/doc2struct/tables/054/result.md) | HTML | 100.00% |
| [tables/055](runs/doc2struct/tables/055/result.md) | HTML | 100.00% |
| [tables/056](runs/doc2struct/tables/056/result.md) | HTML | 100.00% |
| [tables/058](runs/doc2struct/tables/058/result.md) | HTML | 74.00% |
| [tables/059](runs/doc2struct/tables/059/result.md) | HTML | 0.33% |
| [tables/060](runs/doc2struct/tables/060/result.md) | HTML | 100.00% |
| [tables/061](runs/doc2struct/tables/061/result.md) | HTML | 100.00% |
| [tables/062](runs/doc2struct/tables/062/result.md) | HTML | 100.00% |
| [tables/063](runs/doc2struct/tables/063/result.md) | HTML | 100.00% |
| [tables/064](runs/doc2struct/tables/064/result.md) | HTML | 100.00% |
| [tables/065](runs/doc2struct/tables/065/result.md) | HTML | 100.00% |
| [tables/066](runs/doc2struct/tables/066/result.md) | HTML | 100.00% |
| [tables/067](runs/doc2struct/tables/067/result.md) | PDF | Excluded (PDF table) |
| [tables/068](runs/doc2struct/tables/068/result.md) | PDF | Excluded (PDF table) |
| [tables/069](runs/doc2struct/tables/069/result.md) | PDF | Excluded (PDF table) |
| [tables/070](runs/doc2struct/tables/070/result.md) | HTML | 95.00% |
| [tables/071](runs/doc2struct/tables/071/result.md) | HTML | 100.00% |
| [tables/072](runs/doc2struct/tables/072/result.md) | HTML | 100.00% |
| [tables/073](runs/doc2struct/tables/073/result.md) | HTML | 100.00% |
| [tables/074](runs/doc2struct/tables/074/result.md) | HTML | 95.00% |
| [tables/075](runs/doc2struct/tables/075/result.md) | PDF | Excluded (PDF table) |
| [tables/076](runs/doc2struct/tables/076/result.md) | PDF | Excluded (PDF table) |
| [tables/077](runs/doc2struct/tables/077/result.md) | PDF | Excluded (PDF table) |
| [tables/078](runs/doc2struct/tables/078/result.md) | PDF | Excluded (PDF table) |
| [tables/079](runs/doc2struct/tables/079/result.md) | PDF | Excluded (PDF table) |
| [tables/080](runs/doc2struct/tables/080/result.md) | PDF | Excluded (PDF table) |
| [tables/081](runs/doc2struct/tables/081/result.md) | HTML | 94.00% |
| [tables/082](runs/doc2struct/tables/082/result.md) | HTML | 100.00% |
| [tables/083](runs/doc2struct/tables/083/result.md) | HTML | 100.00% |
| [tables/084](runs/doc2struct/tables/084/result.md) | HTML | 100.00% |
| [tables/085](runs/doc2struct/tables/085/result.md) | HTML | 90.00% |
| [tables/086](runs/doc2struct/tables/086/result.md) | HTML | 100.00% |
| [tables/087](runs/doc2struct/tables/087/result.md) | HTML | 95.65% |
| [tables/088](runs/doc2struct/tables/088/result.md) | HTML | 100.00% |
| [tables/089](runs/doc2struct/tables/089/result.md) | HTML | 100.00% |
| [tables/090](runs/doc2struct/tables/090/result.md) | HTML | 100.00% |
| [tables/091](runs/doc2struct/tables/091/result.md) | HTML | 100.00% |
| [tables/092](runs/doc2struct/tables/092/result.md) | HTML | 95.00% |
| [tables/093](runs/doc2struct/tables/093/result.md) | HTML | 100.00% |
| [tables/094](runs/doc2struct/tables/094/result.md) | HTML | 100.00% |
| [tables/095](runs/doc2struct/tables/095/result.md) | HTML | 100.00% |
| [tables/096](runs/doc2struct/tables/096/result.md) | HTML | 95.00% |
| [text/001](runs/doc2struct/text/001/result.md) | HTML | 100.00% |
| [text/002](runs/doc2struct/text/002/result.md) | PDF | 100.00% |
| [text/003](runs/doc2struct/text/003/result.md) | HTML | 100.00% |
| [text/004](runs/doc2struct/text/004/result.md) | HTML | 100.00% |
| [text/005](runs/doc2struct/text/005/result.md) | PDF | 0.00% |
| [text/006](runs/doc2struct/text/006/result.md) | HTML | 100.00% |

</details>

# Acknowledgments

Thank you to [LlamaIndex](https://www.llamaindex.ai/) for releasing a neat parsing benchmark!