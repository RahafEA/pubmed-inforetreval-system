class evaluation:
    def precision_at_k(self, retrieved, relevant, k):
        if k == 0:
            return 0.0
        retrieved_k = retrieved[:k]
        rel_retrieved = sum(1 for d in retrieved_k if d in relevant)
        return rel_retrieved / k

    def recall_at_k(self, retrieved, relevant, k):
        if not relevant:
            return 0.0
        retrieved_k = retrieved[:k]
        rel_retrieved = sum(1 for d in retrieved_k if d in relevant)
        return rel_retrieved / len(relevant)

    def f1_score(self, precision, recall):
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def average_precision(self, retrieved, relevant):
        if not relevant:
            return 0.0

        precisions = []
        num_relevant_retrieved = 0

        for i, doc_id in enumerate(retrieved, start=1):
            if doc_id in relevant:
                num_relevant_retrieved += 1
                precision_i = num_relevant_retrieved / i
                precisions.append(precision_i)

        if not precisions:
            return 0.0

        return sum(precisions) / len(relevant)

    def mean_average_precision(self, results, qrels):
        if not results:
            return 0.0

        ap_values = []
        for qid, retrieved in results.items():
            relevant = qrels.get(qid, set())
            ap = self.average_precision(retrieved, relevant)
            ap_values.append(ap)

        return sum(ap_values) / len(ap_values)

    def print_evaluation_report(self, name, results, qrels, k=3):
        print("=" * 60)
        print(f"System: {name}")
        print("=" * 60)

        for qid, retrieved in results.items():
            relevant = qrels.get(qid, set())

            p = self.precision_at_k(retrieved, relevant, k)
            r = self.recall_at_k(retrieved, relevant, k)
            f1 = self.f1_score(p, r)
            ap = self.average_precision(retrieved, relevant)

            print(f"\nQuery: {qid}")
            print(f"  P@{k}: {p:.4f}")
            print(f"  R@{k}: {r:.4f}")
            print(f"  F1@{k}: {f1:.4f}")
            print(f"  AP: {ap:.4f}")

        map_score = self.mean_average_precision(results, qrels)
        print("\n--- Overall ---")
        print(f"MAP: {map_score:.4f}")
        print("=" * 60)
    