[comment]
/*******************************************************************************
 * Copyright (c) 2015-2017 GenMyModel
 * See the file located at https://github.com/genmymodel/generators/blob/master/LICENSE for copying permission.
 *
 * This is a MTL generator template
 * See: 
 * Language Reference: http://help.eclipse.org/juno/topic/org.eclipse.acceleo.doc/pages/reference/language.html?cp=5_3_0
 * Operations: http://help.eclipse.org/juno/topic/org.eclipse.acceleo.doc/pages/reference/operations.html?cp=5_3_2
 * Text production rules: http://help.eclipse.org/juno/topic/org.eclipse.acceleo.doc/pages/reference/textproductionrules.html?cp=5_3_5
 *
 * Author:  Vincent Aranega - GenMyModel
 * Contributor:  Alexis Muller - GenMyModel
 *******************************************************************************
[/comment]
[module uml2python('http://www.eclipse.org/uml2/4.0.0/UML')/]


[comment]
 Main entry point. This main template MUST be named 'generate' and it must
 own the main annotation.
[/comment]
[template public generate(m : Package)]
[comment @main/]
[file (m.name.concat('.py'), false, 'UTF-8')]
[if (not m.ownedComment->isEmpty())]
"""
[m.ownedComment.genComment(' ')/]
"""

[/if]
[comment Dummy and very simple import management (misses the extern module imports) /]
[if (not m.allOwnedElements()->filter(TypedElement)->select(type <> null and type.name <> null and type.name = 'Date')->isEmpty())]
from datetime import datetime

[/if]
[comment Generate code for classes/interfaces /]
[let nonInherit : Set(Classifier) = 
    m.ownedElement->
        filter(Classifier)->
            select(generalization->isEmpty())->reject(oclIsKindOf(Class) and not oclAsType(Class).interfaceRealization->isEmpty())]
[for (e : Classifier | nonInherit->sortedBy(not oclIsKindOf(Enumeration)))]
[e.genClassif()/]
[/for]
[for (e : Classifier | m.ownedElement->filter(Classifier)
                        ->select(c | nonInherit->excludes(c))
                        ->sortedBy(getAllUsedInterfaces()->union(getGenerals())->size()))]
[e.genClassif()/]
[/for]
[/let]

# [protected ('-> functions/methods for ' + m.name + ' package')]

# [/protected]
[/file]
[/template]

[comment]
 These templates are used to generate 'Classifier' code, i.e., Class, Interface and Enumeration.
[/comment]
[template public genClassif(e : Classifier)/]
[template public genClassif(c : Class)]
[let inherited : Bag(Classifier) = c.superClass->union(c.interfaceRealization.contract)]
class [c.name/]([if (not inherited->isEmpty())][for (cl : Classifier | inherited) separator(', ')][cl.name/][/for][else]object[/if]):
    [if (not c.ownedComment->isEmpty())]
    """
    [c.ownedComment.genComment(' ')/]
    """
    [/if]
    [let navig : Bag(Property) = c.getAssociations().navigableOwnedEnd->select(type <> c)]
    [if (not c.ownedAttribute->union(navig)->isEmpty())]
    def __init__(self):
        [c.ownedAttribute.gen()/]
        [navig.gen()/]
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
        [i.ownedAttribute.gen()/]
        [navig.gen()/]
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

[comment]
 This template represents the choice we made about UML Enumeration
 compilation to python code.
[/comment]
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
    """
    [o.ownedComment.genComment(' ')/]
    """
    [/if]
    [o.bodyOperation()/]	
[/template]

[comment]
 Generate an operation header. If the operation visibility is set to
 private, '__' prefixes the operation name.
[/comment]
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

[comment]
 Generate single values for methods and attributes initialization.
[/comment]
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