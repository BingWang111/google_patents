import os
import json
import multiprocessing

ipt_dirt = "/Volumes/WDC3/google_patents/publications/"
opt_dirt = "/Volumes/WDC3/google_patents/tidydata/"
finished = "finished.txt"

if not os.path.exists(os.path.join(opt_dirt, finished)):
    with open(os.path.join(opt_dirt, finished), 'w') as file:
        pass

def parser(file, ipt_dirt, opt_dirt, finished):
    if file.startswith('ggpatentdata'):
        with open(ipt_dirt+file, "r") as f:
            for pt in f.readlines():
                patent = json.loads(pt)
                with open(opt_dirt+'app_pub_number.txt','a') as fs:
                    fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format("|", patent["publication_number"],
                                                      patent["application_number"],
                                                      patent["country_code"],
                                                      patent["application_kind"],
                                                      patent["pct_number"],
                                                      patent["family_id"]))
                with open(opt_dirt+'date.txt','a') as fs:
                    fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format("|",patent["publication_number"],
                                                      patent["application_number"],
                                                      patent["publication_date"],
                                                      patent["filing_date"],
                                                      patent["grant_date"],
                                                      patent["priority_date"]))
        with open(os.path.join(opt_dirt, finished), 'a') as fs:
            fs.write(file+'\n')
                # if len(patent["title_localized"]) > 0:
                #     with open(opt_dirt+'title.txt','a') as fs:
                #         fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           patent["title_localized"][0]["text"]))
                # if len(patent["abstract_localized"]) > 0:
                #     with open(opt_dirt+'abstract.txt','a') as fs:
                #         fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           patent["abstract_localized"][0]["text"]))
                # if len(patent["claims_localized"]) > 0:
                #     claim = {'app_num': patent["application_number"],
                #              'claims':patent["claims_localized"][0]["text"]}
                #     with open(opt_dirt+'claims.txt','a') as fs:
                #         fs.write(json.dumps(claim)+'\n')
                # if len(patent["description_localized"]) > 0:
                #     descr = {'app_num': patent["application_number"],
                #              'descrip':patent["description_localized"][0]["text"]}
                #     with open(opt_dirt+'description.txt','a') as fs:
                #         fs.write(json.dumps(descr)+'\n')
                # if len(patent["ipc"]) > 0:
                #     for ipc in patent["ipc"]:
                #         with open(opt_dirt + 'ipc.txt', 'a') as fs:
                #             fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           ipc["code"]))
                # if len(patent["citation"]) > 0:
                #     for cite in patent["citation"]:
                #         if cite["npl_text"].__len__() > 0:
                #             with open(opt_dirt+"npc.txt","a") as fs:
                #                 fs.write("{1}{0}{2}{0}{3}\n".format("|",patent["publication_number"],
                #                                                   cite["npl_text"],cite["category"]))
                #         else:
                #             with open(opt_dirt+"backward.txt","a") as fs:
                #                 fs.write("{1}{0}{2}{0}{3}\n".format("|",patent["publication_number"],
                #                                                   cite["publication_number"],
                #                                                   cite["application_number"],
                #                                                   cite["type"],
                #                                                   cite["category"]))

if __name__ == '__main__':
    files = os.listdir(ipt_dirt)
    with open(os.path.join(opt_dirt, finished), 'r') as file:
        finish = [line.strip() for line in file.readlines()]
    pool = multiprocessing.Pool(12)
    for file in files:
        print(file)
        if file not in finish:
            pool.apply_async(func=parser, args=(file, ipt_dirt, opt_dirt, finished,))
    pool.close()
    pool.join()
