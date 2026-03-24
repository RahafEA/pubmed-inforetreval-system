# -*- coding: utf-8 -*-
"""Fetch Pubmed Cancer"""

import time
import pandas as pd
from Bio import Entrez

Entrez.email = "rahafelhawy@gmail.com"

class PubMedFetcher:
    def search_pubmed(self, query, max_results=1000):
        print(f"Searching PubMed for: '{query}'")
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
        record = Entrez.read(handle)
        handle.close()
        pmids = record.get("IdList", [])
        print(f"Found {len(pmids)} articles")
        return pmids

    def fetch_article_details(self, pmid):
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
            record = Entrez.read(handle)
            handle.close()

            article = record['PubmedArticle'][0]
            medline = article['MedlineCitation']
            article_data = medline['Article']

            title = article_data.get('ArticleTitle', "")
            abstract_list = article_data.get('Abstract', {}).get('AbstractText', [])
            abstract = " ".join(str(x) for x in abstract_list) if abstract_list else ""

            authors_raw = article_data.get('AuthorList', [])
            authors = []
            for a in authors_raw:
                last = a.get('LastName', '')
                initials = a.get('Initials', '')
                full = f"{last} {initials}".strip()
                if full:
                    authors.append(full)

            journal = article_data.get('Journal', {}).get('Title', "")
            pub_date = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})

            return {
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'pub_date': pub_date
            }
        except Exception as e:
            print(f"Error fetching PMID {pmid}: {e}")
            return None

    def fetch_multiple_articles(self, pmids, delay=0.4):
        articles = []
        for i, pmid in enumerate(pmids):
            print(f"Fetching article {i+1}/{len(pmids)}: PMID {pmid}")
            details = self.fetch_article_details(pmid)
            if details:
                articles.append(details)
            time.sleep(delay)
        return articles

    def save_articles_to_csv(self, query, max_results=1000, filename="pubmed_cancer_1000.csv"):
        pmids = self.search_pubmed(query, max_results)
        articles = self.fetch_multiple_articles(pmids)
        df = pd.DataFrame(articles)
        df['authors'] = df['authors'].apply(lambda x: '; '.join(x) if isinstance(x, list) else str(x))
        df.to_csv(filename, index=False, encoding='utf-8')
        return df
