from typing import List, Dict

from domains.lex.entity.const import BuildKey
from domains.lex.infra.node import BaseNode, Operation, OperationCategory, Id, ExpressionOperations, TermOperations
from domains.lex.infra.parser import YaccAnalyzer, visit_tree, NodeKind
import domains.item.service.item_facade as item_facade


def get_attr_before_visit(node: BaseNode, names: List[str]):
    if node.kind == NodeKind.Id.value:
        names.append(node.name)
    return


def build_expression_sql(node: Operation) -> str:
    sql = ''
    if node.category == OperationCategory.And.value:
        if node.left.value:
            sql = node.left.get_extra(BuildKey)
        elif node.right.value:
            sql = node.right.get_extra(BuildKey)
        else:
            sql = '( ' + node.left.get_extra(BuildKey) + ' ) and ( ' + node.right.get_extra(BuildKey) + ' )'
    elif node.category == OperationCategory.Or.value:
        sql = '( ' + node.left.get_extra(BuildKey) + ' ) or ( ' + node.right.get_extra(BuildKey) + ' )'
    else:
        raise ValueError(f'[build_expression_sql]: invalid expression node category {node}')
    return sql


def build_term_sql(node: Operation) -> str:
    sql = ''
    if node.right.value is None:
        raise ValueError(f'[build_query_before_visit]: Id at term`s right {node}')
    if node.category == OperationCategory.Eq.value:
        sql = node.left.get_extra(BuildKey) + ' = ' + node.right.get_extra(BuildKey)
    elif node.category == OperationCategory.Le.value:
        sql = node.left.get_extra(BuildKey) + ' >= ' + node.right.get_extra(BuildKey)
    elif node.category == OperationCategory.Lt.value:
        sql = node.left.get_extra(BuildKey) + ' > ' + node.right.get_extra(BuildKey)
    elif node.category == OperationCategory.Se.value:
        sql = node.left.get_extra(BuildKey) + ' <= ' + node.right.get_extra(BuildKey)
    elif node.category == OperationCategory.St.value:
        sql = node.left.get_extra(BuildKey) + ' < ' + node.right.get_extra(BuildKey)
    else:
        raise ValueError(f'[build_term_sql]: invalid expression node category {node}')
    return sql


def build_query_after_visit(node: BaseNode, key2id: Dict[str, int]):
    sql = ''
    if node.kind == NodeKind.Id.value:
        node: Id
        if node.name not in key2id.keys():
            raise ValueError(f"[build_query_after_visit] Id name not in attr key2id map")
        sql = f'attach_id = {key2id[node.name]} and extra'
    elif node.kind == NodeKind.Num.value:
        sql = str(node.value)
    elif node.kind == NodeKind.Str.value:
        sql = "'" + node.value + "'"
    else:
        if node.kind != NodeKind.Operation.value:
            raise ValueError(f"[build_query_before_visit]: invalid node {node}")
        node: Operation
        if node.value is not None:
            if node.value:
                sql = '1 = 1'
            else:
                sql = '1 != 1'
        elif node.category in ExpressionOperations:
            sql = build_expression_sql(node)
        elif node.category in TermOperations:
            sql = build_term_sql(node)
        else:
            raise ValueError(f"[build_query_before_visit]: invalid operation category or Id at opration left {node}")
    node.set_extra(BuildKey, sql)
    return


class SyntaxAnalyzeServiceSupplier(object):
    def __init__(self, in_str, debug: bool = False):
        self._analyzer = YaccAnalyzer(debug)
        self._Sql = None
        try:
            self._tree = self._analyzer.get_ast_tree(in_str)
            self._attr_names = list()
            visit_tree(self._tree, get_attr_before_visit, None, self._attr_names)
            self._attr_names = list(set(self._attr_names))
            self._key2attr = {item.key: item for item in item_facade.get_attributes_by_keys(keys=self._attr_names)}
        except Exception as e:
            raise Exception(f"init syntax analyze service fail: {e}")

    @property
    def tree(self):
        return self._tree

    @property
    def attr_names(self):
        return self._attr_names

    @property
    def attrs(self):
        return self._name_to_attr.values()

    def convert_to_sql(self):
        if not self._Sql:
            visit_tree(self._tree, None, build_query_after_visit, self._key2attr)
            self._Sql = 'where ' + self._tree.get_extra(BuildKey)
        return self._Sql


if __name__ == '__main__':
    supplier = SyntaxAnalyzeServiceSupplier('(a <= 1 & b = 2) | c = 3', True)
    tokens = supplier.attr_names
    sql = supplier.convert_to_sql()
    print(tokens)
