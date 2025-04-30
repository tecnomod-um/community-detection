# feature_builder/config.py

# Diccionario con los namespaces definidos en el .ttl (prefix → URI base)
# Ajusta cada URI al valor que tengas en tu archivo .ttl
NAMESPACES = {
    'ns1': 'http://www.semanticweb.org/catimc/SemanticCommonDataModel#',  # Propiedades clínicas (hasPart, hasObservable, etc.)
    'ns2': 'http://purl.org/biotop/btl2.owl#',  # Valores cuantitativos (hasValue)
    'ns3': 'http://www.semanticweb.org/catimc/resqplus#',  # Tipos de statements (ClinicalCase, ObservationResultStatement, etc.)
}