from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import TypeAliasType, AnyType, TypeOfAny


class ReturnTypePlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        if fullname.endswith("return_type.ReturnType"):

            def hook(ana: AnalyzeTypeContext):
                tp = ana.type
                api = ana.api

                if tp.args:
                    arg = tp.args[0]
                    arg_tp = api.anal_type(arg)
                    if isinstance(arg_tp, TypeAliasType):
                        arg_tp = arg_tp.alias.target
                    return arg_tp.ret_type
                return AnyType(TypeOfAny.from_omitted_generics)

            return hook


def plugin(version: str):
    return ReturnTypePlugin
