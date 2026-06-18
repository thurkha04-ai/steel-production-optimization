# Steel Production Optimization Model

This project implements a linear optimization model using Gurobi to determine the most profitable production plan for two steel alloys (A and B) using a set of raw metal inputs.

## Problem Overview

The model decides:
- How much of each alloy (A and B) to produce
- How much of each raw metal to use in each alloy

The goal is to maximize profit, which is:

Profit = Revenue from alloys − Cost of raw metals

## Model Structure

### Decision Variables
- `x[j]`: amount of alloy j produced
- `y[i]`: amount of raw metal i used
- `z[i,j]`: amount of raw metal i allocated to alloy j

### Constraints
- Raw metal availability limits
- Flow conservation (metal usage consistency)
- Alloy composition requirements (Fe, C, Cr, Ni, Mn ranges)

### Objective
Maximize total profit from selling alloys minus raw material costs.

## Requirements

- Python 3.x
- Gurobi Optimizer
- gurobipy package

## How to Run

```bash
python steelproduction.py
