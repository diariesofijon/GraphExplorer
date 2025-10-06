#!/usr/bin/env python

# We'll generate TWO separate graphs:
# 1. Half-year education plan graph (foundational roadmap)
# 2. Post-plan deepening graph (advanced exploration)

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display



'''
  There is a cool and stuffed examination that shows on a data set of
  pre-structured manually Python's code in a Pythonic way. You can use
  it as a mixture for TDD model or even manual testing. Also it could
  usefull find new info and can be inserted by new updated info. It
  could be recensy or even new publishing house and edition!

  To use it as library or executable pythonic script just od it:
    1. pip install pandas
    2. pip install matplotlib
    3. pip install networkx
    4. pip install jupyter 
    5. pip install notebook
    6. pip install jupyterlab
    7. pip install ipython

    It's required python 3.12.6 as minimum

    requirements.txt ->
        astroid==3.3.11
        asttokens==3.0.0
        certifi==2025.8.3
        colorama==0.4.6
        contourpy==1.3.3
        cycler==0.12.1
        decorator==5.2.1
        dill==0.4.0
        distlib==0.4.0
        executing==2.2.1
        filelock==3.19.1
        fonttools==4.59.2
        ipython==9.5.0
        ipython_pygments_lexers==1.1.1
        isort==6.0.1
        jedi==0.19.2
        kiwisolver==1.4.9
        matplotlib==3.10.6
        matplotlib-inline==0.1.7
        mccabe==0.7.0
        networkx==3.5
        numpy==2.3.3
        packaging==25.0
        pandas==2.3.2
        parso==0.8.5
        pillow==11.3.0
        pipenv==2025.0.4
        platformdirs==4.4.0
        prompt_toolkit==3.0.52
        pure_eval==0.2.3
        Pygments==2.19.2
        pylint==3.3.8
        pyparsing==3.2.4
        python-dateutil==2.9.0.post0
        pytz==2025.2
        setuptools==80.9.0
        six==1.17.0
        stack-data==0.6.3
        tomlkit==0.13.3
        traitlets==5.14.3
        tzdata==2025.2
        virtualenv==20.34.0
        wcwidth==0.2.13

'''


# ---------------------------
# Half-Year Education Plan Graph
# ---------------------------
plan_nodes = [
    {
        "id": "Criminology_Basics", 
        "label": "Criminology: The Basics (Walklate)", 
        "type": "book", 
        "url": "https://www.amazon.com/Criminology-Basics-Sandra-Walklate/dp/103269517X"},
    {
        "id": "Inside_CriminalMind", 
        "label": "Inside the Criminal Mind (Samenow)", 
        "type": "book", 
        "url": 
            "https://www.penguinrandomhouse.com/books/235734/inside-the-criminal-mind-newly-revised-edition-by-stanton-samenow/"},
    {
        "id": "Healing_CPTSD", 
        "label": "Healing Complex PTSD (Brown)", 
        "type": "book", 
        "url": "https://link.springer.com/book/10.1007/978-3-030-61416-4"},
    {
        "id": "Trauma_Handbook", 
        "label": "International Handbook of Human Response to Trauma (Shalev et al.)", 
        "type": "book", 
        "url": 
            "https://link.springer.com/book/10.1007/978-1-4615-4177-6"},
    {
        "id": "Motivational_Interviewing", 
        "label": "Motivational Interviewing (Miller & Rollnick)", 
        "type": "book", 
        "url": 
            "https://www.guilford.com/books/Motivational-Interviewing/Miller-Rollnick/9781462552795"},
    {
        "id": "Criminalistics", 
        "label": "Criminalistics: Intro to Forensic Science (Saferstein)", 
        "type": "book", 
        "url": 
            "https://www.pearson.com/en-us/subject-catalog/p/criminalistics-an-introduction-to-forensic-science/P200000001769/9780137542512"},
    {
        "id": "What_Works", 
        "label": "What Works in Crime Prevention & Rehab (Weisburd)", 
        "type": "book", 
        "url": "https://link.springer.com/book/10.1007/978-1-4939-3477-5"},
    {
        "id": "arXiv_ips_2305", 
        "label": "Incremental Propensity Score Effects (arXiv:2305.14040)", 
        "type": "paper", 
        "url": "https://arxiv.org/abs/2305.14040"},
    {
        "id": "arXiv_fairness_1703", 
        "label": "Fairness in CJ Risk Assessments (arXiv:1703.09207)", 
        "type": "paper", 
        "url": "https://arxiv.org/abs/1703.09207"},
    {
        "id": "arXiv_monotonic_2301", 
        "label": "Monotonicity in AI Ethics (arXiv:2301.07060)", 
        "type": "paper", 
        "url": "https://arxiv.org/abs/2301.07060"},
    {
        "id": "arXiv_crim_org_2403", 
        "label": "Criminal Organizations Resilience (arXiv:2403.03720)", 
        "type": "paper", 
        "url": "https://arxiv.org/abs/2403.03720"},
    {
        "id": "arXiv_hotspot_2506", 
        "label": "Crime Hotspot Prediction w/ GCNs (arXiv:2506.13116)", 
        "type": "paper", 
        "url": "https://arxiv.org/abs/2506.13116"}
]

plan_edges = [
    ("Criminology_Basics", "Inside_CriminalMind"),
    ("Criminology_Basics", "What_Works"),
    ("Inside_CriminalMind", "Motivational_Interviewing"),
    ("Healing_CPTSD", "Motivational_Interviewing"),
    ("Trauma_Handbook", "Healing_CPTSD"),
    ("Trauma_Handbook", "arXiv_ips_2305"),
    ("What_Works", "arXiv_ips_2305"),
    ("What_Works", "arXiv_hotspot_2506"),
    ("arXiv_fairness_1703", "arXiv_monotonic_2301"),
    ("arXiv_fairness_1703", "arXiv_hotspot_2506"),
    ("arXiv_monotonic_2301", "arXiv_hotspot_2506"),
    ("arXiv_crim_org_2403", "What_Works"),
    ("Criminalistics", "arXiv_hotspot_2506"),
    ("Motivational_Interviewing", "arXiv_ips_2305")
]

G_plan = nx.DiGraph()
for n in plan_nodes:
    G_plan.add_node(n["id"], label=n["label"], url=n["url"], type=n["type"])
for e in plan_edges:
    G_plan.add_edge(e[0], e[1])


# ---------------------------
# Post-Plan Deepening Graph
# ---------------------------
deep_nodes = [
    {
      "id": "Oxford_Handbook", 
      "label": "Oxford Handbook of Criminology", 
      "type": "book", 
      "url": 
        "https://global.oup.com/academic/product/the-oxford-handbook-of-criminology-9780198860914"},
    {
      "id": "Punishment_Structure",
      "label": "Punishment and Social Structure (Rusche & Kirchheimer)", 
      "type": "book", 
      "url": 
        "https://www.routledge.com/Punishment-and-Social-Structure/Rusche-Kirchheimer/p/book/9781412809990"},
    {
      "id": "Crime_Everyday_Life", 
      "label": "Crime and Everyday Life (Felson)",
      "type": "book", 
      "url": 
        "https://www.routledge.com/Crime-and-Everyday-Life/Felson/p/book/9781544375893"},
    {
      "id": "Theoretical_Criminology", 
      "label": "Theoretical Criminology (Young, Taylor, Walton)", 
      "type": "book", 
      "url": "https://journals.sagepub.com/home/tcr"},
    {
      "id": "Methods_Criminology", 
      "label": "Empirical Methods in Criminology", 
      "type": "book", 
      "url": "https://link.springer.com/book/10.1007/978-3-030-50992-7"},
    {
      "id": "arXiv_fairness_survey", 
      "label": "Recent Advances in Algorithmic Fairness & CJ (arXiv survey)", 
      "type": "paper", 
      "url": "https://arxiv.org/abs/2401.00001"}
]

deep_edges = [
    ("Oxford_Handbook", "Methods_Criminology"),
    ("Oxford_Handbook", "Theoretical_Criminology"),
    ("Punishment_Structure", "Theoretical_Criminology"),
    ("Crime_Everyday_Life", "Oxford_Handbook"),
    ("Methods_Criminology", "arXiv_fairness_survey"),
    ("Oxford_Handbook", "arXiv_fairness_survey")
]

G_deep = nx.DiGraph()
for n in deep_nodes:
    G_deep.add_node(n["id"], label=n["label"], url=n["url"], type=n["type"])
for e in deep_edges:
    G_deep.add_edge(e[0], e[1])



plan_df = pd.DataFrame(
    [{
        "id": n["id"],
        "title": n["label"],
        "type": n["type"],
        "link": n["url"]} for n in plan_nodes]) 

deep_df = pd.DataFrame(
    [{
        "id": n["id"], 
        "title": n["label"],
        "type": n["type"], 
        "link": n["url"]} for n in deep_nodes])


if __name__ == '__main__':
    plt.figure(figsize=(12,10))
    pos = nx.spring_layout(G_plan, seed=42, k=0.8)
    labels = {
        node: G_plan.nodes[node]["label"].split(
            "(")[0] for node in G_plan.nodes()}
    nx.draw(G_plan, pos, with_labels=False, node_size=2000)
    nx.draw_networkx_labels(G_plan, pos, labels, font_size=8)
    plt.title(
        "Half-Year Education Plan: Criminology Books & Papers", fontsize=12)
    plt.axis('off')
    plt.show()
    

    display("Half-Year Plan Nodes", plan_df)
    
    plt.figure(figsize=(12,10))
    pos = nx.spring_layout(G_deep, seed=42, k=0.8)
    labels = {
        node: G_deep.nodes[node]["label"].split(
            "(")[0] for node in G_deep.nodes()}
    nx.draw(G_deep, pos, with_labels=False, node_size=2000)
    nx.draw_networkx_labels(G_deep, pos, labels, font_size=8)
    plt.title(
        "Post-Plan Deepening: Advanced Criminology Resources", fontsize=12)
    plt.axis('off')
    plt.show()
    

    display("Post-Plan Deepening Nodes", deep_df)
