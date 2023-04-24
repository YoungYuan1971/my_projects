import streamlit as st


def bmi(height, weight):  # 计算BMI
    bmi_value = weight / (height / 100) ** 2
    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'),
                  (22.9, '正常'), (27.5, '过重'),
                  (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    for top, status in top_status:
        if bmi_value <= top:
            return bmi_value, status


def main():
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        st.write('<center>BMI 计算器</center><br>', unsafe_allow_html=True)
        height = st.number_input("请输入你的身高(cm)：", min_value=0, step=10)
        weight = st.number_input("请输入你的体重(kg)：", min_value=0, step=10)
        try:
            bmi_value, status = bmi(height, weight)
            st.write(f'你的 BMI 值：{bmi_value:.1f}，身体状态：{status}')
        except ZeroDivisionError:
            pass


if __name__ == '__main__':
    main()
