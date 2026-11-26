import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    n = len(corpus)
    links = corpus[page]

    # A page with no links is treated as linking to every page (itself included)
    if not links:
        return {p: 1 / n for p in corpus}

    distribution = {p: (1 - damping_factor) / n for p in corpus}
    for link in links:
        distribution[link] += damping_factor / len(links)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {p: 0 for p in corpus}

    # First sample: a page chosen at random
    page = random.choice(list(corpus))
    counts[page] += 1

    # Remaining samples: generated from the previous sample's transition model
    for _ in range(n - 1):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model), weights=list(model.values()), k=1)[0]
        counts[page] += 1

    return {p: counts[p] / n for p in corpus}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {p: 1 / n for p in corpus}

    # A page with no links is interpreted as linking to every page
    outgoing = {
        p: (set(corpus) if not links else links)
        for p, links in corpus.items()
    }

    while True:
        new_ranks = {}
        for page in corpus:
            incoming = sum(
                ranks[other] / len(outgoing[other])
                for other in corpus
                if page in outgoing[other]
            )
            new_ranks[page] = (1 - damping_factor) / n + damping_factor * incoming

        converged = all(abs(new_ranks[p] - ranks[p]) <= 0.001 for p in corpus)
        ranks = new_ranks
        if converged:
            break

    return ranks


if __name__ == "__main__":
    main()
