import pandas as pd
import os, sys

if __name__ == '__main__':
    if not os.path.exists(sys.argv[1]):
        raise EnvironmentError("file", sys.argv[1], " not existed")
    if not os.path.exists("url_downloaded.csv"):
        raise EnvironmentError("file url_downloaded.csv not existed")
    df = pd.read_csv("url_downloaded.csv")
    downloaded_urls = list(df["link"])
    df2 = pd.read_csv(sys.argv[1])
    urls = list(df2["link"])
    exited_count = 0
    for i, url in enumerate(urls):
        if url in downloaded_urls:
            print(url, "existed")
            exited_count = exited_count + 1
            df2 = df2[df2.link != url]
            continue
    df2.to_csv(sys.argv[1], index=False)
    print("Removed=", exited_count)