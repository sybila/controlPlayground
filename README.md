# controlPlayground

The repository provides several tools:

### Control folder

* control of dynamical systems

### Bioreactor folder

* provides interface to operate photobioreactor
* three devices are enabled: Photobioreactor (PBR), GasMixer (GMS), GasAnalyser (GAS)

```python
>>> import bioreactor

>>> node = bioreactor.Node()
>>> node.add_device("PBR", "PBR07", 72700007)
>>> node.add_device("GMS", "GMS", 46700003)
>>> node.add_device("GAS", "GAS", 42700007)

>>> print(node.PBR.get_temp())
25.68

```

> When testing all the functionality, it is useful to use *fake* bioreactor. In order to do it, uncomment `TESTING` part in main.py file and comment out `EXPERIMENTS` part.