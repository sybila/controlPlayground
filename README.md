# controlPlayground

The repository provides several tools:

### Control folder

* control of dynamical systems

### Bioreactor folder

* provides interface to command photobioreactor
* three devices are enabled: GasMixer (GMS), GasAnalyser (GAS), Photobioreactor (PBR)

```python
>>> import bioreactor

>>> node = bioreactor.Node()
>>> node.add_device("PBR", "PBR07", 72700007)
>>> node.add_device("GMS", "GMS", 46700003)
>>> node.add_device("GAS", "GAS", 42700007)

>>> print(node.PBR.get_temp())
25.68

```
