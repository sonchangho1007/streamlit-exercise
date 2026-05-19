import streamlit as st

st.title('손창호의 어플')

st.write('# 1. Markdown 텍스트 작성하기')

st.markdown("""
헤더: 
# 이것은 헤더 1입니다.
## 이것은 헤더 2입니다.
### 이것은 헤더 3입니다.
#### 이것은 헤더 4입니다.
##### 이것은 헤더 5입니다.
###### 이것은 헤더 6입니다.

목록:
- 목록 1
- 목록 2
  - 목록 2.1
    - 목록2.1.1
      - 목록2.1.1.1
      - 목록2.1.1.2

기울임: *기울임*, _기울임_

볼드체: **볼드체**, __볼드체__

기울임+볼드체: ***기울임+볼드체***, ___기울임+볼드체___
""")

import pandas as pd

st.write('# 2. DataFrame 표시하기')
df = pd.DataFrame({
    '이름': ['홍길동', '이순신', '강감찬'],
    '나이': [20, 45, 35]
})

st.dataframe(df)


import numpy as np

st.write('# 그래프 표시하기')
chart_data = pd.DataFrame(np.random.randn(20, 3), columns = ["a", "b", "c"])

st.bar_chart(chart_data)

from PIL import Image

st.write('# 4. 이미지 표시하기')
img = Image.open('assets/chatgpt.jpg')
st.image(img, width=300)

"""
이 부분은 파이썬 코드상으로는 단순 문자열이지만,
:red[**Streamlit에서 자동으로 실제 컨텐츠처럼 렌더링 해줍니다.**]
"""
