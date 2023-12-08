'''


                     /$$$$$$$                            /$$ /$$                     /$$$$$$$  /$$                                       
                    | $$__  $$                          | $$|__/                    | $$__  $$|__/                                       
                    | $$  \ $$  /$$$$$$   /$$$$$$   /$$$$$$$ /$$ /$$$$$$$   /$$$$$$ | $$  \ $$ /$$  /$$$$$$                              
                    | $$$$$$$/ /$$__  $$ |____  $$ /$$__  $$| $$| $$__  $$ /$$__  $$| $$$$$$$/| $$ |____  $$                             
                    | $$__  $$| $$$$$$$$  /$$$$$$$| $$  | $$| $$| $$  \ $$| $$  \ $$| $$____/ | $$  /$$$$$$$                             
                    | $$  \ $$| $$_____/ /$$__  $$| $$  | $$| $$| $$  | $$| $$  | $$| $$      | $$ /$$__  $$                             
                    | $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$| $$  | $$|  $$$$$$$| $$      | $$|  $$$$$$$                             
                    |__/  |__/ \_______/ \_______/ \_______/|__/|__/  |__/ \____  $$|__/      |__/ \_______/                             
                                                                           /$$  \ $$                                                     
                                                                          |  $$$$$$/                                                     
                                                                           \______/                                                      
         /$$   /$$                               /$$        /$$$$$$                                                                      
        | $$$ | $$                              | $$       /$$__  $$                                                                     
        | $$$$| $$  /$$$$$$  /$$    /$$ /$$$$$$ | $$      | $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
        | $$ $$ $$ /$$__  $$|  $$  /$$//$$__  $$| $$      |  $$$$$$  /$$_____/ /$$__  $$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
        | $$  $$$$| $$  \ $$ \  $$/$$/| $$$$$$$$| $$       \____  $$| $$      | $$  \__/ /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
        | $$\  $$$| $$  | $$  \  $$$/ | $$_____/| $$       /$$  \ $$| $$      | $$      /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$      
        | $$ \  $$|  $$$$$$/   \  $/  |  $$$$$$$| $$      |  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/| $$$$$$$/|  $$$$$$$| $$      
        |__/  \__/ \______/     \_/    \_______/|__/       \______/  \_______/|__/      \_______/| $$____/ | $$____/  \_______/|__/      
                                                                                                | $$      | $$                          
                                                                                                | $$      | $$                          
                                                                                                |__/      |__/                          
    
    #READINGPIA.ME NOVEL SCRAPPER
    
    # Scrape any Novel from readingpia.me into pdf.
    
    # Build and maintained:
    
                                                 .x+=:.                                                     ..          .x+=:.   
                        xeee    dL ud8Nu  :8c   z`    ^%                                                  dF           z`    ^%  
                       d888R    8Fd888888L %8      .   <k                             u.      u.    u.   '88bu.           .   <k 
                      d8888R    4N88888888cuR    .@8Ned8"      .u          .    ...ue888b   x@88k u@88c. '*88888bu      .@8Ned8" 
                     @ 8888R    4F   ^""%""d   .@^%8888"    ud8888.   .udR88N   888R Y888r ^"8888""8888"   ^"*8888N   .@^%8888"  
                   .P  8888R    d       .z8   x88:  `)8b. :888'8888. <888'888k  888R I888>   8888  888R   beWE "888L x88:  `)8b. 
                  :F   8888R    ^     z888    8888N=*8888 d888 '88%" 9888 'Y"   888R I888>   8888  888R   888E  888E 8888N=*8888 
                 x"    8888R        d8888'     %8"    R88 8888.+"    9888       888R I888>   8888  888R   888E  888E  %8"    R88 
                d8eeeee88888eer    888888       @8Wou 9%  8888L      9888      u8888cJ888    8888  888R   888E  888F   @8Wou 9%  
                       8888R      :888888     .888888P`   '8888c. .+ ?8888u../  "*888*P"    "*88*" 8888" .888N..888  .888888P`   
                       8888R       888888     `   ^"F      "88888%    "8888P'     'Y"         ""   'Y"    `"888*""   `   ^"F     
                    "*%%%%%%**~    '%**%                     "YP'       "P'                                  ""                  


'''


import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import shutil
from fpdf import FPDF
from PyPDF2 import PdfMerger 

def get_title(soup):
    title = soup.find("title").text
    
    return title

def check_initial(soup):  
    data = soup.find_all("td")
    initial = data[-2].text
    
    return int(initial)

def check_final(soup):
    data = soup.find("td")
    final = data.text
    
    return int(final)

def new_url(soup):    
    link_row = soup.find_all("td")[1]
    link_row_data = link_row.find('a')
    relative_chapter_link = str(link_row_data.get('href'))
    iterable = relative_chapter_link.split("-")[:-1]
    iterable_relative_chapter_link_temp = ""
    for word in iterable:
        iterable_relative_chapter_link_temp = "-".join([iterable_relative_chapter_link_temp, word])
    iterable_relative_chapter_link = iterable_relative_chapter_link_temp[1:]
    chapter_link = "".join(["https://readingpia.me", iterable_relative_chapter_link, "-"])
    
    return chapter_link

def extract_chapter(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    
    data = soup.find(attrs={'id':'chapter-body'})
    chapter_raw = data.text
    chapter_formated = chapter_raw.replace('<br>', '\n').replace('&nbsp;', '')
    chapter = unidecode(chapter_formated)
    return chapter

def save_chapter(chapter, i):
    with open(f'Chapter {i}.txt', 'w') as file:
        file.write(chapter)

def txt_to_pdf(temp_file_path, temp_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("helvetica", size = 12)
    
    with open(temp_file_path, 'r') as text_file:
        text_content = text_file.read()
    
    pdf.multi_cell(0, 10, text_content)
    pdf.output(temp_pdf_path)

def merge_pdf(pdf_files_list, output_folder, title):
    merger = PdfMerger()
    
    for pdf_chapter in pdf_files_list:
        merger.append(pdf_chapter)
    
    os.chdir(output_folder)
    merger.write(f"{title}.pdf")
    merger.close()

def delete_temp_folder(temp_folder_path):
    try:
        shutil.rmtree(temp_folder_path)
    except Exception:
        pass

def main():
    url = input("Enter the url of Novel from readingpia.me : ")
    try:
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
    except Exception as error:
        print(f"Something went wrong.\nlog : {error}")
    
    initial = input("From which chapter (press enter for default [starting 0/1]) : ")
    if initial == "":
        initial = check_initial(soup)
        print(initial)
    else:
        initial = int(initial)
    
    final = input("From which chapter (press enter for default [last]) : ")
    if final == "":
        final = check_final(soup)
        print(final)
    else:
        final = int(final)
        
    title = get_title(soup)
    
    url = new_url(soup)
    print(url)
    
    current_folder = str(os.getcwd())
    temp_folder = ".temp"
    output_folder = "My_Novels"
    
    try:
        os.mkdir(temp_folder)
        os.mkdir(output_folder)
        
    except Exception:
        pass
                
    os.chdir(str(os.path.join(temp_folder)))
    for i in range (initial,final+1):
        current_url = "".join([url, str(i)])
        print(f"Processing Chapter {i}...")
        print(current_url)
        
        chapter = extract_chapter(current_url)
        save_chapter(chapter ,i)
    
    for raw_chapter_file in os.listdir(str(os.getcwd())):
        if raw_chapter_file.endswith(".txt"):
            temp_file_path = os.path.join(raw_chapter_file)
            temp_pdf_path = os.path.join(raw_chapter_file.replace(".txt", ".pdf"))
            txt_to_pdf(temp_file_path, temp_pdf_path)
    
    pdf_files_list = [os.path.join(temp_folder, pdf_chapter) for pdf_chapter in os.listdir(str(os.getcwd())) if pdf_chapter.endswith(".pdf")]
    
    
    os.chdir(current_folder)
    merge_pdf(pdf_files_list, str(os.path.join(output_folder)), title)
    
    delete_temp_folder(os.path.join(current_folder, temp_folder))
    
    print("\nAll Done!\n")
    
if __name__ == "__main__":
    main()


'''


    .S_SsS_S.    .S  S.        sSSs          sSSs   .S_sSSs            sSSs   .S       S.    .S_sSSs    sdSS_SSSSSSbs   .S    sSSs 
   .SS~S*S~SS.  .SS  SS.      d%%SP         d%%SP  .SS~YS%%b          d%%SP  .SS       SS.  .SS~YS%%b   YSSS~S%SSSSSP  .SS   d%%SP 
   S%S `Y' S%S  S%S  S%S     d%S'          d%S'    S%S   `S%b        d%S'    S%S       S%S  S%S   `S%b       S%S       S%S  d%S' 
   S%S     S%S  S%S  S%S     S%S           S%S     S%S    S%S        S%S     S%S       S%S  S%S    S%S       S%S       S%S  S%| 
   S%S     S%S  S&S  S&S     S&S           S&S     S%S    d*S        S&S     S&S       S&S  S%S    d*S       S&S       S&S  S&S 
   S&S     S&S  S&S  S&S     S&S_Ss        S&S_Ss  S&S   .S*S        S&S     S&S       S&S  S&S   .S*S       S&S       S&S  Y&Ss 
   S&S     S&S  S&S  S&S     S&S~SP        S&S~SP  S&S_sdSSS         S&S     S&S       S&S  S&S_sdSSS        S&S       S&S  `S&&S 
   S&S     S&S  S&S  S&S     S&S           S&S     S&S~YSY%b         S&S     S&S       S&S  S&S~YSY%b        S&S       S&S    `S*S 
   S*S     S*S  S*S  S*b     S*b           S*b     S*S   `S%b        S*b     S*b       d*S  S*S   `S%b       S*S       S*S     l*S 
   S*S     S*S  S*S  S*S.    S*S.          S*S.    S*S    S%S        S*S.    S*S.     .S*S  S*S    S%S       S*S       S*S    .S*P 
   S*S     S*S  S*S   SSSbs   SSSbs         SSSbs  S*S    S&S         SSSbs   SSSbs_sdSSS   S*S    S&S       S*S       S*S  sSS*S 
   SSS     S*S  S*S    YSSP    YSSP          YSSP  S*S    SSS          YSSP    YSSP~YSSY    S*S    SSS       S*S       S*S  YSS' 
           SP   SP                                 SP                                       SP               SP        SP 
           Y    Y                                  Y                                        Y                Y         Y


'''