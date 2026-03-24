

from ir_system import InformationRetrievalSystem
from processing_text import Processing_Text
import pandas as pd
import os

from evaluation import evaluation

def build_ir_system():
    # قراءة CSV
    df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "pubmed_cancer_1000.csv"),
    encoding="latin1"
      )

    # إزالة أي أسطر فاضية في العمود abstract
    df = df.dropna(subset=['abstract'])

    # حفظ نسخة من Abstract الأصلي و Title
    df['original_abstract'] = df['abstract']
    df['title'] = df['title']  # تأكد إن العمود موجود في CSV

    # المعالجة للنصوص
    processor = Processing_Text()
    df['processed_abstract'] = df['abstract'].apply(processor.text_process)

    # تحضير المستندات للـ IR system (processed)
    documents = {str(row['pmid']): row['processed_abstract'] for _, row in df.iterrows()}

    # حفظ المستندات الأصلية للعرض في GUI مع Title
    original_documents = {
        str(row['pmid']): {
            "title": row['title'],
            "abstract": row['original_abstract']
        } for _, row in df.iterrows()
    }

    # إنشاء IR system
    ir_system = InformationRetrievalSystem(documents)
    return ir_system, processor, original_documents



def run_evaluation():
    evaluator = evaluation()

    qrels = {
        "Q1": {"D1", "D3", "D5"},
        "Q2": {"D2", "D7"},
        "Q3": {"D4", "D6", "D9"},
        "Q4": {"D8", "D10"},
        "Q5": {"D11", "D13"},
        "Q6": {"D12", "D14", "D16"},
        "Q7": {"D4", "D15"},
        "Q8": {"D17", "D18"},
        "Q9": {"D19"},
        "Q10": {"D20", "D1"},
    }

    boolean_results = {
        "Q1": ["D1", "D3"],
        "Q2": ["D7"],
        "Q3": ["D6", "D4"],
        "Q4": ["D10"],
        "Q5": ["D11"],
        "Q6": ["D14", "D12"],
        "Q7": ["D15"],
        "Q8": ["D18"],
        "Q9": ["D19"],
        "Q10": ["D20", "D1"],
    }

    vector_results = {
        "Q1": ["D3", "D5", "D1", "D9"],
        "Q2": ["D2", "D7", "D4"],
        "Q3": ["D6", "D4", "D9", "D2"],
        "Q4": ["D10", "D8"],
        "Q5": ["D11", "D13", "D7"],
        "Q6": ["D12", "D14", "D16", "D1"],
        "Q7": ["D4", "D15", "D6"],
        "Q8": ["D17", "D18", "D2"],
        "Q9": ["D19", "D3"],
        "Q10": ["D20", "D1", "D3"],
    }

    evaluator.print_evaluation_report(
        "Boolean Model",
        boolean_results,
        qrels,
        k=5
    )

    evaluator.print_evaluation_report(
        "Vector Space Model",
        vector_results,
        qrels,
        k=5
    )


if __name__ == "__main__":
    ir_system, processor, original_documents = build_ir_system()
    run_evaluation()




