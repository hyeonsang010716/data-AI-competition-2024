import csv

qa_data_kr = [
    {"Question": "신도시 지역의 평준화 교육에 대한 논의는 무엇인가요?", 
     "Answer": "신도시 지역에서는 평준화 교육에 대한 논의가 있으며, 비평준화 지역과 평준화 지역 간의 학업 성취도 차이가 낮다는 내용이 있습니다.",
     "Text Reference": "평준화교육 정책과 관련한 논의는 여러 지역에서 진행되고 있으며, 신도시지역의 평준화 정책에 대한 조사 결과와 학부모의 의견을 종합하여 내년 초에 정책을 결정할 예정입니다."},
    
    {"Question": "국가기밀 또는 개인 사생활 침해 여부를 판단하는 책임은 누구에게 있나요?", 
     "Answer": "국가기밀 또는 개인 사생활 침해 여부는 감청을 요구한 기관의 책임으로 보고 있습니다.",
     "Text Reference": "네, 정보통신부가 국가기관인지 여부와 해당 내용이 국가기밀 또는 개인의 사생활 침해인지 여부에 대한 판단은 감청을 요구한 기관의 책임으로 보고 있습니다."},
    
    {"Question": "수협의 경제 사업 운영과 관련된 문제가 무엇인가요?", 
     "Answer": "수협의 경제 사업 운영과 부동산 자산 관리 문제가 지적되었으나, 해결 방안에 대한 명확한 답변을 얻지 못했습니다.",
     "Text Reference": "현 상황에서 수협의 경제사업 운영과 부동산 자산 관리에 대한 문제가 지적되었으며, 수협의 필요성과 해당 문제에 대한 해결 방안에 대한 명확한 답변을 얻지 못한 상태입니다."},
    
    {"Question": "부탄가스 흡입 사고를 예방하기 위한 대책은 무엇인가요?", 
     "Answer": "부탄가스에 고미제 첨가를 의무화하고 있으며, 사고 예방을 위해 대책을 수립 중입니다.",
     "Text Reference": "고미제 첨가는 1998년 7월 1일 이후로 의무화되었으나, 현재 고미제가 일반 부탄가스에 혼합되지 않아 효용가치가 없는 상태입니다."},
    
    {"Question": "도시철도 부채 절감과 관련된 정책은 무엇인가요?", 
     "Answer": "도시철도 부채 절감과 표준화 사업에 대한 대책이 진행 중이며, SOC 사업비 증액이 필요하다고 생각됩니다.",
     "Text Reference": "도시철도 부채절감과 적정운임, 도시철도 표준화 사업에 대한 대책과 방침은 진행 중이며, SOC 사업비의 증액이 건설산업 활성화에 필요하다고 생각하며, SOC 예산이 차지하는 비중이 많을수록 좋다고 봅니다."},
    
    {"Question": "한국 아파트 재건축 주기는 다른 나라와 어떻게 비교되나요?", 
     "Answer": "한국의 아파트 재건축 주기는 미국, 영국 등과 비교해 짧으며, 졸속으로 이루어지고 있다는 비판이 있습니다.",
     "Text Reference": "저 역시 이와 같은 의견을 가지고 있습니다. 한국에서의 아파트 재건축 상황은 너무 졸속하게 이루어지고, 적절한 도시 계획이 부족한 것으로 생각됩니다."},
    
    {"Question": "사격장 안전법에 대해서 알려줘.", 
     "Answer": "현재 한국에서 개인이 운영하는 사격장에서 만 14세 이상의 청소년들은 특정 조건을 만족할 경우 사격을 할 수 있습니다.",
     "Text Reference": "현재 개인이 운영하는 사격장에서 14∼19세 학생들의 출입 현황에 대한 구체적인 정보가 있나요? 이 법이 안전을 강화하면서 사업 영역에서 어떠한 변화가 예상되고 있는지 설명해 주실 수 있을까요? 현재까지의 구체적인 출입 현황에 대한 정보는 확인되지 않았으며, 이 법이 안전을 강화하는 측면에서 어떤 영향을 미칠지에 대한 정확한 예측은 어려우나, 부모나 선생님이 동반된 경우에는 미성년자도 사격을 할 수 있는 기회가 제공될 것으로 예상됩니다."},
    
    {"Question": "그린벨트 외 지역에서 임대주택 개발이 가능한가요?", 
     "Answer": "그린벨트 외 지역에서도 임대주택 개발이 일부 이루어지고 있으며, 건교부와 협의 중입니다.",
     "Text Reference": "그린벨트 이외의 지역에서도 임대주택 활성화를 위해 일부 지구지정이 이루어지고 있습니다."},
    
    {"Question": "증권시장과 선물시장 통합에 대한 상공회의소의 입장은 무엇인가요?", 
     "Answer": "상공회의소는 증권시장과 선물시장 통합 계획에 대해 우려하고 있으며, 부산 지역 선물거래소 유치에 대한 어려움을 느끼고 있습니다.",
     "Text Reference": "상공회의소는 증권시장과 선물시장의 통합 및 지주회사 설립 계획에 대한 우려를 가지고 있으며, 부산 지역 상공업계 역시 선물거래소의 부산 유치가 어려워질 우려를 품고 있습니다."},
    
    {"Question": "노사분규와 관련한 정부의 대책은 무엇인가요?", 
     "Answer": "정부는 노사분규에 대한 대응을 강화하고, 인력 문제 해결과 제조원가 개선을 위해 노력하고 있습니다.",
     "Text Reference": "노사분규의 불법 행위에 대한 대응 강화 및 형평 원칙의 적용, 인력 문제 관리, 제조원가 개선 및 경쟁력 향상, 그리고 고정부채와 세금 관련 문제의 검토와 개선 노력을 지속적으로 진행하겠습니다."},
]

# Writing the Korean CSV with text references
csv_file_path_kr = "./assets/qa_pairs.csv"

# Writing to the CSV file
with open(csv_file_path_kr, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Question", "Answer", "Text Reference"])
    writer.writeheader()
    writer.writerows(qa_data_kr)

csv_file_path_kr
