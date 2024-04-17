from typing import List

from app.common.param.design import ModelVO
from app.repo.po import ModelPO


class ModelConverter:
    @staticmethod
    def convert_model_po_2_vo(model_po: ModelPO) -> ModelVO:
        return ModelVO(name=model_po.model_name, schema=model_po.schema)

    @staticmethod
    def convert_model_list_po_2_vo(model_po_list: List[ModelPO]) -> List[ModelVO]:
        model_vo_list = []
        for model_po in model_po_list:
            model_vo_list.append(ModelConverter.convert_model_po_2_vo(model_po))
        return model_vo_list
