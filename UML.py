[comment]
/*******************************************************************************
 * Copyright (c) 2015-2017 GenMyModel
 * See the file located at https://github.com/genmymodel/generators/blob/master/LICENSE for copying permission.
 *
 * This python codegen generates __init__.py files for each package and applies
 * a one class per file strategy.
 * __init__.py file is empty but if you want to deal with autoimports, set the
 * "autoimport" variable line 21 to "true" 
 *
 * Author:  Vincent Aranega - GenMyModel
 *******************************************************************************
[/comment]
[module python_modules('http://www.eclipse.org/uml2/4.0.0/UML')/]


[**
 * Main entry point. This main template MUST be named 'generate' and it must
 * own the main annotation.
 */]
[template public generate(m : Package)]
[comment @main/]
[file (m.qualifiedName.replaceAll('::', '/') + '/__init__.py', false, 'UTF-8')]
[let autoimport : Boolean = true]
[if (autoimport)]
[if (not m.ownedComment->isEmpty())]
"""
[m.ownedComment.genComment(' ')/]
"""

[/if]
[for (e : Classifier | m.ownedType->filter(Classifier)->reject(oclIsKindOf(Association))) before('__all__ = [') separator(', ') after(']')]
"[e.name/]"[/for]


[for (e : Classifier | m.ownedType->filter(Classifier)->reject(oclIsKindOf(Association)))]
from .[e.name/] import [e.name/]
[/for]
[/if]
[/let]
[/file]
[m.genPackageContent()/]
[/template]

[**
 * This template generates a package content (one class per file)
 */]
[template public genPackageContent(m : Package)]
[for (e : Classifier | m.ownedElement->filter(Classifier)->reject(oclIsKindOf(Association)))]
[file(e.qualifiedName.replaceAll('::', '/') + '.py', false, 'UTF-8')]
[comment Dummy and very simple import management (misses the extern module imports) /]
[if (not m.allOwnedElements()->filter(TypedElement)->select(type <> null and type.name <> null and type.name = 'Date')->isEmpty())]
from datetime import datetime

[/if]
[comment Generate code for classes/interfaces /]
[e.genClassif()/]
[/file]
[/for]
[/template]

[**
 * These templates are used to generate 'Classifier' code, i.e., Class, Interface and Enumeration.
 */]
[template public genClassif(e : Classifier)/]
[template public genClassif(c : Class)]
[let inherited : Bag(Classifier) = c.superClass->union(c.interfaceRealization.contract)]
[for (cl : Classifier | inherited)]
[if (cl.getNearestPackage() <> c.getNearestPackage())]
from [cl.qualifiedName.replaceAll('::', '.')/] import [cl.name/]
[/if]
[/for]

class [c.name/]([if (not inherited->isEmpty())][for (cl : Classifier | inherited) separator(', ')][cl.name/][/for][else]object[/if]):
    [if (not c.ownedComment->isEmpty())]
    """
    [c.ownedComment.genComment(' ')/]
    """
    [/if]
    [let navig : Bag(Property) = c.getAssociations().navigableOwnedEnd->select(type <> c)]
    [if (not c.ownedAttribute->union(navig)->isEmpty())]
    def __init__(self):
        [c.ownedAttribute->union(navig).gen()/]
    [else]
    pass
    [/if][/let]
    # [protected ('-> properties/constructors for ' + c.name + ' class')]

    # [/protected]
    [if (not c.nestedClassifier->isEmpty())]
    [c.nestedClassifier.genClassif()/]
    [/if]
    [if (not c.ownedOperation->isEmpty())]
        [for (ops : Operation | c.ownedOperation)]
    [ops.gen()/]
        [/for]
    [/if]
    # [protected ('-> methods for ' + c.name + ' class')]

    # [/protected]
[/let]
[/template]

[template public genClassif(i : Interface)]
[let inherited : Bag(Classifier) = i.generalization.general]
class [i.name/]([if (not inherited->isEmpty())][for (cl : Classifier | inherited) separator(', ')][cl.name/][/for][else]object[/if]):
    [if (not i.ownedComment->isEmpty())]
    """
    [i.ownedComment.genComment(' ')/]
    """
    [/if]
    [let navig : Bag(Property) = i.getAssociations().navigableOwnedEnd->select(type <> i)]
    [if (not i.ownedAttribute->union(navig)->isEmpty())]
    def __init__(self):
        [i.ownedAttribute->union(navig).gen()/]
    [else]
    pass
    [/if][/let]
    # [protected ('-> properties/constructors for ' + i.name + ' class(interface)')]

    # [/protected]
    [if (not i.nestedClassifier->isEmpty())]
    [i.nestedClassifier.genClassif()/]
    [/if]
    [if (not i.ownedOperation->isEmpty())]
        [for (ops : Operation | i.ownedOperation)]
    [ops.gen()/]
        [/for]
    [/if]
    # [protected ('-> methods for ' + i.name + ' class(interface)')]

    # [/protected]
[/let]
[/template]

[**
 * This template represents the choice we made about UML Enumeration
 * compilation to python code.
 */]
[template public genClassif(e : Enumeration)]
class [e.name/]:
    [if (not e.ownedComment->isEmpty())]
    """
    [e.ownedComment.genComment(' ')/]
    """
    [/if]
    [if (not e.ownedLiteral->isEmpty())]
    [for (lit : EnumerationLiteral | e.ownedLiteral) separator(', ')][lit.name/][/for] = range([e.ownedLiteral->size()/])
    [/if]
[/template]

[template public gen(p : Property)]
[if (not p.ownedComment->isEmpty())]
[p.ownedComment.genComment('#')/]

[/if]
self.[if (p.visibility = VisibilityKind::_private)]__[/if][p.name/] = [p.genValue()/]

[/template]

[template public gen(o : Operation)]
[o.header()/]
    [if (not o.ownedComment->isEmpty())]
    ""
    [o.ownedComment.genComment(' ')/]
    """
    [/if]
    [o.bodyOperation()/]	
[/template]

[**
 * Generate an operation header. If the operation visibility is set to
 * private, '__' prefixes the operation name.
 */]
[template public header(o : Operation)]
def [if (o.visibility = VisibilityKind::_private)]__[/if][o.name/](self[for (param : Parameter | o.ownedParameter->excluding(o.getReturnResult())) before (', ') separator(', ')][param.name/][/for]):
[/template]

[template public bodyOperation(o : Operation)]
# [protected ('protected zone for ' + o.name + ' function body')]
[if (o.getReturnResult() <> null and o.getReturnResult().type <> null)]
return [o.getReturnResult().genValue()/]
[else]raise NotImplementedError
[/if]
# [/protected]
[/template]

[template public genValue(m : MultiplicityElement) post (trim())]
[if (m.isMany())]['['/]]
[elseif (m.oclIsKindOf(TypedElement))][m.oclAsType(TypedElement).type.genSingleValue()/]
[else]None
[/if]
[/template]

[**
 * Generate single values for methods and attributes initialization.
 */]
[template public genSingleValue(t : Type) ? (not t.oclIsUndefined()) post (trim())]
[if (t.name = 'String')]""
[elseif (t.name = 'UnlimitedNatural')]0L
[elseif (t.name = 'Double')]0.
[elseif (t.name = 'Real')]0.
[elseif (t.name = 'Float')]0.
[elseif (t.name = 'Long')]0L
[elseif (t.name = 'Integer')]0
[elseif (t.name = 'Short')]0
[elseif (t.name = 'Byte')]0x0
[elseif (t.name = 'ByteArray')]['['/]]
[elseif (t.name = 'Boolean')]False
[elseif (t.name = 'Date')]datetime()
[elseif (t.name = 'Char')]''
[elseif (t.oclIsKindOf(Enumeration))][if (not t.oclAsType(Enumeration).ownedLiteral->isEmpty())][t.name/].[t.oclAsType(Enumeration).ownedLiteral->at(1).name/][else]None[/if]
[elseif (t.oclIsKindOf(Classifier))]None
[else]None[/if]
[/template]

[template public genComment(c : Comment, prefix : String)]
[prefix/][c.genBody(prefix).replaceAll('\n','\n' + prefix + ' ')/]
[/template]

[template public genBody(c : Comment, prefix : String)]
[c._body/][if (not c.ownedComment->isEmpty())]['\n'/][prefix/] [c.ownedComment.genBody(prefix)->sep('\n ' + prefix)/][/if]
[/template]

[query public isMany(s : MultiplicityElement) : Boolean =
    s.lower > 1 or s.upper = -1 or s.upper > 1 
/]

[query public isAssociation(p : Property) : Boolean =
    not p.association.oclIsUndefined()
/]