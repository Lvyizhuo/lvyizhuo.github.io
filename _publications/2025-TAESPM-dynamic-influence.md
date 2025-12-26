---
title: "TAESPM: A Learning-Based Spatiotemporal Prediction Framework for Dynamic Influence Maximization"
collection: publications
category: manuscripts
permalink: /publication/2025-12-31-taespm-dynamic-influence
excerpt: 'This paper proposes TAESPM, a learning-based spatiotemporal prediction framework designed to overcome the "Myopic Trap" in dynamic influence maximization by capturing long-range dependencies.'
date: 2025-12-31
venue: 'Submitted to IEEE Transactions on Network Science and Engineering (TNSE)'
paperurl: 'https://lvyizhuo.github.io/DocsWeb/'
citation: 'Lvyizhuo, et al. (2025). &quot;TAESPM: A Learning-Based Spatiotemporal Prediction Framework for Dynamic Influence Maximization.&quot; <i>(Under Review in IEEE TNSE)</i>.'
---

## Abstract
In dynamic social networks, identifying critical nodes capable of sustaining influence is paramount. However, existing methodologies frequently succumb to the **"Myopic Trap"**, leading to suboptimal strategies. We propose **TAESPM**, a spatiotemporal prediction framework that forecasts high-potential nodes by synergistically modeling evolutionary characteristics. Specifically, we devise a **Time-aware Influence Capacity (TIFC)** metric and a hybrid encoder (GNN-BiLSTM) with a **Temporal Awareness Enhancement Module (TAEM)**. Experimental results show an accuracy of up to **98%** in candidate node prediction, significantly outperforming SOTA benchmarks on the Cumulative Temporal Spread metric.

## Key Contributions
* **Adaptive Optimization (TIFC)**: A novel methodology that models historical decay effects and neighbor emergence to measure dynamic nodal influence precisely.
* **Hybrid Spatiotemporal Architecture**: Seamlessly integrates GNN and BiLSTM to facilitate multi-scale feature fusion across evolving network topologies.
* **Temporal Awareness Enhancement Module (TAEM)**: Explicitly captures long-range dependencies and critical inflection points, overcoming the forgetting issues of traditional RNN/LSTM models.
* **Performance & Efficiency**: Achieves up to 98% prediction accuracy while drastically curtailing search space and computational overhead in complex dynamic scenarios.

## Keywords
* Dynamic Social Networks
* Influence Maximization
* Spatiotemporal Deep Learning
* Predictive Modeling

---
*The contents above are part of a manuscript currently under professional review. For more information, please visit the [project documentation](https://lvyizhuo.github.io/DocsWeb/).*