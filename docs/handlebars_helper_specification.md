# Glynt Document Variable-set Specification #

This document is the specification document for clause variables that will be used in the glynt document system.
They are handlebars helper methods; and are simply javascript that can be modified and aliased ad nauseum.

They exist in order to make authoring a document as simple as possible

The stanzas are constructed in the form:


# Name #
Description

1. var name: type [*defaults|a|b|where * indicates default value for a param] description

__e.g.__

    Usage Example

** Additional info and usage notes **


# The Glynt Document variable Set #


## Document Variables ##
Standard variables; the default value is defined by the content in-between the "{{#doc_var}}{{/doc_var}}" tags

1. name: String - The variable by which this object is referred to within the document context

__e.g.__

    {{#doc_var name="my_variable_name"}}Some Content Goes here and is the Default Value of the my_variable_name var{{/doc_var}}


## Choice Variables ##
Allow the user to select from a pre-determined set of variable options; or enter their own value if is_static=false

1. name: String - The variable by which this object is referred to within the document context
2. can_toggle: Boolean [true|*false] - Allows the user to turn this clause on or off
3. choices: List ['a','b','c','d'] - Will provide a selection of options the user can select from
4. is_static: Boolean [*true|false] - If true, then the user can choose only 1 of the variables specified by "choices". If false they can enter their own value as well as the ones provided by "choices"

__e.g.__

    {{#doc_choice name="my_variable_name" choices=['a','b','c'] is_static=true}}{{/doc_choice}}

** The default is always the first in the list. **


## Select Clause ##
Select clauses are designed to allow the user to select 1 or more statements or even sections of a document.

1. name: String - The variable by which this object is referred to within the document context
2. multi: Boolean [true|*false] - Can the user select more than 1 of the clauses
3. can_toggle: Boolean [true|*false] - Allows the user to turn this clause on or off

__e.g.__

    {{#doc_select name="my_variable_name"}}
    Clause A
    {{doc_select}}
    Clause B
    {{doc_select}}
    Clause C
    {{/doc_select}}


## Multi-Select Clauses ##
Allow the user to select more than 1 clause; and are simply the doc_select handler with multi set to true.

__e.g.__

    {{#doc_select name="my_variable_name" multi=true}}
    Clause A
    {{doc_select}}
    Clause B
    {{doc_select}}
    Clause C
    {{/doc_select}}

** see Select Clause **
