USABILITY_DOMAIN = """The Usability domain in a BioCompute Object is a plain languages description
of what was done in the project or paper workflow. The Usasability domain conveys the purpose
of the Biocompute Object. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/usability_domain.json",
    "type": "array",
    "title": "Usability Domain",
    "description": "Author-defined usability domain of the IEEE-2791 Object. This field is to aid in search-ability and provide a specific description of the function of the object.",
    "items": {
        "type": "string",
        "description": "Free text values that can be used to provide scientific reasoning and purpose for the experiment",
        "examples": [
            "Identify baseline single nucleotide polymorphisms SNPs [SO:0000694], insertions [so:SO:0000667], and deletions [so:SO:0000045] that correlate with reduced ledipasvir [pubchem.compound:67505836] antiviral drug efficacy in Hepatitis C virus subtype 1 [taxonomy:31646]",
            "Identify treatment emergent amino acid substitutions [so:SO:0000048] that correlate with antiviral drug treatment failure",
            "Determine whether the treatment emergent amino acid substitutions [so:SO:0000048] identified correlate with treatment failure involving other drugs against the same virus"
        ]
    }
}
"""

IO_DOMAIN = """The Input Output domain (or IO domain) represents the list of global input and output files created by the computational workflow,
excluding the intermediate files. These fields are pointers to objects that can reside in the system performing
the ecomputation or any other accessible system. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/io_domain.json",
    "type": "object",
    "title": "Input and Output Domain",
    "description": "The list of global input and output files created by the computational workflow, excluding the intermediate files. Custom to every specific IEEE-2791 Object implementation, these fields are pointers to objects that can reside in the system performing the computation or any other accessible system.",
    "required": [
        "input_subdomain",
        "output_subdomain"
    ],
    "properties": {
        "input_subdomain": {
            "type": "array",
            "title": "input_domain",
            "description": "A record of the references and input files for the entire pipeline. Each type of input file is listed under a key for that type.",
            "items": {
                "additionalProperties": false,
                "type": "object",
                "required": [
                    "uri"
                ],
                "properties": {
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        },
        "output_subdomain": {
            "type": "array",
            "title": "output_subdomain",
            "description": "A record of the outputs for the entire pipeline.",
            "items": {
                "type": "object",
                "title": "The Items Schema",
                "required": [
                    "mediatype",
                    "uri"
                ],
                "properties": {
                    "mediatype": {
                        "type": "string",
                        "title": "mediatype",
                        "description": "https://www.iana.org/assignments/media-types/",
                        "default": "application/octet-stream",
                        "examples": [
                            "text/csv"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        }
    }
}
"""

DESCRIPTION_DOMAIN = """The description domain specifies structured fields for the description of external
resources, the pipeline steps, and the relationship of I/O objects. Information in this domain is not used
for computation. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/description_domain.json",
    "type": "object",
    "title": "Description Domain",
    "description": "Structured field for description of external references, the pipeline steps, and the relationship of I/O objects.",
    "required": [
        "keywords",
        "pipeline_steps"
    ],
    "properties": {
        "keywords": {
            "type": "array",
            "description": "Keywords to aid in search-ability and description of the object.",
            "items": {
                "type": "string",
                "description": "This field should take free text value using common biological research terminology.",
                "examples": [
                    "HCV1a",
                    "Ledipasvir",
                    "antiviral resistance",
                    "SNP",
                    "amino acid substitutions"
                ]
            }
        },
        "xref": {
            "type": "array",
            "description": "List of the databases or ontology IDs that are cross-referenced in the IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "External references are stored in the form of prefixed identifiers (CURIEs). These CURIEs map directly to the URIs maintained by Identifiers.org.",
                "reference": "https://identifiers.org/",
                "required": [
                    "namespace",
                    "name",
                    "ids",
                    "access_time"
                ],
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "External resource vendor prefix",
                        "examples": [
                            "pubchem.compound"
                        ]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of external reference",
                        "examples": [
                            "PubChem-compound"
                        ]
                    },
                    "ids": {
                        "type": "array",
                        "description": "List of reference identifiers",
                        "items": {
                            "type": "string",
                            "description": "Reference identifier",
                            "examples": [
                                "67505836"
                            ]
                        }
                    },
                    "access_time": {
                        "type": "string",
                        "description": "Date and time the external reference was accessed",
                        "format": "date-time"
                    }
                }
            }
        },
        "platform": {
            "type": "array",
            "description": "reference to a particular deployment of an existing platform where this IEEE-2791 Object can be reproduced.",
            "items": {
                "type": "string",
                "examples": [
                    "hive"
                ]
            }
        },
        "pipeline_steps": {
            "type": "array",
            "description": "Each individual tool (or a well defined and reusable script) is represented as a step. Parallel processes are given the same step number.",
            "items": {
                "additionalProperties": false,
                "type": "object",
                "required": [
                    "step_number",
                    "name",
                    "description",
                    "input_list",
                    "output_list"
                ],
                "properties": {
                    "step_number": {
                        "type": "integer",
                        "description": "Non-negative integer value representing the position of the tool in a one-dimensional representation of the pipeline."
                    },
                    "name": {
                        "type": "string",
                        "description": "This is a recognized name of the software tool",
                        "examples": [
                            "HIVE-hexagon"
                        ]
                    },
                    "description": {
                        "type": "string",
                        "description": "Specific purpose of the tool.",
                        "examples": [
                            "Alignment of reads to a set of references"
                        ]
                    },
                    "version": {
                        "type": "string",
                        "description": "Version assigned to the instance of the tool used corresponding to the upstream release.",
                        "examples": [
                            "1.3"
                        ]
                    },
                    "prerequisite": {
                        "type": "array",
                        "description": "Reference or required prereqs",
                        "items": {
                            "type": "object",
                            "description": "Text value to indicate a package or prerequisite for running the tool used.",
                            "required": [
                                "name",
                                "uri"
                            ],
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Public searchable name for reference or prereq.",
                                    "examples": [
                                        "Hepatitis C virus genotype 1"
                                    ]
                                },
                                "uri": {
                                    "$ref": "2791object.json#/definitions/uri"
                                }
                            }
                        }
                    },
                    "input_list": {
                        "type": "array",
                        "description": "URIs (expressed as a URN or URL) of the input files for each tool.",
                        "items": {
                            "$ref": "2791object.json#/definitions/uri"
                        }
                    },
                    "output_list": {
                        "type": "array",
                        "description": "URIs (expressed as a URN or URL) of the output files for each tool.",
                        "items": {
                            "$ref": "2791object.json#/definitions/uri"
                        }
                    }
                }
            }
        }
    }
}
"""

EXECUTION_DOMAIN = """The Execution domain specifies information needed for deployment, software configuration,
and running applications in a dependent environment. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/execution_domain.json",
    "type": "object",
    "title": "Execution Domain",
    "description": "The fields required for execution of the IEEE-2791 Object are herein encapsulated together in order to clearly separate information needed for deployment, software configuration, and running applications in a dependent environment",
    "required": [
        "script",
        "script_driver",
        "software_prerequisites",
        "external_data_endpoints",
        "environment_variables"
    ],
    "additionalProperties": false,
    "properties": {
        "script": {
            "type": "array",
            "description": "points to a script object or objects that was used to perform computations for this IEEE-2791 Object instance.",
            "items": {
                "additionalProperties": false,
                "properties": {
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
			}
        },
        "script_driver": {
            "type": "string",
            "description": "Indication of the kind of executable that can be launched in order to perform a sequence of commands described in the script in order to run the pipelin",
            "examples": [
                "hive",
                "cwl-runner",
                "shell"
            ]
        },
        "software_prerequisites": {
            "type": "array",
            "description": "Minimal necessary prerequisites, library, tool versions needed to successfully run the script to produce this IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "A necessary prerequisite, library, or tool version.",
                "required": [
                    "name",
                    "version",
                    "uri"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Names of software prerequisites",
                        "examples": [
                            "HIVE-hexagon"
                        ]
                    },
                    "version": {
                        "type": "string",
                        "description": "Versions of the software prerequisites",
                        "examples": [
                            "babajanian.1"
                        ]
                    },
                    "uri": {
                        "$ref": "2791object.json#/definitions/uri"
                    }
                }
            }
        },
        "external_data_endpoints": {
            "type": "array",
            "description": "Minimal necessary domain-specific external data source access in order to successfully run the script to produce this IEEE-2791 Object.",
            "items": {
                "type": "object",
                "description": "Requirement for network protocol endpoints used by a pipeline’s scripts, or other software.",
                "required": [
                    "name",
                    "url"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Description of the service that is accessed",
                        "examples": [
                            "HIVE",
                            "access to e-utils"
                        ]
                    },
                    "url": {
                        "type": "string",
                        "description": "The endpoint to be accessed.",
                        "examples": [
                            "https://hive.biochemistry.gwu.edu/dna.cgi?cmd=login"
                        ]
                    }
                }
            }
        },
        "environment_variables": {
            "type": "object",
            "description": "Environmental parameters that are useful to configure the execution environment on the target platform.",
            "additionalProperties": false,
            "patternProperties": {
                "^[a-zA-Z_]+[a-zA-Z0-9_]*$": {
                    "type": "string"
                }
            }
        }
    }
}
"""

PARAMETRIC_DOMAIN = """The parametric domain represents a list of parameters customizing the computational flow which can affect the output of the calculations. These fields can be custom to each kind of analysis andn are tied to a particular pipeline implementation. This domain as a whole is optional so if there is no information in the paper that fits this domain then you can indicate that to the user. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/parametric_domain.json",
    "type": "array",
    "title": "Parametric Domain",
    "description": "This represents the list of NON-default parameters customizing the computational flow which can affect the output of the calculations. These fields can be custom to each kind of analysis and are tied to a particular pipeline implementation",
    "items":{
        "required": [
            "param",
            "value",
            "step"
        ],
        "additionalProperties": false,
        "properties": {
            "param": {
                "type": "string",
                "title": "param",
                "description": "Specific variables for the computational workflow",
                "examples": [
                    "seed"
                ]
            },
            "value": {
                "type": "string",
                "description": "Specific (non-default) parameter values for the computational workflow",
                "title": "value",
                "examples": [
                    "14"
                ]
            },
            "step": {
                "type": "string",
                "title": "step",
                "description": "Refers to the specific step of the workflow relevant to the parameters specified in 'param' and 'value'",
                "examples": [
                    "1"
                ],
                "pattern": "^(.*)$"
            }
        }
    }
}
"""

ERROR_DOMAIN = """The error domain can be used to determine what range of input returns and outputs are within the tolerance level defined in this subdomain and therefore can be used to optimize the algorithm. It consists of two subdomains: empirical and algorithmic. The empirical error subdomain contains empirically determined values such as limits of detectability, false positives, false negatives, statistical confidence of outcomes, etc. The algorithmic subdomain is descriptive of errors that originate by the fuzziness of the algorithms. This domain as a whole is optional so if there is no information in the paper that fits this domain then you can indicate that to the user. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/2791/error_domain.json",
    "type": "object",
    "title": "Error Domain",
    "description": "Fields in the Error Domain are open-ended and not restricted nor defined by the IEEE-2791 standard. It is RECOMMENDED that the keys directly under empirical_error and algorithmic_error use a full URI. Resolving the URI SHOULD give a JSON Schema or textual definition of the field. Other keys are not allowed error_domain",
    "additionalProperties": false,
    "required": [
        "empirical_error",
        "algorithmic_error"
    ],
    "properties": {
        "empirical_error": {
            "type": "object",
            "title": "Empirical Error",
            "description": "empirically determined values such as limits of detectability, false positives, false negatives, statistical confidence of outcomes, etc. This can be measured by running the algorithm on multiple data samples of the usability domain or through the use of carefully designed in-silico data."
        },
        "algorithmic_error": {
            "type": "object",
            "title": "Algorithmic Error",
            "description": "descriptive of errors that originate by fuzziness of the algorithms, driven by stochastic processes, in dynamically parallelized multi-threaded executions, or in machine learning methodologies where the state of the machine can affect the outcome."
        }
    }
}
"""
